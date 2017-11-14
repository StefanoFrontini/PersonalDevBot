import unittest
import app
import secrets


class TestDevBot(unittest.TestCase):
    
    def setUp(self):
        app.app.config['MYSQL_DB'] = 'test_devbot'
        app.app.config['TESTING'] = True              
        self.app = app.app.test_client()
        with app.app.app_context():
            app.init_db()
    
    def tearDown(self):
        pass     

    def test_index(self):
        rv = self.app.get('/', content_type='html/text')
        self.assertEqual(rv.status_code, 200)
    
    def test_welcome(self):
        rv = self.app.get('/', content_type='html/text')
        self.assertTrue(b'Welcome To PersonalDevBot' in rv.data)
    
    def register(self, name, password, confirm, key):
        return self.app.post('/register', data=dict(name=name, password=password, confirm=confirm, key=key), follow_redirects=True)

    def login(self, username, password):
        return self.app.post('/login', data=dict(username=username, password=password), follow_redirects=True)
    
    def logout(self):
        return self.app.get('/logout', follow_redirects=True)         

    def test_register_login_logout(self):
        rv = self.register('Admin', 'Admin', 'Admin', secrets.register_key)
        self.assertIn(b'You are now registered and can login in', rv.data)
        rv = self.login('Admin', 'Admin')
        self.assertIn(b'You are now logged in', rv.data)
        rv = self.logout()
        self.assertIn(b'You are now logged out', rv.data)
        rv = self.login('Ad', 'Admin')
        self.assertIn(b'Username not found', rv.data)
        rv = self.register('Admin', 'Admin', 'Admin', 'wrong_key')
        self.assertIn(b'Invalid Key', rv.data)
    
    def add_new(self, first_name, last_name, phrase):
        return self.app.post('/add_phrase', data=dict(first_name=first_name, last_name=last_name, phrase=phrase), follow_redirects=True)
    
    def test_add(self):
        rv = self.register('Admin', 'Admin', 'Admin', secrets.register_key)
        rv = self.login('Admin', 'Admin')
        self.assertIn(b'No New Phrases Found', rv.data)
        rv = self.add_new('Stefano', 'Frontini', 'Ciao!')
        self.assertIn(b'Phrase Created', rv.data)
#        rv = self.app.get('/tweet', content_type='html/text')
#        self.assertIn(b'Tweet sent!', rv.data)

      
    
#    def test_twitter(self):
#       rv = self.register('Admin', 'Admin', 'Admin', secrets.register_key)
#        rv = self.login('Admin', 'Admin')
#        rv = self.app.get('/twitter', content_type='html/text')

if __name__ == '__main__':    
    unittest.main()

