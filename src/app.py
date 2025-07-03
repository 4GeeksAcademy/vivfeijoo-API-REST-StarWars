import os
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from flask_admin import Admin
from src.models import db, User, People, Planet, Favorite
from src.admin import setup_admin
from src.utils import generate_sitemap

app = Flask(__name__)
app.url_map.strict_slashes = False

# Configuración del secret key y admin
app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
setup_admin(app)

# Configuración de la base de datos
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar DB, migraciones, CORS
db.init_app(app)
Migrate(app, db)
CORS(app)

# Sitemap
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Rutas GET básicas para probar tus modelos

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    return jsonify([p.serialize() for p in people]), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

@app.route('/favorites', methods=['GET'])
def get_favorites():
    favorites = Favorite.query.all()
    return jsonify([fav.serialize() for fav in favorites]), 200

# Para desarrollo local
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
