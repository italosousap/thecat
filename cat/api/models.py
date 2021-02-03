from api import db, ma


class Breed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    origin = db.Column(db.String(100))
    temperament = db.Column(db.String(200))
    description = db.Column(db.String(500))
    image = db.relationship('BreedImage', backref='breed')


class BreedImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_breed = db.Column(db.Integer, db.ForeignKey('breed.id'), nullable=False)
    url_image = db.Column(db.String(200))


class BreedSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Breed
        include_relationships = True
    
    id = ma.auto_field()
    name = ma.auto_field()
    origin = ma.auto_field()
    temperament = ma.auto_field()
    description = ma.auto_field()
    image = ma.auto_field()


class BreedImageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BreedImage
        include_relationships = True
        include_fk = True

    url_image = ma.auto_field()


#create database
db.drop_all()
db.create_all()
