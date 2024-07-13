# ------------------------------------------------------------------------------------------------------------------------------------------------

# Import Library
from . import blog_bp, blogOne_bp, blogTwo_bp
from ...utils import increase_views, fetch_blog_content
from flask import make_response, render_template
from firebase_admin import firestore
from app import cache
from ...utils import log_page_access

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Get a Firestore client
db = firestore.client()

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Route Blog
@blog_bp.route('/')
def blog():
    # Log page access
    log_page_access('blog')
    
    blogs_collection = db.collection("Blogs")
    blogs = blogs_collection.stream()
    blog_list = [blog.to_dict() for blog in blogs]
    sorted_blogs = sorted(blog_list, key=lambda x: x['published'], reverse=True)
    return render_template('blog-page/blog.html', blogs=sorted_blogs)

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Clear Cache Project Page
@blog_bp.route('/clear_cache')
def clear_cache():
    if cache.get('blog_page'):
        cache.delete('blog_page')
        return "Cache for blog page cleared!"
    else:
        return "Cache for blog page does not exist!"

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Route Blog One '1. Exploring the World of Programming'
@blogOne_bp.route('/')
# @cache.cached(timeout=86400, key_prefix='blogOne_page')
def blogOne():
    blog_ref = db.collection('Blogs').document('1. Exploring the World of Programming')
    views_count, blog_data = increase_views(blog_ref) # Meningkatkan jumlah views
    sorted_blogs = fetch_blog_content(blog_ref, 'contentBlogOne') # Mengambil konten blog
    return render_template('blog-page/blogOne.html', blog_data=blog_data, views=views_count, blogs=sorted_blogs)
    # response = make_response(render_template('blog-page/blogOne.html', blog_data=blog_data, views=views_count, blogs=sorted_blogs))
    # response.headers['Cache-Control'] = 'public, max-age=86400'  # Cache di browser selama 1 hari
    # return response

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Route Blog One '2. Best Programming Languages to Learn'
@blogTwo_bp.route('/')
# @cache.cached(timeout=86400, key_prefix='blogTwo_page')
def blogTwo():
    blog_ref = db.collection('Blogs').document('2. Best Programming Languages to Learn')
    views_count, blog_data = increase_views(blog_ref) # Meningkatkan jumlah views
    sorted_blogs = fetch_blog_content(blog_ref, 'contentBlogTwo') # Mengambil konten blog
    return render_template('blog-page/blogTwo.html', blog_data=blog_data, views=views_count, blogs=sorted_blogs)
    # response = make_response(render_template('blog-page/blogTwo.html', blog_data=blog_data, views=views_count, blogs=sorted_blogs))
    # response.headers['Cache-Control'] = 'public, max-age=86400'  # Cache di browser selama 1 hari
    # return response

# ------------------------------------------------------------------------------------------------------------------------------------------------

