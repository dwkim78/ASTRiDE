import numpy as np

from sklearn.cluster import Birch, KMeans, AgglomerativeClustering


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
    def __init__(self, edges, branching_factor=50, threshold=0.1):
        # Make features list.
        features = []
        for i in range(len(edges)):
            edge = edges[i]
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

        self.features = features
        self.normed_features = normed_features
        self.branching_factor = branching_factor
        self.threshold = threshold
        #self.run(Birch, branching_factor=50, threshold=0.1, n_clusters=2)
        self.run(KMeans, n_clusters=2)
        #self.run(AgglomerativeClustering, n_clusters=2)

    def run(self, clf_fnt, **kwargs):
        """
        This routine trains an outlier model to find outliers (i.e. streaks).
        """
        n_iter = 0
        curr_features = self.features.copy()
        curr_normed_features = self.normed_features.copy()
        while True and n_iter < 3:
            clf = clf_fnt(**kwargs).fit(curr_normed_features)

            if len(curr_features[(clf.labels_ == 1)]) >= 5:
                break

            print(clf.labels_)
            print(curr_features[(clf.labels_ == 1)])

            curr_features = curr_features[(clf.labels_ == 0)]
            curr_normed_features = curr_normed_features[(clf.labels_ == 0)]
            n_iter += 1






