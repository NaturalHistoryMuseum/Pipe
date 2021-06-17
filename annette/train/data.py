from sqlalchemy import func, not_

from annette.db import SessionManager
from annette.db.models import Citation, ManualClassification


def get_data(attr_name):
    """

    :param attr_name:
    :return:
    """
    attr = getattr(Citation, attr_name)

    with SessionManager() as session_manager:
        citations = session_manager.session.query(attr,
                                                  ManualClassification.classification_id) \
            .join(ManualClassification, Citation.doi == ManualClassification.doi) \
            .group_by(attr, ManualClassification.classification_id).all()

    return [{
        attr_name: getattr(c, attr_name) if getattr(c, attr_name) is not None else '',
        'class': c.classification_id
        } for c in citations]


def get_multi_data(attr_names):
    attrs = [getattr(Citation, attr_name) for attr_name in attr_names]
    with SessionManager() as session_manager:
        citations = session_manager.session.query(*attrs,
                                                  ManualClassification.classification_id) \
            .join(ManualClassification, Citation.doi == ManualClassification.doi) \
            .group_by(*attrs, ManualClassification.classification_id).all()

    data = []
    for c in citations:
        citation = {}
        for attr_name in attr_names:
            citation[attr_name] = getattr(c, attr_name) if getattr(c, attr_name) is not None else ''
        citation['class'] = c.classification_id
        data.append(citation)

    return data
