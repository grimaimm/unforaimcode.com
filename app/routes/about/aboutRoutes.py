# ------------------------------------------------------------------------------------------------------------------------------------------------

# Import Library and Function
from . import about_bp
from flask import make_response, render_template
from firebase_admin import firestore  # Import firestore
from app import cache
from ...utils import log_page_access

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Get a Firestore client
db = firestore.client()

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Route About
@about_bp.route('/')
def about():
    log_page_access('about')

    @cache.cached(timeout=86400, key_prefix='about_page')
    def cached_about():
        about_ref = db.collection('Abouts').document('contentAbout')
        about_data = about_ref.get().to_dict()
        response = make_response(render_template('about-page/about.html', abouts=about_data))
        response.headers['Cache-Control'] = 'public, max-age=86400'  # Cache di browser selama 1 hari
        return response

    return cached_about()

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Clear Cache About Page
@about_bp.route('/clear_cache')
def clear_cache():
    if cache.get('about_page'):
        cache.delete('about_page')
        return "Cache for about page cleared!"
    else:
        return "Cache for about page does not exist!"

# ------------------------------------------------------------------------------------------------------------------------------------------------