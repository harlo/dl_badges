import os, tornado.web

class DeepLabBadgeApp(tornado.web.Application):
	def __init__(self):
		print "Initing DeepLab Badges Server..."

		self.routes = []

	def run():
		print "Starting DeepLab Badges Server..."


if __name__ == "__main__":
	app = DeepLabBadgeApp()
	app.run()