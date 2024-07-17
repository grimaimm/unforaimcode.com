from . import sitemap_bp, robots_bp
from flask import send_from_directory

@sitemap_bp.route('/')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')
  
@robots_bp.route('/')
def robots():
    return send_from_directory('static', 'robots.txt')