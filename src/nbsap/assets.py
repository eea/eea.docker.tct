from django_assets import Bundle, register
from django.conf import settings

JS_ASSETS = (
    'js/jquery-1.7.1.min.js',
    'js/jquery.uniform.js',
    'js/jquery.utils.js',
    'js/uri.js',
    'bootstrap/js/bootstrap.js',
    'js/main.js',
)

JS_ADMIN_ASSETS = (
    'js/lib/datatables/jquery.dataTables.min.js',
    'js/lib/datatables/DT_bootstrap.js',
)

CSS_ASSETS = (
    'bootstrap/css/bootstrap.css',
    'bootstrap/css/bootstrap-responsive.css',
    'css/bootstrap-ui/jquery-ui-1.8.16.custom.css',
    'css/bootstrap-ui/jquery.ui.1.8.16.ie.css',
    'css/style.css',
) + settings.CSS_ASSETS

js = Bundle(*JS_ASSETS, filters='jsmin', output='gen/packed.js')
js_admin = Bundle(*JS_ADMIN_ASSETS, filters='jsmin', output='gen/admin_packed.js')

css = Bundle(*CSS_ASSETS, filters='cssmin', output='gen/packed.css')

register('js', js)
register('js_admin', js_admin)
register('css', css)
