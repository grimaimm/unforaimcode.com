# ------------------------------------------------------------------------------------------------------------------------------------------------

# Import Library and Function
from . import learn_bp, learnOne_bp
from flask import make_response, render_template
from firebase_admin import firestore  # Import firestore
from app import cache
from ...utils import log_page_access

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Get a Firestore client
db = firestore.client()

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Route Learns
@learn_bp.route('/')
def learn():
    # Log page access
    log_page_access('learn')

    # Cache di server selama 1 hari
    @cache.cached(timeout=86400, key_prefix='learn_page')
    def cached_learn():
        learns_collection = db.collection("Learns")
        learns = learns_collection.stream()
        learn_list = [learn.to_dict() for learn in learns]
        response = make_response(render_template('learn-page/learn.html', learns=learn_list))
        response.headers['Cache-Control'] = 'public, max-age=86400'  # Cache di browser selama 1 hari
        return response

    return cached_learn()

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Clear Cache Learn Page
@learn_bp.route('/clear_cache')
def clear_cache():
    if cache.get('learn_page'):
        cache.delete('learn_page')
        return "Cache for learn page cleared!"
    else:
        return "Cache for learn page does not exist!"

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Route Learns One "1. Python Flask Framework"
@learnOne_bp.route('/')
@cache.cached(timeout=86400, key_prefix='pythonFlask_page')
def pythonFlaskFramework():
    learn_ref = db.collection('Learns').document('1. Python Flask Framework')
    learn_data = learn_ref.get().to_dict()
    doc = learn_ref.get()
    lessons = []
    if doc.exists:
        data = doc.to_dict()
        if 'totalLessons' in data:
            total_lessons_map = data['totalLessons']
            sorted_lessons = sorted(total_lessons_map.items(), key=lambda x: int(x[0].split('_')[1]))
            # Iterasi semua lessons dan tambahkan ke dalam list
            for key, value in sorted_lessons:
                lesson_info = {
                    'title': value['title'].title(),
                    'routes': value['routes'].lower()
                }
                lessons.append(lesson_info)

    return render_template('learn-page/python-flask-framework/index.html', learn_data=learn_data, lessons=lessons)