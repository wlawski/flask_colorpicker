from flask import Markup
from os import path
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class colorpicker(object):
    def __init__(self, app=None, local=[]):
        """
        initiating extension with flask app instance
        @param: app Flask app instance (Default: None)
        @param: local to load .js .css source code locally (Default: [])
        """
        self.app = app
        self.local = local
        if self.app is not None:
            self.init_app(app)
        else:
            raise(AttributeError("must pass app to colorpicker(app=)"))
        if self.local != []:
            if len(self.local) != 2:
                raise(
                    TypeError(
                        "colorpicker(local=) requires a list of" +
                        " two files spectrum.js and spectrum.css"))
        self.injectem()  # injecting module into the template

    def init_app(self, app):
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def teardown(self, exception):
        pass

    def injectem(self):
        """ to inject the module into the template as colorpicker """
        @self.app.context_processor
        def inject_vars():
            return dict(colorpicker=self)

    def loader(self):
        """ to get html imports of colorpicker scripts and css """
        html = ""
        for i, n in enumerate(['js', 'css']):
            links = ('https://cdnjs.cloudflare.com/ajax/' +
                     'libs/spectrum/1.8.0/spectrum.min.css',
                     'https://cdnjs.cloudflare.com/ajax/' +
                     'libs/spectrum/1.8.0/spectrum.min.js') if (
                         self.local == []) else self.local
            for sl in self.local:
                if not path.isfile(sl):
                    raise(FileNotFoundError(
                        "colorpicker.loader() file not found "))
            tags = ['<script src="%s"></script>\n',
                    '<link href="%s" rel="stylesheet">\n']
            html += tags[i] % [
                l for l in links if l.split(
                    '.')[len(l.split('.')) - 1] == n][0]
        return Markup(html)

    def picker(self, id=".colorpicker",
               default_color='rgb(0,0,255)',
               color_format='rgb',
               showAlpha='true',
               showInput='false',
               showButtons='false',
               allowEmpty='true'):
        """
        to get html ready colorpicker initiation with the given options
        @param: id identifier of the html element to assign the color picker to
        (Default: '.colorpicker')
        @param: default_color for the colorpicker to start with (Default:
        'rgb(0,0,255)')
        @param: color_format color format to use (Default: 'rgb')
        @param: showAlpha to enable alpha (Default: 'true')
        @param: showInput to show or hide the color format (Default: 'false')
        @param: showButtons to show or hide buttons (Default: 'false')
        @param: allowEmpty to allow or disallow empty input (Default: 'true')
        """
        for h, a in {'id': id,
                     'showAlpha': showAlpha,
                     'showInput': showInput,
                     'showButtons': showButtons,
                     'allowEmpty': allowEmpty}.items():
            if not isinstance(a, str):
                raise(TypeError("colorpicker.picker(%s) takes string" % h))
            if h != 'id' and a != 'true' and a != 'false':
                raise(TypeError(
                    "colorpicker.picker(%s) only true or false string" % h))
        return Markup(" ".join(['<script>',
                                '$("%s").spectrum({' % id,
                                'showAlpha: %s,' % showAlpha,
                                'showInput: %s,' % showInput,
                                'showButtons: %s,' % showButtons,
                                'allowEmpty: %s,' % allowEmpty,
                                'color: "%s",' % default_color,
                                'preferredFormat: "%s",' % color_format,
                                'move: function(color) {',
                                '$("%s").val(color.toRgbString());' % id,
                                '},', '});',
                                '</script>']))  # html ready colorpicker
