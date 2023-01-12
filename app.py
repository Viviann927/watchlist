from flask import Flask, url_for, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # return '<h1>Hello!</h1><img src="http://helloflask.com/totoro.gif">'
    return render_template('index.html', name=name, movies=movies)

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

if __name__ == '__main__':
    app.run()