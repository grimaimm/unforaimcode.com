from flask import Blueprint

# Define Blueprints
blueprints = {
    'learn': ['learn', 'learnOne'],
    'flaskLessons': [f'flaskLessons_{i}' for i in range(5)]
}

# Initialize Blueprints
for key, bp_names in blueprints.items():
    for idx, bp_name in enumerate(bp_names):
        globals()[f'{bp_name}_bp'] = Blueprint(f'{key}_{idx}', __name__)

# Import Routes
from . import flaskFrameworkLessons, learnRoutes
