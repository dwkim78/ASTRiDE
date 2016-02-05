import numpy as np


class EDGE:
    def __init__(self, contours):
        """
        Initialize.
        :param data: An array containing contour list.
        """
        # Set structure.
        self.edges = []
        for i in range(len(contours)):
            # Remove unclosed contours.
            if contours[i][0][0] != contours[i][-1][0] or \
               contours[i][0][1] != contours[i][-1][1]:
                continue

            self.edges.append({'positions': contours[i],
                               'x_center': 0., 'y_center': 0.,
                               'perimeter': 0., 'area': 0.,
                               'shape_factor': 0.})

    def quantify(self):
        """
        Quantify shape of the contours.
        """
        four_pi = 4. * np.pi
        for edge in self.edges:
            # Positions
            x = edge['positions'][::, 1]
            y = edge['positions'][::, 0]

            # Area.
            xyxy = (x[:-1] * y[1:] - x[1:] * y[:-1])
            A = 1. / 2. * np.sum(xyxy)

            # X and Y center.
            one_sixth_a = 1. / (6. * A)
            x_center = one_sixth_a * np.sum((x[:-1] + x[1:]) * xyxy)
            y_center = one_sixth_a * np.sum((y[:-1] + y[1:]) * xyxy)

            # Perimeter.
            perimeter = np.sum(np.sqrt((x[1:] - x[:-1])**2 +
                                       (y[1:] - y[:-1])**2))

            # Set values.
            edge['area'] = np.abs(A)
            edge['perimeter'] = perimeter
            edge['x_center'] = x_center
            edge['y_center'] = y_center
            # Circle is 1. Rectangle is 0.78. Thread-like is close to zero.
            edge['shape_factor'] = four_pi * edge['area'] / \
                                   edge['perimeter'] ** 2.

    def get_edges(self):
        return self.edges

if __name__ == '__main__':
    import pylab as pl

    contours = np.array([[[ 510.11046156,  244.        ],
     [ 510.,          243.76897833],
     [ 509.83048219,  244.        ],
     [ 510.,          244.13376629],
     [ 510.11046156,  244.        ]]])

    pl.plot(contours[0][::, 0], contours[0][::, 1])
    pl.show()

    edge = EDGE(contours)
    edge.quantify()
    print edge.get_edges()

