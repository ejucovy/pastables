from webob import Response

class ImgLinkFilter(object):
    def __init__(self, app, raw_link):
        self.app = app
        self.raw_link = raw_link

    def __call__(self, environ, start_response):
        location = environ['PATH_INFO']
        raw_link = self.raw_link % location
        return Response("""<a href="%s"><img src="%s" /></a>""" % (raw_link, raw_link))

def filter_factory(global_conf, **kw):
    def filter(app):
        return ImgLinkFilter(app)
    return filter
