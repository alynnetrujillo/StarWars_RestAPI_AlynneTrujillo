from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    favorite_people = db.relationship('Favorite_People', backref="user")
    favorite_planets = db.relationship('Favorite_Planets', backref="user")

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorite_people": [fav_person.serialize() for fav_person in self.favorite_people],
            "favorite_planets": [fav_planets.serialize() for fav_planets in self.favorite_planets]
            # do not serialize the password, its a security breach
        }
    
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    # Python isnt liking this LIne
    favorite_people = db.relationship('Favorite_People', backref="people")

    def __repr__(self):
        return '<People %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "favorite_people": [fav_person.serialize() for fav_person in self.favorite_people],
        }
    
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    favorite_planets = db.relationship('Favorite_Planets', backref='planets')

    def __repr__(self):
        return '<Planets %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "favorite_planets": [fav_planets.serialize() for fav_planets in self.favorite_planets]
            
        }
    

class Favorite_People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    people_id = db.Column(db.Integer, db.ForeignKey(People.id))
    #people = db.relationship('People', backref='favorite_people')

    def __repr__(self):
        return '<Favorite_People %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user.id,
            "people_id": self.people_id,

        }
    
class Favorite_Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    planet_id = db.Column(db.Integer, db.ForeignKey(Planets.id))

    def __repr__(self):
        return '<Favorite_Planets %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
        }