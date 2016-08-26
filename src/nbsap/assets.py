from django_assets import Bundle, register
from django.conf import settings

JS_ASSETS = (
    'js/jquery-1.11.1.min.js',
    'js/jquery.utils.js',
    'js/uri.js',
    'bootstrap/js/bootstrap.min.js',
    'js/main.js',
    'js/lib/jquery.columnlist.js',
)

JS_ADMIN_ASSETS = (
    'js/jquery-1.11.1.min.js',
    'js/jquery.utils.js',
    'bootstrap/js/bootstrap.min.js',
    'js/lib/datatables/jquery.dataTables.min.js',
    'js/jquery.browser.min.js',
    'js/uri.js',
    'js/main.js',
    'js/chosen/chosen.jquery.min.js',
    'js/app.min.js'
)

CSS_ASSETS = (
    # 'bootstrap/css/bootstrap.min.css',
    'bootstrap/css/normalize.css',
    'bootstrap/css/skeleton.css',
    'js/chosen/chosen.css',
    'css/style.css'
) + settings.CSS_ASSETS

CSS_ADMIN_ASSETS = (
    'bootstrap/css/bootstrap.min.css',
    'js/lib/datatables/dataTables.bootstrap.min.css',
    'js/chosen/chosen.css',
    'css/AdminLTE.min.css',
    'css/admin_style.css',
    'css/skin-black.min.css'
) + settings.CSS_ASSETS

js = Bundle(*JS_ASSETS, filters='jsmin', output='gen/packed.js')
js_admin = Bundle(*JS_ADMIN_ASSETS, filters='jsmin', output='gen/admin_packed.js')

css = Bundle(*CSS_ASSETS, filters='cssmin', output='gen/packed.css')
css_admin = Bundle(*CSS_ADMIN_ASSETS, filters='cssmin', output='gen/admin_packed.css')

register('js', js)
register('js_admin', js_admin)
register('css', css)
register('css_admin', css_admin)
