from flask import Flask, jsonify, render_template, request
from routes.moviesRoute import movies_bp
import requests

app = Flask(__name__)
app.register_blueprint(movies_bp)

@app.route('/', methods=['GET', 'POST'])
def index():
    filter = request.form.get('dropdown')
    param = request.form.get('filter')
    genre = request.form.get('genre')
    response = []

    if filter == "Title":
        response = requests.get('http://127.0.0.1:5000/movies', params={'title': param})
    elif filter == "Year and genre":
        response = requests.get('http://127.0.0.1:5000/movies', params={'year': param, 'genres': genre})
    elif filter == "Top K rated":
        response = requests.get('http://127.0.0.1:5000/movies', params={'top': param})

    return render_template('index.html', movies=response.json())

if __name__ == '__main__':
    app.run()