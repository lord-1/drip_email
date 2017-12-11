from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler 
import logging

def set_config():
	
	app = Flask(__name__)
	db = SQLAlchemy(app)
	app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost/postgres"
	logging.basicConfig()
	scheduler = BackgroundScheduler()
	scheduler.start()
	return app, db, scheduler


def register_views(app):
	
	from campaign.views import campaign_app
	from user.views import user_app
	app.register_blueprint(campaign_app, url_prefix='/camp')
	app.register_blueprint(user_app, url_prefix='/user')