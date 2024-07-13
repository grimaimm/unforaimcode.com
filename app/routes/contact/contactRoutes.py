# ------------------------------------------------------------------------------------------------------------------------------------------------

# Import Library and Function
from . import contact_bp
from flask import render_template, request, flash, redirect, url_for
from flask_mail import Message
from app import mail
import os
from ...utils import log_page_access

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Get a Firestore client
# db = firestore.client()

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Route Contacts
@contact_bp.route('/', methods=['GET', 'POST'])
def contact():
    # Log page access
    log_page_access('contact')
    
    if request.method == 'POST':
        name = request.form['name']
        sender_email = request.form['email']
        message = request.form['message']

        # Membuat pesan email
        msg = Message(subject="New Message from Contact Form",
                    sender=(name, sender_email),
                    recipients=[os.getenv('MAIL_USERNAME')],
                    body=f"Name: {name}\nEmail: {sender_email}\n\nMessage:\n{message}")
        try:
            # Mengirim email
            mail.send(msg)
            flash('Message sent successfully!', 'success')
        except Exception as e:
            flash('Cannot Send Message Now!', 'error')

        return redirect(url_for('contact.contact'))
    
    return render_template('contact-page/contact.html')

# ------------------------------------------------------------------------------------------------------------------------------------------------