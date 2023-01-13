from flask import Flask, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import sys
import click

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __repr__(self):
        return '<User %r>' % self.id

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    name = 'Vivian Lu'
    movies = [
        {'title': 'Fantastic Beasts and Where to Find Them', 'year': '2016'},
        {'title': 'Crazy Rich Asians', 'year': '2018'},
        {'title': 'Captain Marvel', 'year': '2019'},
        {'title': 'Gemini Man', 'year': '2020'},
        {'title': 'Spider-Man: No Way Home', 'year': '2021'},
        {'title': 'Shang-Chi and the Legend of the Ten Rings', 'year': '2021'},
        {'title': 'Venom: Let There Be Carnage', 'year': '2021'},
        {'title': 'Eternals', 'year': '2021'},
        {'title': 'Avatar: The Way of Water', 'year': '2022'},
        {'title': 'Doctor Strange in the Multiverse of Madness', 'year': '2022'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)



if __name__ == '__main__':
    app.run()