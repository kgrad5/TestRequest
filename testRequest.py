import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import smtplib

from datetime import datetime
from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
	fields = [ 'FogBugz Cases:', 'Changes/Features:', 'System impact:', 'Tests written:', 'What needs testing:']
	
	def __init__(self):
		handlers = [
			(r"/", IndexHandler),
		]
		settings = dict(
			template_path = os.path.join(os.path.dirname(__file__), "templates"),
			static_path = os.path.join(os.path.dirname(__file__), "static"),
			debug = True,	
		)	
		tornado.web.Application.__init__(self, handlers, **settings)
		
class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html', fields = Application.fields, error_message = "")
	def post(self):
		sender = ''
		receivers = ['']

		message = """From: 
To: 
Subject: Request for testing

"""
		try:
			message += "From: " + self.get_argument('from') +"\n\n"
		except:
			self.render('index.html', fields = Application.fields, error_message = "All fields are required.")
		for field in Application.fields:
			try:
				arg = self.get_argument(field.replace(' ', '-'))
			except:
				self.render('index.html', fields = Application.fields, error_message = "All fields are required.")

			line = field + "\n" + arg + '\n\n'
			message += line
		
		try:
   			smtpObj = smtplib.SMTP('localhost')
   			smtpObj.sendmail(sender, receivers, message)         
   			print("Successfully sent email")
		except SMTPException:
   			print("Error: unable to send email")

		self.render('index.html', fields = Application.fields, error_message="")


if __name__ == '__main__':
	# Parse the command line options defined with define() statements, this comes from the
	# tornado.options package
	tornado.options.parse_command_line()
	
	# Boilerplate
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
