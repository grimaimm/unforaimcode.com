from flask import Blueprint

# Define Blueprints
blueprints = ['blog', 'blogOne', 'blogTwo']

# Initialize Blueprints
for bp_name in blueprints:
    globals()[f'{bp_name}_bp'] = Blueprint(bp_name, __name__)

# Import Routes
from . import blogRoutes