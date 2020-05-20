from flask import render_template
from flask_wtf import FlaskForm
from app.forms import ContactForm

def contact():
    form = ContactForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('contact.html', form=form)