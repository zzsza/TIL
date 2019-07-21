from sklearn import datasets, model_selection
from sklearn.ensemble import RandomForestClassifier
from sacred import Experiment
from sacred.observers import FileStorageObserver
from sklearn import metrics

ex = Experiment('rf')
ex.observers.append(FileStorageObserver.create('my_runs'))


@ex.config
def cfg():
    n_estimators=100
    seed = 42


@ex.capture
def get_model(n_estimators):
    return RandomForestClassifier(n_estimators)


@ex.automain
def run(_log):
    X, y = datasets.load_breast_cancer(return_X_y=True)
    _log.info("[INFO] Now split dataset in RF")
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2)
    clf = get_model()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    _log.info("[INFO] End Predict!")

    return metrics.accuracy_score(y_test, y_pred)

