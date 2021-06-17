import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.naive_bayes import BernoulliNB
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier


def report(test, model):
    predicted = model.predict(test['x'])

    p_bool = predicted.astype(bool)
    t_bool = test['y'].astype(bool)

    compared = predicted == test['y']
    true_positives = np.logical_and(t_bool, p_bool).sum()
    false_positives = np.logical_and(~t_bool, p_bool).sum()
    true_negatives = np.logical_and(~t_bool, ~p_bool).sum()
    actual_positives = t_bool.sum()
    actual_negatives = t_bool.size - actual_positives

    accuracy = compared.sum() / compared.size
    misclassification = 1 - accuracy
    tpr = true_positives / actual_positives
    fpr = false_positives / actual_negatives
    tnr = true_negatives / actual_negatives
    precision = true_positives / compared.sum()
    prevalence = actual_positives / compared.size

    print(f'Accuracy: {round(accuracy, 2)}')
    print(f'Misclassification rate: {round(misclassification, 2)}')
    print(f'True positive rate: {round(tpr, 2)}')
    print(f'False positive rate: {round(fpr, 2)}')
    print(f'True negative rate: {round(tnr, 2)}')
    print(f'Precision: {round(precision, 2)}')
    print(f'Prevalence: {round(prevalence, 2)}')

    print(model.score(test['x'], test['y']))
    print(confusion_matrix(test['y'], predicted))
    print(classification_report(test['y'], predicted))


def bayes(train, test):
    model = BernoulliNB()
    model.fit(train['x'], train['y'])
    report(test, model)
    return model


def neural_net(train, test):
    mlp = MLPClassifier(solver='lbfgs')
    mlp.fit(train['x'], train['y'].values.ravel())
    report(test, mlp)
    return mlp


def decision_tree(train, test):
    tree = DecisionTreeClassifier()
    tree.fit(train['x'], train['y'])
    report(test, tree)
    return tree


def kmeans(train, test):
    model = KMeans()
    model.fit(train['x'])
    predicted = model.predict(test['x'])
    compared = predicted == test['y'].to_numpy(dtype=int)
    print(round((compared.sum() / compared.size) * 100, 2))
    return model
