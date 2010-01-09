from webob import Request, Response
from datetime import datetime
from pprint import pformat
import os

def filter_factory(global_conf, base_dir):
    def filter(app):
        return LogMiddleware(app, base_dir)
    return filter

class LogMiddleware(object):
    
    outer_template = """<table><thead>
<th>time</th><th>environ</th>
</thead><tbody>
%s
</tbody></table>
"""

    inner_template = """<tr>
 <td>
  %(time)s
 </td><td>
  %(environ)s
 </td></tr>
"""

    def __init__(self, app, dir):
        self.dir = dir
        self.app = app

    def __call__(self, environ, start_response):
        req = Request(environ)
        
        self.write_entry(environ)

        if environ['PATH_INFO'].startswith('/log/'):
            req.path_info_pop()

            file = open(os.path.sep.join((self.dir, req.path_info)))
            data = file.read()
            file.close()

            template = self.outer_template % data
            return Response(template)(environ, start_response)

        return self.app(environ, start_response)

    def write_entry(self, environ):
        now = datetime.now()

        environ = pformat(environ)

        inner_template = self.inner_template % dict(time=now, environ=environ)
        
        file = open(os.path.join(self.dir, now.strftime('%Y-%m-%d')), 'a')
        print >> file, inner_template
        file.close()

