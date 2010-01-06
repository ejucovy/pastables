"""
{{{
[composite:domains]
use = egg:pastables#domain
somanywhales.com = whales
worldofbears.net = bears
your.worldofbears.net = totally-different-bears
zebra-associates.org = zebra

[composite:bears]
use = egg:pastables#strictdomain
edit.worldofbears.net = bears-edit
upload.worldofbears.net = bears-upload
worldofbears.net = bears-published
*.worldofbears.net = default-bears
}}}

currently what we have is neither.
"""

from webob.exc import *

def composite_factory(loader, global_conf, **local_conf):
    domains = generate_hostmap(local_conf)
    return MethodDispatcher(domains)

def strict_composite_factory(loader, global_conf, **local_conf):
    domains = generate_hostmap(local_conf)
    return MethodDispatcher(domains, loose=False)

    
def generate_hostmap(local_conf):
    domains = {}
    for host, appname in local_conf.items():

        domain = '.'.join(host.split('.')[-2:])
        subdomain = '.'.join(host.split('.')[:-2])

        if domain not in domains: domains[domain] = {}

        assert subdomain not in domains[domain], "Duplicate assignment for host %s" % host

        domains[domain][subdomain] = loader.get_app(appname)

    

# TODO: default?
class LiteralHostDispatcher(object):
    def __init__(self, apps, loose=True):
        self.hostmap = apps
        self.loose = loose

    # XXX overridable in config somehow?
    @property
    def default_app(self):
        return HTTPNotFound()

    def __call__(self, environ, start_response):
        host = environ['HTTP_HOST'].split(':')[0]

        domain = '.'.join(host.split('.')[-2:])
        subdomain = '.'.join(host.split('.')[:-2])

        if domain not in self.hostmap:
            return self.default_app(environ, start_response)

        domainmap = self.hostmap[domain]
        if subdomain in domainmap:
            return domainmmap[subdomain](environ, start_response)

        if not self.loose:
            if "*" in domainmap:
                return domainmap["*"](environ, start_response)
            return self.default_app(environ, start_response)

        if '' in domainmap:
            return domainmap[''](environ, start_response)
        return self.default_app(environ, start_response)
