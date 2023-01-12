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

@app.route('/')
def index():
    # return '<h1>Hello!</h1><img src="http://helloflask.com/totoro.gif">'
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)

@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % name

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name='Vivian'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', num=2))
    return 'Test Page'



if __name__ == '__main__':
    app.run()