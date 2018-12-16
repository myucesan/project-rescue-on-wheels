import aiohttp_jinja2
from aiohttp import web

def redirect(router, route_name):
    location = router[route_name].url_for()
    return web.HTTPFound(location)

@aiohttp_jinja2.template('index.html')
async def index(request):
    pass

@aiohttp_jinja2.template('ControlPage.html')
async def control(request):
    pass

       
