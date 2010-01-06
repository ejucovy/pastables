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

def app_factory(global_conf, **local_conf):
    redirect = local_conf['redirect_to']
    return Redirector(redirect)
    
class Redirector(object):
    def __init__(self, redirect):
        self.redirect = redirect

    def __call__(self, environ, start_response):
        return exc.HTTPFound(location=self.redirect)(
            environ, start_response)
