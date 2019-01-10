import pathlib

from views import index, control

def setup_routes(app):
    app.router.add_get('/', index, name='index')
    app.router.add_get('/control', control, name='control')
    setup_static_routes(app)
    

def setup_static_routes(app):
    app.router.add_static('/static/',
                          path='./static',
                          name='static')
