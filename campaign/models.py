# from sqlalchemy.dialects.postgresql import JSON
# from flask2.flask_app import db

# class Campaign(db.Model):
# 	__tablename__ = 'campaigns'

# 	id = db.Column(db.Integer, primary_key=True)
# 	campaign_name = db.Column(db.String(100), unique=True, nullable=False)
# 	day_flow = db.Column(JSON)
# 	mail_info = db.Column(JSON)

# 	def __init__(self, campaign_name, day_flow, mail_info):
# 		self.campaign_name = campaign_name
# 		self.day_flow = day_flow
# 		self.mail_info = mail_info