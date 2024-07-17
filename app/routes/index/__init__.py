from flask import Blueprint

sitemap_bp = Blueprint('sitemap', __name__)
robots_bp = Blueprint('robots', __name__)

from . import indexmap
