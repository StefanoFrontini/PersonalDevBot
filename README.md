# PersonalDevBot

*A simple twitter bot that stores and tweets personal development quotes I like*

[Twitter Bot](https://twitter.com/PersonalDevBot)

[PersonalDevBot Website](http://stefanofrontini75.pythonanywhere.com/)

Powered by: Python, Flask and MySQL

## Libraries used:
* Flask
* Flask_mysqldb
* Passlib
* WTForms
* Tweepy

## Want to create your own Twitter bot?
#### [Step1] Create a folder and git clone the repository
`git clone https://github.com/StefanoFrontini/PersonalDevBot.git .`


#### [Step2] In the folder you created add a secret_code.py file:
```python
# Twitter credentials
consumer_key = "<your twitter consumer key here>"
consumer_secret = "<your twitter consumer secret key here>"
access_token = "<your twitter access token here>"
access_token_secret = "<your twitter access token secret here>"

# MySQL credentials
mysql_host = "<your mysql host>"
mysql_user = "<your mysql user>"
mysql_password = "<your mysql password>"
mysql_db_name = "<your mysql db name>"

# Other keys
register_key = "<this key let a user register to the site, add quotes and tweet>"
flask_secret_key = '<youe flask secret key here>'
```


#### [Step3] 
* Install MySQL
* From the mysql command line create the DB using this sql command :`CREATE DATABASE <your mysql db name>;`
* From the mysql command line run the commands found on schema.sql 

## Usage
* Register
* Login
* Go to Add Phrase page and add a quote you like
* Go to Home and press Tweet!
