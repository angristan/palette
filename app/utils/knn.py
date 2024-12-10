import pandas as pd
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier


class Knn:

    def prepare_dataset(self):
        data = pd.read_csv("dataset/wikipedia_color_names.csv")

        self.color_names = data["name"].tolist()
        self.r = data["red"].tolist()
        self.g = data["green"].tolist()
        self.b = data["blue"].tolist()

    def encode_dataset(self):
        self.prepare_dataset()

        le = preprocessing.LabelEncoder()

        r_encoded = le.fit_transform(self.r)
        g_encoded = le.fit_transform(self.g)
        b_encoded = le.fit_transform(self.b)
        self.features = list(zip(r_encoded, g_encoded, b_encoded))

        self.labels = le.fit_transform(self.color_names)

    def train_model(self):
        self.encode_dataset()

        self.target_colors = dict(zip(self.labels, self.color_names))

        self.model = KNeighborsClassifier(n_neighbors=1)

        self.model.fit(self.features, self.labels)

    def get_color_name(self, r, g, b):
        self.train_model()

        name = self.target_colors[int(self.model.predict([[r, g, b]])[0])]
        return name
