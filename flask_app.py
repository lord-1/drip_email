from config import set_config, register_views
app, db, scheduler = set_config()

register_views(app)

if __name__ == '__main__':
	scheduler.start()
	app.run(debug=True)

'''
This design has flaw that both the shell and the server cannot be used at 
the same time, need to fix it.
'''