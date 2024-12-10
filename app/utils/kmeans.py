import cv2
import imutils
from sklearn.cluster import KMeans
from webcolors import rgb_to_hex


class Kmeans:
    def __init__(self, imagepath, clusters=3):
        self.clusters = clusters
        self.imagepath = imagepath
        self.img = None
        self.colors = None

    def clusterize(self):
        # the number of clusters indicate how many leading colors we want (k of k-means)
        # we use k-means++ to ensure ensures a smarter initialization of the centroids
        # and improve the quality of the clustering
        self.model = KMeans(
            n_clusters=self.clusters,
            init="k-means++",
            n_init=10,
            max_iter=300,
            algorithm="elkan",
        )
        self.model.fit(self.img)

    def transform_img(self):
        self.img = cv2.imread(self.imagepath)
        self.img = imutils.resize(self.img, width=300)

        # by default, cv2 uses BGR so we need to change it to RGB
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)

        # row * column, and number of color channels (3 because of RGB)
        self.img = self.img.reshape((self.img.shape[0] * self.img.shape[1], 3))

    def get_tints(self):
        self.transform_img()
        self.clusterize()

        self.colors = self.model.cluster_centers_.astype(int)

        return list(map(rgb_to_hex, tuple(self.colors)))
