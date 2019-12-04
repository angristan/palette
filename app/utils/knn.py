from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing

class Knn:

    def __init__(self):
            self.r = []
            self.g = []
            self.b = []
            self.color_names = []
            self.features = list()
            self.labels = None
            self.model = None
            self.target_colors = None

    def prepare_dataset(self):
        dataset = [
            {
                'name': 'red',
                'r': 255,
                'g': 0,
                'b': 0,
            },
            {
                'name': 'orange',
                'r': 255,
                'g': 128,
                'b': 0,
            },
            {
                'name': 'yellow',
                'r': 255,
                'g': 255,
                'b': 0,
            },
            {
                'name': 'green',
                'r': 128,
                'g': 255,
                'b': 0,
            },
            {
                'name': 'green',
                'r': 0,
                'g': 255,
                'b': 0,
            },
            {
                'name': 'green',
                'r': 0,
                'g': 255,
                'b': 128,
            },
            {
                'name': 'blue',
                'r': 0,
                'g': 255,
                'b': 255,
            },
            {
                'name': 'blue',
                'r': 0,
                'g': 128,
                'b': 255,
            },
            {
                'name': 'blue',
                'r': 0,
                'g': 0,
                'b': 255,
            },
            {
                'name': 'purple',
                'r': 127,
                'g': 0,
                'b': 255,
            },
            {
                'name': 'pink',
                'r': 255,
                'g': 0,
                'b': 255,
            },
            {
                'name': 'pink',
                'r': 255,
                'g': 0,
                'b': 127,
            },
            {
                'name': 'grey',
                'r': 128,
                'g': 128,
                'b': 128,
            },
        ]

        for color in dataset:
            self.color_names.append(color['name'])
            self.r.append(color['r'])
            self.g.append(color['g'])
            self.b.append(color['b'])

    def encode_dataset(self):
        self.prepare_dataset()

        le = preprocessing.LabelEncoder()

        r_encoded = le.fit_transform(self.r)
        g_encoded = le.fit_transform(self.g)
        b_encoded = le.fit_transform(self.b)
        self.features = list(zip(r_encoded,g_encoded,b_encoded))

        self.labels = le.fit_transform(self.color_names)


    def train_model(self):
        self.encode_dataset()

        self.target_colors = dict(zip(self.labels, self.color_names))
        # print(self.target_colors)

        self.model = KNeighborsClassifier(n_neighbors=1)

        self.model.fit(self.features, self.labels)


    def get_color_name(self,r,g,b):
        self.train_model()

        name = self.target_colors[int(self.model.predict([[r,g,b]])[0])]
        return name
