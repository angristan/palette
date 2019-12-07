import cv2
import numpy as np
import imutils

from sklearn.cluster import KMeans
from webcolors import rgb_to_hex

def kmeans(img, k):
    # the number of clusters indicate how many leading colors we want (k of k-means)
    model = KMeans(n_clusters=k, init='random', random_state=88)
    model.fit(img)

    return model


def transform_img(filepath):
    img = cv2.imread(filepath)
    img = imutils.resize(img, width=300)

    # by default, cv2 uses BGR so we need to change it to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # row * column, and number of color channels (3 because of RGB)
    img = img.reshape((img.shape[0] * img.shape[1], 3))

    return img

def get_tints(filepath, n_tints):
    img = transform_img(filepath)

    model = kmeans(img, n_tints)

    dominant_colors_rgb = model.cluster_centers_.astype(int)

    return list(map(rgb_to_hex, tuple(dominant_colors_rgb)))
