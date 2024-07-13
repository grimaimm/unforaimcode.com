# ------------------------------------------------------------------------------------------------------------------------------------------------

# Import Library and Function
from . import home_bp
from flask import make_response, render_template
from firebase_admin import firestore  # Import firestore
from app import cache
from ...utils import log_page_access

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Get a Firestore client
db = firestore.client()

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Route Home
@home_bp.route('/')
def home():
    # Log page access
    # log_page_access('home')
    
    # Cache di server selama 1 hari
    # @cache.cached(timeout=86400, key_prefix='home_page')
    def cached_home():
        blog_list = [blog.to_dict() for blog in db.collection("Blogs").stream()]
        service_list = [service.to_dict() for service in db.collection("Services").stream()]
        skill_list = [skill.to_dict() for skill in db.collection("Skills").stream()]
        
        # return render_template('home-page/index.html', blogs=blog_list, services=service_list, skills=skill_list)

        response = make_response(render_template('home-page/index.html', blogs=blog_list, services=service_list, skills=skill_list))
        response.headers['Cache-Control'] = 'public, max-age=86400'  # Cache di browser selama 1 hari
        return response

    return cached_home()

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Clear Cache Home Page
@home_bp.route('/clear_cache')
def clear_cache():
    if cache.get('home_page'):
        cache.delete('home_page')
        return "Cache for home page cleared!"
    else:
        return "Cache for home page does not exist!"

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Clear Cache All Page
@home_bp.route('/clear_all_cache')
def clear_all_cache():
    cache.clear()
    return "All cache cleared!"

# ------------------------------------------------------------------------------------------------------------------------------------------------
