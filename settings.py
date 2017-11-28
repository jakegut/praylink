import os

SECRET_KEY="asdlfkjasd;lfjasd;lfj"
DEBUG = True
PER_PAGE = 10
# DB_USERNAME = 'borgdude'
# DB_PASSWORD = ''
# BLOG_DB_NAME = 'blog'
# DB_HOST = os.getenv("IP", '0.0.0.0')
# DB_URI = "mysql+pymysql://%s:%s@%s/%s" % (DB_USERNAME, DB_PASSWORD, DB_HOST, BLOG_DB_NAME)
db_path = os.path.join(os.path.dirname(__file__), 'app.db')
db_uri = 'sqlite:///{}'.format(db_path)
SQLALCHEMY_DATABASE_URI = db_uri
CELERY_BROKER = "amqp://localhost/"
SQLALCHEMY_TRACK_MODIFICATIONS = True
TWILIO_NUMBER = "+19799852372"
TWILIO_ACCOUNT_SID = "AC744e39fb93fbf1eb1c7daa5f3387833c"
TEST_ACCOUNT_SID = "ACf1ff724f7bdd84ad8ecd488cf61710d3"
TWILIO_AUTH_TOKEN = "d9222b83165d5297efcbc60a12deb594"
TEST_AUTH_TOKEN = "35a61d6c62c15acedf9ed7aae4948732"