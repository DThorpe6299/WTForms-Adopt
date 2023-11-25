from flask import Flask, render_template, redirect, flash, url_for
from flask_debugtoolbar import DebugToolbarExtension
from model import db, connect_db, Pet, PetForm, EditPetForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adoption_agency'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = 'adoption-agency-key'
debug = DebugToolbarExtension(app)


@app.before_first_request
def create_tables():
    """Create all tables."""
    db.create_all()

@app.route('/')
def homepage():
    pet_data = db.session.query(Pet.pet_name, Pet.photo_url, Pet.available).all()

    return render_template('homepage.html', pets=pet_data)

@app.route('/add', methods=["GET", "POST"])
def add_pet():
    """Add a pet form; handle adding."""

    form = PetForm()
    if form.validate_on_submit():
        pet_name=form.pet_name.data
        species=form.species.data
        photo_url=form.photo_url.data
        age=form.age.data
        notes=form.notes.data
        flash(f"Added {pet_name}, {species}, {photo_url}, {age} and {notes}.")
        return redirect(url_for('homepage'))
    else:
        return render_template("add_pet_form.html", form=form)

@app.route('/<int:pet_id>/edit', methods=["GET", "POST"])
def edit_form(pet_id):
    """Show a form that allows us to edit this pet: Photo URL, Notes, Available."""

    pet= Pet.query.get_or_404(pet_id)
    form=EditPetForm(obj=pet)
    
    if form.validate_on_submit():
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data
        db.session.commit()
        flash(f"{pet.name} updated.")
        return redirect(url_for('homepage'))
    else:
        return render_template('edit_petform.html', form=form, pet=pet)
    