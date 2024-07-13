# ------------------------------------------------------------------------------------------------------------------------------------------------

# Import Library
from flask import Flask
from flask_compress import Compress
from flask_caching import Cache
from flask_minify import minify
from flask_mail import Mail
from flaskext.markdown import Markdown
import os
import secrets
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, initialize_app
from instance.config import config

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Inisialisasi ekstensi Flask
compress = Compress()
cache = Cache()
mail = Mail()

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Fungsi untuk membuat dan mengkonfigurasi objek aplikasi Flask
def create_app(config_name='default'):
    app = Flask(__name__, instance_relative_config=True)
    
    # Load environment variables from .env file
    load_dotenv()

    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.py', silent=True)
    app.config['SECRET_KEY'] = secrets.token_hex(16)
    app.config['CACHE_DEFAULT_TIMEOUT'] = 86400

    # Inisialisasi Flask-Compress
    compress.init_app(app)

    # Inisialisasi Flask-Caching
    cache.init_app(app)

    # Inisialisasi Flask-Minify
    minify(app=app, html=True, js=True, cssless=True, static=True) 

    # Inisialisasi Flask-Mail
    app.config.update(
        MAIL_SERVER=os.getenv('MAIL_SERVER'),
        MAIL_PORT=int(os.getenv('MAIL_PORT', 587)),
        MAIL_USE_TLS=os.getenv('MAIL_USE_TLS', 'false').lower() == 'true',
        MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
        MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
    )
    mail.init_app(app)

    # Inisialisasi Markdown
    Markdown(app)

    # Inisialisasi Firebase Admin SDK
    firebase_credentials = os.path.join(os.path.dirname(__file__), '..', 'instance', 'serviceAccountKey.json')
    # firebase_credentials = os.getenv('FIREBASE_CREDENTIALS')
    if firebase_credentials:
        cred = credentials.Certificate(firebase_credentials)
        firebase_admin.initialize_app(cred)
        

    # Registrasi blueprints dan error handlers setelah inisialisasi Firebase
    from .utils import register_blueprints, register_error_handlers
    register_blueprints(app)
    register_error_handlers(app)

    @app.after_request
    def after_request(response):
        from .utils import add_cache_header  # Mengimpor fungsi add_cache_header di sini

        # Memanggil add_cache_header untuk setiap path yang perlu di-cache
        response = add_cache_header(response, 'static/')
        # response = add_cache_header(response, 'static/assets/markdown-code/')
        # response = add_cache_header(response, 'static/css/')
        # response = add_cache_header(response, 'static/fonts/')
        # response = add_cache_header(response, 'static/js/')
        # response = add_cache_header(response, 'static/images/')
        # response = add_cache_header(response, 'static/modules/')
        # response = add_cache_header(response, 'static/modules/highlight/')
        # response = add_cache_header(response, 'static/modules/page-speed/')
        # response = add_cache_header(response, 'static/modules/flowbite/')
        # response = add_cache_header(response, 'static/modules/animation-infinity/')
        # response = add_cache_header(response, 'static/modules/typed/index.js')
        # response = add_cache_header(response, 'static/modules/chart/')
        # response = add_cache_header(response, 'static/modules/alpine/')

        return response

    return app

# ------------------------------------------------------------------------------------------------------------------------------------------------
