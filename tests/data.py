from datetime import datetime as dt

from annette.db.models import Access, Citation, ExtractedCitation, Metrics, Name, RunLog, Taxonomy


def runlog(**kwargs):
    data = dict(start=dt.strptime('2000-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
                end=dt.strptime('2000-01-01 01:00:00', '%Y-%m-%d %H:%M:%S'),
                harvest=True,
                identify=True,
                enhance=True,
                classify=True)
    data.update(kwargs)
    return RunLog(**data)


def citation(**kwargs):
    data = dict(doi='10.1002/ajb2.1133',
                author='Aubriot, Xavier; Knapp, Sandra; Syfert, Mindy M.; Poczai, '
                       'Péter; Buerki, Sven',
                title='Shedding new light on the origin and spread of the brinjal eggplant ('
                      'Solanum melongena L.) and its wild relatives',
                type='journal-article',
                issued_date=dt.strptime('2018-07-01', '%Y-%m-%d'),
                subject='Plant Science,Genetics,Ecology, Evolution, Behavior and Systematics',
                pub_title='American Journal of Botany',
                pub_publisher='Wiley',
                issn='0002-9122',
                isbn=None,
                issue='7',
                volume='105',
                page='1175-1187',
                ecid=1,
                log_id=2,
                classification_id=1)
    data.update(kwargs)
    return Citation(**data)


def extracted_citation(**kwargs):
    data = dict(email_id='not-a-real-id',
                title='Shedding new light on the origin and spread of the '
                      'brinjal eggplant (Solanum melongena L.) and its '
                      'wild relatives',
                snippet='Page 1. American Journal of Botany 105(7): 1–13, '
                        '2018; http://www.wileyonlinelibrary. com/journal/AJB © 2018 '
                        'Botanical Society of America • 1 Crop wild relatives (CWRs) '
                        'are likely to play a significant role in securing 21st '
                        'century',
                author='X Aubriot, S Knapp, MM Syfert, P Poczai, S Buerki',
                pub_title='American journal of botany',
                pub_year=2018,
                sent_date=dt.strptime('2018-08-14', '%Y-%m-%d'),
                source='GS',
                id_status=0,
                label='Label_4',
                doi=None,
                snippet_match=0,
                highlight_length=0,
                last_identify_run=None,
                log_id=2)
    data.update(kwargs)
    return ExtractedCitation(**data)


def metrics(**kwargs):
    data = {
        'times_cited': 1234,
        'recent_citations': 25,
        'retrieved_date': dt.now().date(),
        'relative_citation_ratio': 0.6,
        'field_citation_ratio': 0.9,
        'log_id': 1,
        'doi': '10.1002/ajb2.1133'
        }
    data.update(kwargs)
    return Metrics(**data)


def taxonomy(**kwargs):
    return Taxonomy()


def access(**kwargs):
    data = {
        'best_oa_url': 'http://http.cat/200',
        'updated_date': dt.now().date(),
        'pdf_url': 'http://http.cat/200.pdf',
        'is_oa': True,
        'host_type': 'repository',
        'version': 'acceptedVersion',
        'log_id': 1,
        'doi': '10.1002/ajb2.1133'
        }
    data.update(kwargs)
    return Access(**data)


def name(**kwargs):
    return Name()


def get_all():
    _runlog = runlog()
    _exci = extracted_citation(log_id=_runlog.id)
    _ci = citation(log_id=_runlog.id, ecid=_exci.id)
    _met = metrics(log_id=_runlog.id, doi=_ci.doi)
    _acc = access(log_id=_runlog.id, doi=_ci.doi)
    return _runlog, _exci, _ci, _met, _acc
