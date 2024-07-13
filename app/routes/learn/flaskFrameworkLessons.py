# ------------------------------------------------------------------------------------------------------------------------------------------------

# Import Library and Function
from . import (
    flaskLessons_0_bp, 
    flaskLessons_1_bp,
    flaskLessons_2_bp,
    flaskLessons_3_bp,
    flaskLessons_4_bp
)
from ...utils import convert_markdown_to_html
from flask import make_response, render_template
from firebase_admin import firestore  # Import firestore
import mistune, os
from app import cache

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Get a Firestore client
db = firestore.client()

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Route Learns = Flask Framework Lessons 0 - Introduction
@flaskLessons_0_bp.route('/')
@cache.cached(timeout=86400, key_prefix='flaskLessons0_page')
def lessons0():
    # Mendapatkan dokumen spesifik dari koleksi 'Learns'
    learn_ref = db.collection('Learns').document('1. Python Flask Framework')
    learn_contents_ref = learn_ref.collection('lessons').document('0. Introduction')
    lesson_data = learn_contents_ref.get().to_dict()  # Mengambil data dari dokumen
    response = make_response(render_template('learn-page/python-flask-framework/py-lessons-0.html', lesson_data=lesson_data))
    response.headers['Cache-Control'] = 'public, max-age=86400'  # Cache di browser selama 1 hari
    return response

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Route Learns = Flask Framework Lessons 1 - Install Flask
@flaskLessons_1_bp.route('/')
@cache.cached(timeout=86400, key_prefix='flaskLessons1_page')
def lessons1():
    learn_ref = db.collection('Learns').document('1. Python Flask Framework')
    learn_contents_ref = learn_ref.collection('lessons').document('1. Install Flask')
    lesson_data = learn_contents_ref.get().to_dict()  # Mengambil data dari dokumen
    if lesson_data:
        lesson_data["content"] = convert_markdown_to_html(lesson_data.get("content", [])) # Mengonversi konten markdown menjadi HTML
    response = make_response(render_template('learn-page/python-flask-framework/py-lessons-1.html', lesson_data=lesson_data))
    response.headers['Cache-Control'] = 'public, max-age=86400'  # Cache di browser selama 1 hari
    return response

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Route Learns = Flask Framework Lessons 2 - Your First Flask Application
@flaskLessons_2_bp.route('/')
@cache.cached(timeout=86400, key_prefix='flaskLessons2_page')
def lessons2():
    learn_ref = db.collection('Learns').document('1. Python Flask Framework')
    learn_contents_ref = learn_ref.collection('lessons').document('2. Your First Flask Application')
    lesson_data = learn_contents_ref.get().to_dict() # Mengambil data dari dokumen
    if lesson_data:
        lesson_data["content"] = convert_markdown_to_html(lesson_data.get("content", []))
    response = make_response(render_template('learn-page/python-flask-framework/py-lessons-2.html', lesson_data=lesson_data))
    response.headers['Cache-Control'] = 'public, max-age=86400'  # Cache di browser selama 1 hari
    return response

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Route Learns = Flask Framework Lessons 3 - Routing and Views
@flaskLessons_3_bp.route('/')
@cache.cached(timeout=86400, key_prefix='flaskLessons3_page')
def lessons3():
    learn_ref = db.collection('Learns').document('1. Python Flask Framework')
    learn_contents_ref = learn_ref.collection('lessons').document('3. Routing and Views')
    lesson_data = learn_contents_ref.get().to_dict() # Mengambil data dari dokumen
    if lesson_data:
        lesson_data["content"] = convert_markdown_to_html(lesson_data.get("content", []))
    response = make_response(render_template('learn-page/python-flask-framework/py-lessons-3.html', lesson_data=lesson_data))
    response.headers['Cache-Control'] = 'public, max-age=86400'  # Cache di browser selama 1 hari
    return response

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Route Learns = Flask Framework Lessons 4 - Templates
@flaskLessons_4_bp.route('/')
@cache.cached(timeout=86400, key_prefix='flaskLessons4_page')
def lessons4():
    learn_ref = db.collection('Learns').document('1. Python Flask Framework')
    learn_contents_ref = learn_ref.collection('lessons').document('4. Templates')
    lesson_data = learn_contents_ref.get().to_dict() # Mengambil data dari dokumen
    if lesson_data:
        lesson_data["content"] = convert_markdown_to_html(lesson_data.get("content", []))
    response = make_response(render_template('learn-page/python-flask-framework/py-lessons-4.html', lesson_data=lesson_data))
    response.headers['Cache-Control'] = 'public, max-age=86400'  # Cache di browser selama 1 hari
    return response