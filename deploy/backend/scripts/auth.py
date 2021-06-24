from oauth2client import client, tools
from oauth2client.file import Storage
import argparse


scopes = 'https://www.googleapis.com/auth/gmail.modify'
client_secret_file = 'annette/.credentials/client_secret.json'
application_name = 'DCP Pipeline'
credential_path = 'annette/.credentials/gmail-credentials.json'

flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

store = Storage(credential_path)
credentials = store.get()

if not credentials or credentials.invalid:
    flow = client.flow_from_clientsecrets(client_secret_file, scopes)
    flow.user_agent = application_name
    credentials = tools.run_flow(flow, store, flags)
    with open(credential_path, 'w') as f:
        f.write(credentials.to_json())
