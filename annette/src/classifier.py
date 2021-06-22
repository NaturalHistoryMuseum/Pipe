import dill as pickle
import pandas as pd
from annette.db.session import engine
import logging


class Classifier:
    def __init__(self, records):
        self.records = records
        self.model = self.load_model()
        self.data = self.load_data()
        self.grouped_data = self.shape_data(self.data)

    @staticmethod
    def load_model():
        with open('annette/data/model_forest.pk', 'rb') as f:
            loaded_forest = pickle.load(f)
        return loaded_forest

    @staticmethod
    def load_data():
        df = pd.read_sql_table('vw_classifier', engine)
        return df

    @staticmethod
    def shape_data(df):
        df3 = df.drop_duplicates().copy()

        labels = ['Label_1', 'Label_2', 'Label_3', 'Label_4', 'Label_5', 'Label_8']

        for l in labels:
            if l in df3.iloc[:, -1:].values:
                labels.remove(l)

        df4 = pd.get_dummies(df3, columns=['label'], prefix='L')

        for label in labels:
            df4[f"L_{label}"] = 0

        aggregations = {'nhm_sub': 'max',
                        'snippet_match': 'mean',
                        'highlight_length': 'mean',
                        'L_Label_1': 'max',
                        'L_Label_2': 'max',
                        'L_Label_3': 'max',
                        'L_Label_4': 'max',
                        'L_Label_5': 'max',
                        'L_Label_8': 'max'}

        grouped_data = df4.groupby(['doi']).agg(aggregations).reset_index()

        return grouped_data

    def classify(self):
        preds = self.model.predict(self.grouped_data.iloc[:, 1:].values)

        logging.info(f"Starting classification. {len(preds)} citations to classify...")

        self.grouped_data['classification_id'] = pd.Series(preds, index=self.grouped_data.index)

        # Extract results
        results = {key: value for (key, value) in zip(self.grouped_data.doi, self.grouped_data.classification_id.astype(str))}

        # Update records
        for r in self.records:
            r.classification_id = results[r.doi]

        classified_true = len([x for x in self.records if x.classification_id == '1'])
        logging.info(f"Records classified true: {classified_true}")
        logging.info(f"Records classified false: {len(self.records) - classified_true}")

        return self.records

