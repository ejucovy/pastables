from lxml.etree import tostring, _Element
from tempita import HTMLTemplate, html_quote, html

import logging

NOTIFY = (logging.INFO + logging.WARN) / 2
logging.addLevelName(NOTIFY, 'NOTIFY')

class SavingLogger(object):
    """
    Logger that saves all its messages locally.
    """
    def __init__(self):
        self.messages = []

    def message(self, level, el, msg, *args, **kw):
        """Add one message at the given log level"""
        if args:
            msg = msg % args
        elif kw:
            msg = msg % kw
        self.messages.append((level, el, msg))
        return msg

    def debug(self, el, msg, *args, **kw):
        """Log at the DEBUG level"""
        return self.message(logging.DEBUG, el, msg, *args, **kw)
    def info(self, el, msg, *args, **kw):
        """Log at the INFO level"""
        return self.message(logging.INFO, el, msg, *args, **kw)
    def notify(self, el, msg, *args, **kw):
        """Log at the NOTIFY level"""
        return self.message(NOTIFY, el, msg, *args, **kw)
    def warn(self, el, msg, *args, **kw):
        """Log at the WARN level"""
        return self.message(logging.WARN, el, msg, *args, **kw)
    warning = warn
    def error(self, el, msg, *args, **kw):
        """Log at the ERROR level"""
        return self.message(logging.ERROR, el, msg, *args, **kw)
    def fatal(self, el, msg, *args, **kw):
        """Log at the FATAL level"""
        return self.message(logging.FATAL, el, msg, *args, **kw)

    log_template = HTMLTemplate('''\
    <h1 style="border-top: 3px dotted #f00">Log Information</h1>

    {{if log.messages}}
      <h2>Log</h2>
      <table>
          <tr>
            <th>Level</th><th>Message</th><th>Context</th>
          </tr>
        {{for level, level_name, el, message in log.resolved_messages():}}
          {{py:color, bgcolor = log.color_for_level(level)}}
          <tr style="color: {{color}}; background-color: {{bgcolor}}; vertical-align: top">
            {{td}}{{level_name}}</td>
            {{td}}{{message}}</td>
            {{td}}{{log.obj_as_html(el) | html}}</td>
          </tr>
        {{endfor}}
      </table>
    {{else}}
      {{h2}}No Log Messages</h2>
    {{endif}}
    ''', name='pastables.request_logger.log_template')
     
    def format_html_log(self, **kw):
        """Formats this log object as HTML"""

        return self.log_template.substitute(log=self, **kw)

    def resolved_messages(self):
        """
        Yields a list of ``(level, level_name, context_el, rendered_message)``
        """
        for level, el, msg in self.messages:
            level_name = logging.getLevelName(level)
            yield level, level_name, el, msg

    def obj_as_html(self, el):
        """
        Returns the object formatted as HTML.  This is used to show
        the context in log messages.
        """
        ## FIXME: another magic method?
        if hasattr(el, 'log_description'):
            return el.log_description(self)
        elif isinstance(el, _Element):
            return html_quote(tostring(el))
        else:
            return html_quote(unicode(el))

    colors_for_levels = {
        logging.DEBUG: ('#666', '#fff'),
        logging.INFO: ('#333', '#fff'),
        NOTIFY: ('#000', '#fff'),
        logging.WARNING: ('#600', '#fff'),
        logging.ERROR: ('#fff', '#600'),
        logging.CRITICAL: ('#000', '#f33')}
    
    def color_for_level(self, level):
        """
        The HTML foreground/background colors for a given level.
        """
        return self.colors_for_levels[level]


class PrintingLogger(SavingLogger):
    """Logger that saves messages, but also prints out messages
    immediately"""

    def __init__(self, print_level=logging.DEBUG):
        SavingLogger.__init__(self, middleware)
        self.print_level = print_level

    def message(self, level, el, msg, *args, **kw):
        """Add one message at the given log level"""
        msg = super(PrintingLogger, self).message(
            level, el, msg, *args, **kw)
        if level >= self.print_level:
            if isinstance(el, _Element):
                s = tostring(el)
            else:
                s = str(el)
            print '%s (%s)' % (msg, s)
        return msg

class RequestLoggerMiddleware(object):
    def __init__(self, app, environ_key=None, log_factory=None, log_factory_kw=None):
        self.app = app

        log_factory_kw = log_factory_kw or {}
        log_factory = log_factory or SavingLogger

        self.logger = log_factory(**log_factory_kw)
        self.environ_key = environ_key or 'pastables.logger'

    def __call__(self, environ, start_response):
        _old_logger = environ.get(self.environ_key)
        environ[self.environ_key] = self.logger
        res = self.app(environ, start_response)

        if _old_logger:
            environ[self.environ_key] = _old_logger
        else:
            del environ[self.environ_key]
        return res

