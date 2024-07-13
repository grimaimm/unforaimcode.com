# ------------------------------------------------------------------------------------------------------------------------------------------------

# Import Library and Function
from . import project_bp, projectOne_bp, projectTwo_bp, projectThree_bp, projectFour_bp
from ...utils import fetch_projects_content
from flask import make_response, render_template
from firebase_admin import firestore  # Import firestore
from app import cache
from ...utils import log_page_access

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Get a Firestore client
db = firestore.client()

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Route Project
@project_bp.route('/')
def project():
    # Log page access
    # log_page_access('projects')
    
    # Cache di server selama 1 hari
    @cache.cached(timeout=86400, key_prefix='project_page')
    def cached_project():
        projects_collection = db.collection("Projects")
        projects = projects_collection.stream()
        project_list = [project.to_dict() for project in projects]
        sorted_projects = sorted(project_list, key=lambda x: x['id'], reverse=True)
        # return render_template('project-page/project.html', projects=sorted_projects)
        response = make_response(render_template('project-page/project.html', projects=sorted_projects))
        response.headers['Cache-Control'] = 'public, max-age=86400'  # Cache di browser selama 1 hari
        return response

    return cached_project()

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Clear Cache Project Page
@project_bp.route('/clear_cache')
def clear_cache():
    if cache.get('project_page'):
        cache.delete('project_page')
        return "Cache for project page cleared!"
    else:
        return "Cache for project page does not exist!"

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Route Project One "1. Grimaim Financial Dashboard"
@projectOne_bp.route('/')
@cache.cached(timeout=86400, key_prefix='projectOne_page')
def projectOne():
    project_ref = db.collection('Projects').document('1. Grimaim Financial Dashboard')
    project_data = project_ref.get().to_dict()
    sorted_projects = fetch_projects_content(project_ref, 'contentProjectOne')
    response = make_response(render_template('project-page/projectOne.html', project_data=project_data, project_contents_data=sorted_projects))
    response.headers['Cache-Control'] = 'public, max-age=86400'  # Cache di browser selama 1 hari
    return response

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Route Project Two "2. unforaimcode.com"
@projectTwo_bp.route('/')
@cache.cached(timeout=86400, key_prefix='projectTwo_page')
def projectTwo():
    project_ref = db.collection('Projects').document('2. unforaimcode.com')
    project_data = project_ref.get().to_dict()
    sorted_projects = fetch_projects_content(project_ref, 'contentProjectTwo')
    response = make_response(render_template('project-page/projectTwo.html', project_data=project_data, project_contents_data=sorted_projects))
    response.headers['Cache-Control'] = 'public, max-age=86400'  # Cache di browser selama 1 hari
    return response

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Route Project Three "3. Social Widget"
@projectThree_bp.route('/')
@cache.cached(timeout=86400, key_prefix='projectThree_page')
def projectThree():
    project_ref = db.collection('Projects').document('3. Social Widget')
    project_data = project_ref.get().to_dict()
    sorted_projects = fetch_projects_content(project_ref, 'contentProjectThree')
    response = make_response(render_template('project-page/projectThree.html', project_data=project_data, project_contents_data=sorted_projects))
    response.headers['Cache-Control'] = 'public, max-age=86400'  # Cache di browser selama 1 hari
    return response

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Route Project Four "4. Chat Room"
@projectFour_bp.route('/')
@cache.cached(timeout=86400, key_prefix='projectFour_page')
def projectFour():
    project_ref = db.collection('Projects').document('4. Chat Room')
    project_data = project_ref.get().to_dict()
    sorted_projects = fetch_projects_content(project_ref, 'contentProjectFour')
    response = make_response(render_template('project-page/projectFour.html', project_data=project_data, project_contents_data=sorted_projects))
    response.headers['Cache-Control'] = 'public, max-age=86400'  # Cache di browser selama 1 hari
    return response

# ------------------------------------------------------------------------------------------------------------------------------------------------