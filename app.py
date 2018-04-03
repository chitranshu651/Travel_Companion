from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)


# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '4071'
app.config['MYSQL_DB'] = 'project'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init MYSQL
mysql = MySQL(app)


@app.route('/')
def index():
    return render_template("index.html")

# Register Form class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    reg = StringField('Registration No.', [validators.Length(max=8)])
    hostel = StringField('Hostel', [validators.Length(min=4, max=10)])
    room = StringField('Room No', [validators.Length(min=1, max=10)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    mobile = StringField('Mobile', [validators.Length(max=10)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


#User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        reg = form.reg.data
        hostel = form.hostel.data
        room = form.room.data
        email = form.email.data
        mobile = form.mobile.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()

        #Execute query
        cur.execute("INSERT INTO users(reg, name, hostel, room,email ,mobile, password) VALUES(%s,%s,%s,%s,%s,%s,%s)",( reg, name, hostel, room, email , mobile, password))

        #Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


if __name__=='__main__':
    app.secret_key='prashant'
    app.debug = True
    app.run(host = '0.0.0.0',port=5000)
