from wtforms import Form, StringField, TextAreaField, PasswordField, validators

# Phrase Form class
class PhraseForm(Form):
    first_name = StringField('Author First Name', [validators.Length(min=1, max=30)])
    last_name = StringField('Author Last Name', [validators.Length(min=1, max=30)])
    phrase = TextAreaField('Phrase', [validators.Length(min=1, max=280)])

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
    key = PasswordField('Register Key', [validators.DataRequired()])