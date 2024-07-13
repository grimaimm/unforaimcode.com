from flask import Blueprint

# Define Blueprints
blueprints = ['project', 'projectOne', 'projectTwo', 'projectThree', 'projectFour']

# Initialize Blueprints
for idx, bp_name in enumerate(blueprints):
    globals()[f'{bp_name}_bp'] = Blueprint(f'{bp_name}', __name__)

# Import Routes
from . import projectRoutes
