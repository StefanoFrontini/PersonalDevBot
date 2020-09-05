from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, g
from flask_mysqldb import MySQL
from passlib.hash import pbkdf2_sha256
from functools import wraps
import tweepy
from random import randint
import secret_code
from form_class import PhraseForm, RegisterForm

app = Flask(__name__) # create the application instance
app.config.from_object(__name__) # load config from this file, app.py

app.config.update(dict(
    # Secret key
    SECRET_KEY='$5$rounds=535000$.BcaNky3Hofqawf6$RizLei0PwoS1ISLhd4XJnJL9VqB5P2e14vCoD9gHth7',
    # MySQL config
    MYSQL_HOST='eu-cdbr-west-03.cleardb.net',
    MYSQL_USER='bac309b2497661',
    MYSQL_PASSWORD='1660d98b',
    MYSQL_DB='heroku_c6c6eb78adee638',
    MYSQL_CURSORCLASS='DictCursor'
))

# init MySQL
mysql = MySQL(app)



def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'mysql_db'):
        g.mysql_db = mysql.connect
    return g.mysql_db

def init_db():
    """Inizializes the Database. Function used only for tests"""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        query = " ".join(f.readlines())
        cur = db.cursor()
        cur.execute(query)
        more = True
        while more:
            more = cur.nextset()
    db.commit()


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'mysql_db'):
        g.mysql_db.close()


# Homepage - Dashboard
@app.route('/', methods=['GET', 'POST'])
def index():
        # Check for db connection
        db = get_db()

        # Create cursor
        cur = db.cursor()

        # Get tweets
        result = cur.execute("SELECT author.first_name, author.last_name, tweets.tweet_phrase, tweets.tweet_date FROM author JOIN tweets ON author.author_id = tweets.author_id ORDER BY tweets.tweet_date DESC")
        tweets = cur.fetchall() # tweets is a tuple of dicts because app.config['MYSQL_CURSORCLASS'] = 'DictCursor'. Default is tuple instead of dict.

        # Logging result and tweets to the console
        app.logger.info(result)
        app.logger.info(tweets)

        if result > 0:
            return render_template('home.html', tweets=tweets)

        else:
            msg = 'No Records Found'
            return render_template('home.html', msg=msg)


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = str(request.form['password'])

        # Check for db connection
        db = get_db()

        # Create cursor
        cur = db.cursor()

        #Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", (username,))

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if pbkdf2_sha256.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('add_phrase'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)


        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    else:
        return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        password = pbkdf2_sha256.hash(str(form.password.data))
        register_key_candidate = form.key.data

        # Check register key
        if register_key_candidate != secret_code.register_key:
            flash('Invalid Key', 'danger')
            return redirect(url_for('register'))

        else:

            # Check for db connection
            db = get_db()

            # Create cursor
            cur = db.cursor()

            cur.execute("INSERT INTO users(username, password) VALUES(%s, %s)", (name, password))

            # Commit to DB
            db.commit()

            flash('You are now registered and can login in', 'success')

            return redirect(url_for('index'))

    else:
        return render_template('register.html', form=form)




# Add Phrase
@app.route('/add_phrase', methods=['GET', 'POST'])
@is_logged_in
def add_phrase():

    # Check for db connection
    db = get_db()

    # Create cursor
    cur = db.cursor()

    # Get tweets
    result = cur.execute("SELECT author.first_name, author.last_name, new_phrases.new_phrase, new_phrases.new_phrase_date FROM author JOIN new_phrases ON author.author_id = new_phrases.author_id ORDER BY new_phrases.new_phrase_date;")
    tweets = cur.fetchall() # tweets is a tuple of dicts because app.config['MYSQL_CURSORCLASS'] = 'DictCursor'. Default is tuple instead of dict.
    app.logger.info(result)
    app.logger.info(tweets)



    if result == 0:
        msg = 'No New Phrases Found'

    else:
        msg = 'Showing new phrases!'

    form = PhraseForm(request.form)
    if request.method == 'POST' and form.validate():
        first_name = form.first_name.data.capitalize()
        #.replace("'", "\u02C8")
        last_name = form.last_name.data.capitalize()
        #.replace("'", "\u02C8")
        phrase = form.phrase.data.capitalize()
        #.replace("'", "\u02C8")

        # Check for db connection
        db = get_db()

        # Create cursor
        cur = db.cursor()


        result = cur.execute("SELECT * FROM author WHERE first_name= %s AND last_name= %s", (first_name, last_name))

        #Check weather author exists
        # if author exists then insert phrase into new_phrases table
        if result > 0:
            author = cur.fetchone()
            cur.execute("INSERT INTO new_phrases(new_phrase, author_id) VALUES (%s, %s)", (phrase, author['author_id']))
        # else insert first_name and last_name into author and new_phrase and author_id into new_phrases
        else:
            cur.execute("INSERT INTO author(first_name, last_name) VALUES (%s, %s)", (first_name, last_name))
            result = cur.execute("SELECT * FROM author WHERE first_name= %s AND last_name= %s", (first_name, last_name))
            author = cur.fetchone()
            cur.execute("INSERT INTO new_phrases(new_phrase, author_id) VALUES (%s, %s)", (phrase, author['author_id']))

        # Commit to DB
        db.commit()


        flash('Phrase Created', 'success')

        return redirect(url_for('add_phrase'))

    else:
        return render_template('add_phrase.html', form=form, tweets=tweets, msg=msg)


# Tweet
@app.route('/tweet')
@is_logged_in
def tweet():
    # Check for db connection
    db = get_db()

    # Create cursor
    cur = db.cursor()

    result = cur.execute("SELECT * FROM new_phrases ORDER BY new_phrase_date limit 1")

    if result > 0:
        row = cur.fetchone()
        new_phrase = row['new_phrase']
        cur.execute("SELECT * FROM author WHERE author_id = %s", (row['author_id'],))
        author_name = cur.fetchone()
        author_first_name = author_name['first_name']
        author_last_name = author_name['last_name']
        message = f"{new_phrase}\n{author_first_name} {author_last_name}"
        cur.execute("INSERT INTO tweets(tweet_phrase, author_id) VALUES (%s, %s)", (new_phrase, author_name['author_id']))
        # Deleting the tweet from new_phrases
        cur.execute("DELETE FROM new_phrases WHERE new_phrase_id = %s", (row['new_phrase_id'],) )

        # Commit to DB
        db.commit()

    else:
        result = cur.execute("SELECT * FROM tweets")
        tweets = cur.fetchall()
        number = randint(0, result - 1)
        row = tweets[number]
        cur.execute("SELECT * FROM author WHERE author_id = %s", (row['author_id'],))
        author_name = cur.fetchone()
        author_first_name = author_name['first_name']
        author_last_name = author_name['last_name']
        message = f"{row['tweet_phrase']}\n{author_first_name} {author_last_name}"

    # Twitter authentication
    auth = tweepy.OAuthHandler(secret_code.consumer_key, secret_code.consumer_secret)
    auth.set_access_token(secret_code.access_token, secret_code.access_token_secret)
    api = tweepy.API(auth)
    auth.secure = True
    # Posting Twitter message
    api.update_status(status=message)

    flash('Tweet sent!', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)


