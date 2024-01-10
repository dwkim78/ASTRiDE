import numpy as np

from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor


class Outlier:
    """
    Detect outliers using Machine Learning Algorithm.

    This module will train a model in real-time, so it might be
    CPU-intensive and time-consuming. Still testing and under development.

    Parameters
    ----------
    edges: array_like
        A list of an edge instance.
    """
    def __init__(self, edges):
        # Make features list.
        features = []
        for edge in edges:
            features.append([edge['perimeter'], edge['area'],
                             edge['shape_factor'], edge['radius_deviation']])
        features = np.array(features)

        # Normalize features
        normed_features = features.copy()
        for i in range(features.shape[1]):
            avg = np.median(features[::, i])
            std = np.std(features[::, i])

            normed_features[::, i] -= avg
            normed_features[::, i] /= avg

        self.edges = edges
        self.features = features
        self.normed_features = normed_features

    def run(self, clf_fnt=IsolationForest, **kwargs):
        """
        This routine trains an outlier model to find outliers (i.e. streaks).
        """
        curr_normed_features = self.normed_features.copy()
        clf = clf_fnt(**kwargs).fit(curr_normed_features)

        pred = clf.predict(curr_normed_features)

        # return outliers' edges.
        return np.array(self.edges)[np.where(pred==-1)]
