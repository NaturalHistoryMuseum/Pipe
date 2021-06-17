import os

import dill
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MultiLabelBinarizer

from annette.db import SessionManager
from annette.db.models import Citation, ManualClassification
from annette.train.utils import train_test


class BaseAttributeCluster(object):
    attribute_name = ''

    def __init__(self):
        self._binariser = None
        self._kmeans_model = None
        self._records = self.get_records()
        self.data = pd.DataFrame(self._records)
        self.binarised_data = self.transform_data(self.data[self.attribute_name])
        self.train, self.test = train_test(self.binarised_data, self.data['class'])

    @property
    def binariser(self):
        if self._binariser is None:
            all_labels = list(
                set([item for r in self._records for item in
                     self.tokenise(r[self.attribute_name])]))
            self._binariser = MultiLabelBinarizer()
            self._binariser.fit([all_labels])
        return self._binariser

    def kmeans_model(self, filepath=None, ignore_no_file=True, n_clusters=2):
        if filepath is not None and os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                self._kmeans_model = dill.load(f)
        elif filepath is not None and not ignore_no_file:
            raise FileNotFoundError(f'Saved model not found at {filepath}.')
        else:
            if self._kmeans_model is None:
                self._kmeans_model = KMeans(n_clusters=n_clusters)
                self._kmeans_model.fit(self.train['x'])
            if filepath is not None:
                with open(filepath, 'wb') as f:
                    dill.dump(self._kmeans_model, f)
        return self._kmeans_model

    def get_records(self):
        attr = getattr(Citation, self.attribute_name)

        with SessionManager() as session_manager:
            citations = session_manager.session.query(attr,
                                                      ManualClassification.classification_id) \
                .join(ManualClassification, Citation.doi == ManualClassification.doi) \
                .group_by(attr, ManualClassification.classification_id).all()

        return [{
            self.attribute_name: getattr(c, self.attribute_name) if getattr(c,
                                                                            self.attribute_name)
                                                                    is not None else '',
            'class': c.classification_id
            } for c in citations]

    @staticmethod
    def tokenise(input_string):
        return [t.strip().lower() for t in input_string.split(',')]

    def transform_data(self, data):
        binarised_data = self.binariser.transform([self.tokenise(x) for x in data])
        return binarised_data
