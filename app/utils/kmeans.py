import cv2
from sklearn.cluster import KMeans


def kmeans(img, k):
    # the number of clusters indicate how many leading colors we want (k of k-means)
    model = KMeans(n_clusters=k, init='random', random_state=88)
    model.fit(img)

    return model


def transform_img(filepath):
    img = cv2.imread(filepath)

    # by default, cv2 uses BGR so we need to change it to RGB
    img_data = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    r, g, b = cv2.split(img_data)

    # row * column, and number of color channels (3 because of RGB)
    img = img.reshape((img_data.shape[0] * img_data.shape[1], 3))

    return img

def get_tints(filepath, n_tints):
    img = transform_img(filepath)

    model = kmeans(img, n_tints)

    return model.cluster_centers_.tolist()
