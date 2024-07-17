from flask import Blueprint

# Define Blueprints
blueprints = {
    'home': ['home'],
    'project': ['project', 'projectOne', 'projectTwo', 'projectThree', 'projectFour'],
    'blog': ['blog', 'blogOne', 'blogTwo'],
    'learn': ['learn', 'learnOne'],
    'flaskLessons': [f'flaskLessons_{i}' for i in range(5)],
    'about': ['about'],
    'contact': ['contact'],
    'dashboard': ['dashboard', 'dashboardGithub'],
    'index': ['sitemap', 'robots']
}

# Initialize Blueprints
for key, bp_names in blueprints.items():
    for bp_name in bp_names:
        globals()[f'{bp_name}_bp'] = Blueprint(bp_name, __name__)

# Import Routes
from .home import homeRoutes
from .index import indexmap
from .project import projectRoutes
from .blog import blogRoutes
from .learn import learnRoutes, flaskFrameworkLessons
from .about import aboutRoutes
from .contact import contactRoutes
from .dashboard import dashboardRoutes
from . import errorHandlers
