"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask_jwt_extended import JWTManager  # Importa JWTManager
import os
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_migrate import Migrate
from flask_cors import CORS
from flask_swagger import swagger
from api.utils import APIException, generate_sitemap
from api.models import db, User
from api.routes import api
from api.admin import setup_admin
from api.commands import setup_commands


# from models import Person
def create_app():
    app = Flask(__name__)  # Usa la función create_app para crear la aplicación
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # Configura la URI de la base de datos
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configuración de la clave secreta para JWT
    app.config['JWT_SECRET_KEY'] = 'tu_clave_secreta'  # Usa una clave secreta segura
    jwt = JWTManager(app)  # Inicializa JWTManager con la aplicación

    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)

    ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
    static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../public/')
    app.url_map.strict_slashes = False
    # database configuration

    # add the admin
    setup_admin(app)

    # add the commands
    setup_commands(app)

    # Add all endpoints form the API with a "api" prefix
    app.register_blueprint(api, url_prefix='/api')

    # Handle/serialize errors like a JSON object
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': User}

    @app.errorhandler(APIException)
    def handle_invalid_usage(error):
        return jsonify(error.to_dict()), error.status_code

    # generate sitemap with all your endpoints
    @app.route('/')
    def sitemap():
        if ENV == "development":
            return generate_sitemap(app)
        return send_from_directory(static_file_dir, 'index.html')

    # any other endpoint will try to serve it like a static file
    @app.route('/<path:path>', methods=['GET'])
    def serve_any_other_file(path):
        if not os.path.isfile(os.path.join(static_file_dir, path)):
            path = 'index.html'
        response = send_from_directory(static_file_dir, path)
        response.cache_control.max_age = 0  # avoid cache memory
        return response

    return app

if __name__ == '__main__':
    app = create_app()
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)
