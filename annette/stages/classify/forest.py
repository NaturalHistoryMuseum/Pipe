import dill as pickle
import pandas as pd
from sqlalchemy import func, not_

from annette.db.models import Citation, ExtractedCitation, NHMPub
from ._base import BaseClassifier


class RandomForestClassifier(BaseClassifier):
    def __init__(self, session_manager):
        super(RandomForestClassifier, self).__init__(session_manager)
        self.model = self.load_model()

    @staticmethod
    def load_model():
        with open('annette/data/model_forest.pk', 'rb') as f:
            loaded_forest = pickle.load(f)
        return loaded_forest

    def grouped_data(self):
        q = self.session_manager.session.query(Citation.doi,
                                               func.max(not_(func.isnull(NHMPub.issn))).label(
                                                   'nhm_sub'),
                                               ExtractedCitation.snippet_match.label(
                                                   'snippet_match'),
                                               ExtractedCitation.highlight_length.label(
                                                   'highlight_length'),
                                               ExtractedCitation.label_id.label('label_id'))
        q = q.join(ExtractedCitation)
        q = q.outerjoin(NHMPub, Citation.issn == NHMPub.issn).order_by(Citation.doi)
        q = q.group_by(Citation.doi, ExtractedCitation.snippet_match,
                       ExtractedCitation.highlight_length, ExtractedCitation.label_id)

        df = pd.read_sql(q.statement, q.session.bind).drop_duplicates()

        labels = [f'Label_{i}' for i in [2, 3, 4, 5, 8]]

        for label in labels:
            if label in df.iloc[:, -1:].values:
                labels.remove(label)

        expanded_labels = pd.get_dummies(df, columns=['label_id'], prefix='L')

        aggregations = {
            'nhm_sub': 'max',
            'snippet_match': 'mean',
            'highlight_length': 'mean',
            'L_Label_1': 'max',
            'L_Label_2': 'max',
            'L_Label_3': 'max',
            'L_Label_4': 'max',
            'L_Label_5': 'max',
            'L_Label_8': 'max'
            }

        grouped_data = expanded_labels.groupby(['doi']).agg(aggregations).reset_index()
        return grouped_data.fillna(0)

    def process_data(self, citations):
        grouped_data = self.grouped_data()
        preds = self.model.predict(grouped_data.iloc[:, 1:].values)
        grouped_data['classification_id'] = pd.Series(preds, index=grouped_data.index)

        # Extract results
        results = {key: value for (key, value) in
                   zip(grouped_data.doi, grouped_data.classification_id.astype(str))}

        # Update records
        for c in citations:
            c.classification_id = results[c.doi]

        return citations
