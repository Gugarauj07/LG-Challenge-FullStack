from flask import Flask, jsonify, render_template
from routes.moviesRoute import movies_bp

app = Flask(__name__)
app.register_blueprint(movies_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()