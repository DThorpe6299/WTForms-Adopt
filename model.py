from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Optional, NumberRange, URL, Length

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)

class Pet(db.Model):
    """This models a pet potentially available for adoption."""

    __tablename__ = "pets"

    id = db.Column(db.Integer,
                    primary_key= True,
                     autoincrement = True)
    name = db.Column(db.String(50), nullable=False)
    species  = db.Column(db.String(50), nullable=False)
    photo_url = db.Column(db.String(255), default='deafault_photo.jpg')
    age = db.Column(db.Integer)
    notes = db.Column(db.String(200))
    available = db.Column(db.Boolean, default=True)

class PetForm(FlaskForm):
    """Form for adding a pet."""

    pet_name = StringField("Pet name", validators=[InputRequired()])
    species = SelectField(
        "Species",
        choices=[("cat", "Cat"), ("dog", "Dog"), ("porcupine", "Porcupine")],
    )
    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    age = IntegerField("Age", validators=[NumberRange(min=0, max=30), Optional()])
    notes = StringField("Notes")

class EditPetForm(FlaskForm):
    """Form for editing an existing pet."""

    photo_url = StringField(
        "Photo URL",
        validators=[Optional(), URL()],
    )
    notes = TextAreaField(
        "Comments",
        validators=[Optional(), Length(min=10)],
    )
    available = BooleanField("Available?")