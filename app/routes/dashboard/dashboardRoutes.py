# ------------------------------------------------------------------------------------------------------------------------------------------------

# Import Library
from . import dashboard_bp
from flask import make_response, render_template, session, request, jsonify
from firebase_admin import firestore  # Import firestore
from ...utils import get_contributions_from_github, get_github_contributions
from app import cache
from ...utils import log_page_access

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Get a Firestore client
db = firestore.client()

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Route Dashboard
@dashboard_bp.route('/')
def dashboard():
    log_page_access('dashboard')

    @cache.cached(timeout=86400, key_prefix='dashboard_page')
    def cached_dashboard():
        # Ambil data dari Firestore
        dashboard_collection = db.collection("Dashboard")
        dashboards = dashboard_collection.stream()

        # Membuat list untuk menampung dashboard yang diambil
        dashboard_list = []

        for dashboard in dashboards:
            data = dashboard.to_dict()
            # Menghapus nomor di depan ID dokumen
            page = dashboard.id.split('. ', 1)[1]
            dashboard_list.append({'id': page, 'contents': data['contents']})

        # Ambil active_tab dari URL parameter atau default ke 'home'
        active_tab = request.args.get('tab', 'home')
        session['active_tab'] = active_tab

        contributions = get_contributions_from_github()
        contributions_last_year, weekly_contributions = get_github_contributions()

        response = make_response(render_template('dashboard-page/dashboard.html', 
                                dashboards=dashboard_list, 
                                active_tab=active_tab, 
                                contributions=contributions,
                                contributions_last_year=contributions_last_year, 
                                weekly_contributions=weekly_contributions))
        response.headers['Cache-Control'] = 'public, max-age=86400'  # Cache di browser selama 1 hari
        return response

    return cached_dashboard()

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Clear Cache Dashboard Page
@dashboard_bp.route('/clear_cache')
def clear_cache():
    if cache.get('dashboard_page'):
        cache.delete('dashboard_page')
        return "Cache for dashboard page cleared!"
    else:
        return "Cache for dashboard page does not exist!"

# ------------------------------------------------------------------------------------------------------------------------------------------------

