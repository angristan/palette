from app import db

class Color(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    r = db.Column(db.SmallInteger)
    g = db.Column(db.SmallInteger)
    b = db.Column(db.SmallInteger)

    def __repr__(self):
        return '<Color {}: {},{},{}>'.format(self.name, self.r, self.g, self.b)
