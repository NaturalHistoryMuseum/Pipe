import abc
import argparse
import base64
import os
import re
from datetime import date
from getpass import getpass

import httplib2
import imap_tools
from apiclient import discovery, errors
from bs4 import BeautifulSoup
from oauth2client import client, tools
from oauth2client.file import Storage

from annette.db.models import ExtractedCitation
from . import _utils
from ._base import BaseHarvester


class ScholarMailHarvester(BaseHarvester):
    def __init__(self, session_manager):
        super(ScholarMailHarvester, self).__init__(session_manager)

    def get_data(self):
        """
        Runs class logic: controls flow of authentication,
        message retrieval and inbox updates.

        :return: List of Messages constructed by MessageFactory.
        These messages have been retrieved from the Gmail inbox and parsed to extract metadata.
        """
        prefer_imap = os.getenv('ANNETTE_PREFER_IMAP', 'false').lower() in ['true', '1']
        retriever = None
        if not prefer_imap:
            try:
                retriever = GmailRetriever()
            except:
                prefer_imap = True
        if prefer_imap:
            retriever = ImapRetriever()
        if retriever is None:
            return []
        emails = retriever.get_emails()

        _utils.logger.debug(f"Starting harvest. {len(emails)} new emails found.")

        extracted_citations = []
        for email in emails:
            extracted_citations += self.parse_email(email)
        return extracted_citations

    @classmethod
    def parse_email(cls, email):
        soup = BeautifulSoup(email['body'], 'html.parser')

        raw_citations = soup('h3')
        extracted_citations = []

        for i in raw_citations:
            # Retrieve + parse bib_data
            bib_data = i.find_next_sibling('div')
            parsed_bib_data = cls._parse_email_bib_data(_utils.clean_string(bib_data.text))

            # Get snippet + features from highlights
            snippet = i.find_next(class_='gse_alrt_sni')
            if snippet is None:
                snippet_distance = None
                snippet_clean = ''
            else:
                snippet_distance = _utils.minimum_word_distance(snippet.text)
                snippet_clean = _utils.clean_string(" ".join(snippet.stripped_strings))
            snippet_match = snippet_distance is not None

            # Get title
            title = _utils.clean_string(i.find('a', class_="gse_alrt_title").text)
            print(f'Email {email["id"]}. Parsing "{title}"...')

            # Build message object + add to list
            extracted_citations.append(ExtractedCitation(email_id=email['id'],
                                                         title=title,
                                                         snippet=snippet_clean,
                                                         author=parsed_bib_data['author'],
                                                         pub_title=parsed_bib_data['pub_title'],
                                                         pub_year=parsed_bib_data['pub_year'],
                                                         sent_date=email['received_date'],
                                                         source='GS',
                                                         id_status=False,
                                                         label=email['label'],
                                                         snippet_match=snippet_match,
                                                         highlight_length=snippet_distance
                                                         ))

        return extracted_citations

    @classmethod
    def _parse_email_bib_data(cls, bib_data):
        """
        Parses the string containg author name, publication title and pub year.
        :param bib_data: String
        :return: Dict containing author name, publication title and year
        """
        pub_title = None
        pub_year = None

        # Get author name(s)
        parsed_bib = bib_data.split(" - ")
        m_author = _utils.clean_string(parsed_bib[0])

        # Split further to get year and author
        if len(parsed_bib) > 1:
            parsed_b2 = parsed_bib[1].split(',')

            if len(parsed_b2) == 2:
                pub_title = _utils.clean_string(parsed_b2[0])
                try:
                    pub_year = int(_utils.clean_string(parsed_b2[1]))
                except ValueError:
                    pub_year = None

            else:
                try:
                    pub_year = int(_utils.clean_string(parsed_b2[0]))
                except ValueError:
                    pub_year = None
                    pub_title = _utils.clean_string(parsed_b2[0])

        return {
            'author': m_author,
            'pub_title': pub_title,
            'pub_year': pub_year
        }


class Retriever(abc.ABC):
    label_rgx = re.compile('^"([^"]+)"')

    def __init__(self):
        self.mailbox = self.connect()

    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def get_emails(self):
        return []


class GmailRetriever(Retriever):
    scopes = 'https://www.googleapis.com/auth/gmail.modify'
    client_secret_file = 'annette/.credentials/client_secret.json'
    application_name = 'DCP Pipeline'

    def connect(self):
        """
        Gets user credentials from storage.
        If credentials not found or invalid, the OAuth2 flow is completed to obtain the new
        credentials.

        :return: Gmail Service object
        """
        credential_path = 'annette/.credentials/gmail-credentials.json'

        store = Storage(credential_path)
        credentials = store.get()
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

        if not credentials:
            _utils.logger.debug('Credentials not found.')
        if credentials.invalid:
            _utils.logger.debug('Credentials found, but they\'re invalid.')

        if not credentials or credentials.invalid:
            raise Exception('Could not connect to Gmail.')

        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http, cache_discovery=False)
        return service

    def list_unread_emails(self):
        """
        Retrieves IDs for all unread emails from Google Scholar in the inbox.
        :return: List of unread email IDs
        """
        try:
            query = 'is:unread from:scholaralerts-noreply@google.com'
            page_token = None
            p_emails = []
            while True:
                request = self.mailbox.users().messages().list(userId='me',
                                                               q=query, pageToken=page_token)
                response = request.execute()
                if 'messages' not in response:
                    break
                p_emails.extend(response['messages'])
                if 'nextPageToken' not in response:
                    break
                page_token = response['nextPageToken']
            return p_emails

        except errors.HttpError as error:
            _utils.logger.error(f'An error occurred during unread email retrieval: ${error}')

    def util_unread(self):
        """
        A utility function for marking all Google Scholar emails as unread. For testing/dev.
        """
        try:
            query = 'from:scholaralerts-noreply@google.com'
            page_token = None
            p_emails = []
            while True:
                request = self.mailbox.users().messages().list(userId='me',
                                                               q=query, pageToken=page_token)
                response = request.execute()
                if 'messages' not in response:
                    break
                p_emails.extend(response['messages'])
                if 'nextPageToken' not in response:
                    break
                page_token = response['nextPageToken']
            self.mailbox.users().messages().batchModify(userId='me', body={
                'addLabelIds': ['UNREAD'],
                'ids': [e['id'] for e in p_emails]
            }).execute()

        except errors.HttpError as error:
            _utils.logger.error(f'An error occurred: ${error}')

    def _get_one_email(self, email_id):
        email = {
            'id': email_id,
            'harvested_date': date.today()
        }
        try:
            email_data = self.mailbox.users().messages().get(userId='me', id=email_id,
                                                             format='full').execute()
        except errors.HttpError as error:
            _utils.logger.error(f'An error occurred during full-text message retrieval: {error}')
            raise error
        email['label'] = self._get_email_label(email_data)

        email['received_date'] = date.fromtimestamp(
            int(email_data['internalDate']) / 1000).isoformat()
        encoded_body = email_data.get('payload', {}).get('body', {}).get('data', b'')
        email['body'] = base64.urlsafe_b64decode(encoded_body)
        self._mark_emails_read([email_id])
        return email

    def _get_email_label(self, email_data):
        label = None
        for lab in email_data['labelIds']:
            match = re.match("Label", lab)
            if match:
                label = lab
                break
        return label

    def _mark_emails_read(self, email_ids):
        self.mailbox.users().messages().batchModify(userId='me', body={
            'removeLabelIds': ['UNREAD'],
            'ids': email_ids
        }).execute()

    def get_emails(self):
        return [self._get_one_email(eid) for eid in self.list_unread_emails()]


class ImapRetriever(Retriever):
    def connect(self):
        server = os.getenv('IMAP_HOST') or input('IMAP server: ')
        usr = os.getenv('IMAP_EMAIL_ADDRESS') or input('Email address: ')
        pwd = os.getenv('IMAP_EMAIL_PASSWORD') or getpass()
        mailbox = imap_tools.MailBox(server)
        mailbox.login(usr, pwd, initial_folder='INBOX')
        return mailbox

    def _get_one_email(self, email: imap_tools.message.MailMessage):
        return {
            'id': email.uid,
            'harvested_date': date.today(),
            'label': self._get_email_label(email),
            'received_date': email.date.date(),
            'body': email.html
        }

    def _get_email_label(self, email: imap_tools.message.MailMessage):
        from_subject = self.label_rgx.findall(email.subject)
        if len(from_subject) > 0:
            return from_subject[0]
        else:
            return ''

    def get_emails(self):
        with self.mailbox as mailbox:
            messages = [m for m in mailbox.fetch(imap_tools.AND(seen=False, from_='scholaralerts-noreply@google.com'))]
        return [self._get_one_email(email) for email in messages]
