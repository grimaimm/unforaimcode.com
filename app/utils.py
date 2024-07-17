# ------------------------------------------------------------------------------------------------------------------------------------------------

# Import Library
from flask import render_template, request
from datetime import datetime, timedelta
import requests
import mistune
import os
from firebase_admin import firestore
# ------------------------------------------------------------------------------------------------------------------------------------------------

# Fungsi untuk Mendaftarkan blueprint (modul atau komponen aplikasi) ke aplikasi Flask app.
def register_blueprints(app):
    # Import semua blueprints yang diperlukan
    from .routes.home import home_bp
    from .routes.project import project_bp, projectOne_bp, projectTwo_bp, projectThree_bp, projectFour_bp
    from .routes.blog import blog_bp, blogOne_bp, blogTwo_bp
    from .routes.learn import learn_bp, learnOne_bp, flaskLessons_0_bp, flaskLessons_1_bp, flaskLessons_2_bp, flaskLessons_3_bp, flaskLessons_4_bp
    from .routes.about import about_bp
    from .routes.contact import contact_bp
    from .routes.dashboard import dashboard_bp
    from .routes.index import sitemap_bp, robots_bp

    app.register_blueprint(home_bp, url_prefix='/')
    app.register_blueprint(sitemap_bp, url_prefix='/sitemap.xml')
    app.register_blueprint(robots_bp, url_prefix='/robots.txt')
    app.register_blueprint(project_bp, url_prefix='/projects')
    app.register_blueprint(projectOne_bp, url_prefix='/projects/grimaim-financial-dashboard')
    app.register_blueprint(projectTwo_bp, url_prefix='/projects/unforaim-code-com')
    app.register_blueprint(projectThree_bp, url_prefix='/projects/social-widget')
    app.register_blueprint(projectFour_bp, url_prefix='/projects/chat-room')
    app.register_blueprint(blog_bp, url_prefix='/blog')
    app.register_blueprint(blogOne_bp, url_prefix='/blog/exploring-the-world-of-programming')
    app.register_blueprint(blogTwo_bp, url_prefix='/blog/best-programming-languages-to-learn')
    app.register_blueprint(learn_bp, url_prefix='/learn')
    app.register_blueprint(learnOne_bp, url_prefix='/learn/python-flask-framework')
    app.register_blueprint(about_bp, url_prefix='/about')
    app.register_blueprint(contact_bp, url_prefix='/contact')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

    app.register_blueprint(flaskLessons_0_bp, url_prefix='/learn/python-flask-framework/0-introduction')
    app.register_blueprint(flaskLessons_1_bp, url_prefix='/learn/python-flask-framework/1-install-flask')
    app.register_blueprint(flaskLessons_2_bp, url_prefix='/learn/python-flask-framework/2-your-first-flask-application')
    app.register_blueprint(flaskLessons_3_bp, url_prefix='/learn/python-flask-framework/3-routing-and-views')
    app.register_blueprint(flaskLessons_4_bp, url_prefix='/learn/python-flask-framework/4-templates')

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Fungsi untuk Mendaftarkan penanganan kesalahan (error handlers) ke aplikasi Flask app untuk menangani berbagai jenis error (misalnya, 404, 500).
def register_error_handlers(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Fungsi untuk Meningkatkan (menambah) jumlah tampilan (views) pada referensi blog tertentu 'blog_ref'.
def increase_views(blog_ref):
    blog_data = blog_ref.get().to_dict()
    views_count = blog_data.get('views', 0) + 1
    blog_ref.update({'views': views_count})
    return views_count, blog_data

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Fungsi untuk Mengambil (fetch) konten blog dari koleksi collection_name berdasarkan referensi blog 'blog_ref'.
def fetch_blog_content(blog_ref, collection_name):
    blogs = blog_ref.collection(collection_name).stream()
    blog_contents = []

    for blog in blogs:
        blog_dict = blog.to_dict()
        blog_dict["number"] = int(blog.id.split(".")[0].strip())

        for item in blog_dict.get("list", []):
            if "code" in item:
                item["html_content"] = convert_to_markdown(item["code"])

        blog_contents.append(blog_dict)

    return sorted(blog_contents, key=lambda x: x["number"])

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Fungsi untuk Mengambil (fetch) konten project dari koleksi collection_name berdasarkan referensi blog 'project_ref'.
def fetch_projects_content(project_ref, collection_name):
    projects = project_ref.collection(collection_name).stream()
    project_contents = []

    for project in projects:
        project_dict = project.to_dict()
        project_id_parts = project.id.split(".")

        if project_id_parts and project_id_parts[0].strip().isdigit():
            project_dict["number"] = int(project_id_parts[0].strip())
        else:
            continue

        # Proses untuk 'listStep'
        for item in project_dict.get("listStep", []):
            if "listCode" in item:
                item["html_content"] = convert_to_markdown(item["listCode"])

        # Proses untuk 'stepByStep'
        for step in project_dict.get("listStep", []):
            if isinstance(step, dict):
                for item in step.get("stepByStep", []):
                    if "code" in item:
                        item["html_content"] = convert_to_markdown(item["code"])

        project_contents.append(project_dict)

    return sorted(project_contents, key=lambda x: x["number"])

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Fungsi untuk Convert Markdown to HTML Route collection Learn
def convert_markdown_to_html(content):
    for step in content:
        if isinstance(step, dict):
            for item in step.get("listDesc", []):
                if isinstance(item, dict) and "descValue" in item:
                    item["html_content"] = convert_to_markdown(item["descValue"])
    return content
# ------------------------------------------------------------------------------------------------------------------------------------------------

# Fungsi untuk Convert Markdown All Collection
def convert_to_markdown(markdown_file_name):
    try:
        with open(f"app/static/assets/markdown-code/{markdown_file_name}", "r") as f:
            return mistune.markdown(f.read())
    except FileNotFoundError:
        return "<p>Markdown file not found</p>"
    except Exception as e:
        return f"<p>Error reading markdown file: {str(e)}</p>"

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Fungsi untuk mendapatkan kontribusi menggunakan GitHub REST API
def get_contributions_from_github():
    username = os.getenv("GITHUB_USERNAME")
    access_token = os.getenv("GITHUB_ACCESS_TOKEN")
    url = f'https://api.github.com/users/{username}/events'
    headers = {'Authorization': f'token {access_token}'}

    try:
        # Ambil semua event kontribusi dari GitHub
        events = []
        while url:
            response = requests.get(url, headers=headers)
            events.extend(response.json())
            url = response.links.get('next', {}).get('url')

        total_contributions = len(events)
        best_day = find_best_day(events)
        average_per_day = total_contributions / len(events) if events else 0

        # Ambil informasi repositori dari GitHub (hanya repositori publik)
        repo_url = "https://api.github.com/user/repos?type=public"
        repo_response = requests.get(repo_url, headers=headers)
        repositories = repo_response.json()

        total_repositories = len(repositories)

        return {
            'total_contributions': total_contributions,
            'best_day': best_day,
            'average_per_day': "{:.0f}".format(average_per_day),
            'total_repositories': total_repositories
        }
    
    except requests.RequestException as e:
        print(f'Error fetching contributions from GitHub: {e}')
        return {}

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Fungsi untuk mendapatkan total kontribusi dalam setahun terakhir menggunakan GitHub GraphQL API
def get_github_contributions():
    username = os.getenv("GITHUB_USERNAME")
    access_token = os.getenv("GITHUB_ACCESS_TOKEN")
    url = 'https://api.github.com/graphql'
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Menghitung tanggal setahun yang lalu dari sekarang
    from_date = (datetime.utcnow() - timedelta(days=365)).isoformat()

    query = """
    query {
        user(login: "%s") {
            contributionsCollection(from: "%s") {
                contributionCalendar {
                    totalContributions
                    weeks {
                        contributionDays {
                            contributionCount
                            date
                        }
                    }
                }
            }
        }
    }
    """ % (username, from_date)

    response = requests.post(url, json={'query': query}, headers=headers)
    data = response.json()

    contributions_last_year = data['data']['user']['contributionsCollection']['contributionCalendar']['totalContributions']
    weekly_contributions = {}

    for week in data['data']['user']['contributionsCollection']['contributionCalendar']['weeks']:
        for day in week['contributionDays']:
            date = datetime.strptime(day['date'], "%Y-%m-%d").strftime("%B %Y")
            weekly_contributions[date] = weekly_contributions.get(date, 0) + day['contributionCount']

    return contributions_last_year, weekly_contributions

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Fungsi untuk mendapatkan hari terbaik dalam kontribusi menggunakan GitHub REST API
def find_best_day(events):
    from collections import Counter

    contributions_per_day = Counter(event['created_at'][:10] for event in events)

    if not contributions_per_day:
        return None

    best_day = contributions_per_day.most_common(1)[0][1]
    return best_day

# ------------------------------------------------------------------------------------------------------------------------------------------------

def add_cache_header_fonts(response):
    # Jika file adalah di static/ atau subfoldernya, tambahkan cache header
    if 'static/fonts/' in request.path:
        response.cache_control.max_age = 31536000  # Cache selama 1 tahun
        response.cache_control.public = True
        response.cache_control.no_cache = None  # Menghapus no-cache
    return response

def add_cache_header_admin(response):
    # Jika file adalah gambar di static/images/admin, tambahkan cache header
    if 'static/images/admin/' in request.path:
        response.cache_control.max_age = 31536000  # Cache selama 1 tahun
        response.cache_control.public = True
        response.cache_control.no_cache = None  # Menghapus no-cache
    return response


def add_cache_header_skills(response):
    # Jika file adalah gambar di static/images/skills, tambahkan cache header
    if 'static/images/skills/' in request.path:
        response.cache_control.max_age = 31536000  # Cache selama 1 tahun
        response.cache_control.public = True
        response.cache_control.no_cache = None  # Menghapus no-cache
    return response


def add_cache_header_assets(response):
    # Jika file adalah gambar di static/images/skills, tambahkan cache header
    if 'static/assets/' in request.path:
        response.cache_control.max_age = 31536000  # Cache selama 1 tahun
        response.cache_control.public = True
        response.cache_control.no_cache = None  # Menghapus no-cache
    return response


def add_cache_header_highlight(response):
    # Jika file adalah gambar di static/images/skills, tambahkan cache header
    if 'static/modules/highlight' in request.path:
        response.cache_control.max_age = 31536000  # Cache selama 1 tahun
        response.cache_control.public = True
        response.cache_control.no_cache = None  # Menghapus no-cache
    return response


def add_cache_header_pagespeed(response):
    # Jika file adalah gambar di static/images/skills, tambahkan cache header
    if 'static/modules/page-speed' in request.path:
        response.cache_control.max_age = 31536000  # Cache selama 1 tahun
        response.cache_control.public = True
        response.cache_control.no_cache = None  # Menghapus no-cache
    return response

def add_cache_header(response, path_prefix):
    # Jika file berada di dalam path_prefix, tambahkan cache header
    if path_prefix in request.path:
        response.cache_control.max_age = 86400  # Cache selama 1 tahun
        response.cache_control.public = True
        response.cache_control.no_cache = None  # Menghapus no-cache
    return response


def log_page_access(page_name):
    db = firestore.client()
    page_ref = db.collection("pageAccess").document(page_name)
    page = page_ref.get()
    
    if page.exists:
        access_count = page.to_dict().get('accessCount', 0) + 1
        page_ref.update({'accessCount': access_count})
    else:
        page_ref.set({'accessCount': 1})