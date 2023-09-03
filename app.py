from flask import Flask
from flask_cors import CORS
from routes.spotipyroutes import spotify_blueprint
from routes.authroutes import auth_blueprint
from routes.queryroutes import query_blueprint


app = Flask(__name__)
CORS(app)  # enable cors on app

app.register_blueprint(spotify_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(query_blueprint)

if __name__ == "__main__":
    app.run()
