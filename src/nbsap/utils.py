import re

DENIED_TAGS = ('html', 'head', 'link', 'body', 'meta', 'script', 'title',
               'style', 'applet',)


def remove_tags(html, tags=DENIED_TAGS):
    """ Returns the given HTML with given tags removed. """
    tags_re = '(%s)' % '|'.join(re.escape(tag) for tag in tags)
    starttag_re = re.compile(r'<%s(/?>|(\s+[^>]*>))' % tags_re, re.U)
    endtag_re = re.compile('</%s>' % tags_re)
    html = starttag_re.sub('', html)
    html = endtag_re.sub('', html)
    return html


def get_next_code(model_cls):
    codes = [int(code.split('.')[0]) for code in
             model_cls.objects.values_list('code', flat=True)]
    return str(max(codes) + 1)
