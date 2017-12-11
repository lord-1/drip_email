from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask_app import app, db
import os

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	from models import *
	manager.run()



