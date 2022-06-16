# import falcon
# class QuoteResource:
# 	def on_get(self, req, resp):
# 		print(req)
#
# 		"""Handles GET requests"""
# 		quote = {
# 			'quote': (
# 				"I've always been more interested in "
# 				"the future than in the past."
# 			),
# 			'author': 'Grace Hopper'
# 		}
# 		resp.media = quote
# app = falcon.App()
# app.add_route('/quote', QuoteResource())

from pyramid.config import Configurator
from pyramid.response import Response


def hello_world(request):
    return Response(
        "Hello world from Pyramid!\n",
        content_type="text/plain",
    )


config = Configurator()
config.add_route("hello", "/hello")
config.add_view(hello_world, route_name="hello")
app = config.make_wsgi_app()
