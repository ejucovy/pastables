import site
from paste.deploy.loadwsgi import loadapp

def app_factory(global_conf, virtualenv=None, config=None, **kw):

    assert virtualenv is not None

    site.addsitedir(virtualenv)
    return loadapp(config)

