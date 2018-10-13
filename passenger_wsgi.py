import imp
import os
import sys


sys.path.insert(0, os.path.dirname(__file__))

wsgi = imp.load_source('wsgi', 'medisproj/wsgi.py')
application = wsgi.application
# def application(environ, start_response):
#     start_response('200 OK', [('Content-Type', 'text/plain')])
#     message = 'Maintenance... \n'
#     # version = 'Python %s\n' % sys.version.split()[0]
#     version = 'Sedang dalam pengembangan...!'
#     response = '\n'.join([message, version])
#     return [response.encode()]