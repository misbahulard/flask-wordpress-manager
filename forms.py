from flask_wtf import Form
from wtforms import TextField, PasswordField, SubmitField

class CreateForm(Form):
    """Create Form for generate wordpress purpose"""
    
    username = TextField("Input username")
    password = PasswordField("Input password")
    submit = SubmitField("Submit")
