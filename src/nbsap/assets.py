from django_assets import Bundle, register


JS_ASSETS = (
    'js/jquery-1.7.1.min.js',
    'js/jquery.uniform.js',
    'js/chosen.jquery.js',
    'js/jquery.utils.js',
    'bootstrap/js/bootstrap-collapse.js',
    'bootstrap/js/bootstrap-dropdown.js',
    'bootstrap/js/bootstrap-tooltip.js',
)


CSS_ASSETS = (
    'bootstrap/css/bootstrap.css',
    'bootstrap/css/bootstrap-responsive.css',
    'css/bootstrap-ui/jquery-ui-1.8.16.custom.css',
    'css/bootstrap-ui/jquery.ui.1.8.16.ie.css',
    'css/uniform.default.css',
    'css/chosen.css',
    'css/style.css',
)


js = Bundle(*JS_ASSETS, filters='jsmin', output='gen/packed.js')
css = Bundle(*CSS_ASSETS, filters='cssmin', output='gen/packed.css')


register('js', js)
register('css', css)
