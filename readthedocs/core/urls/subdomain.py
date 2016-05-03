from operator import add

from django.conf.urls import url, patterns
from django.conf import settings
from django.conf.urls.static import static

from readthedocs.constants import pattern_opts

handler500 = 'readthedocs.core.views.server_error'
handler404 = 'readthedocs.core.views.server_error_404'

subdomain_urls = patterns(
    '',  # base view, flake8 complains if it is on the previous line.
    url(r'^page/(?P<filename>.*)$',
        'readthedocs.core.views.serve.redirect_page_with_filename',
        name='docs_detail'),

    url(r'^$', 'readthedocs.core.views.serve.redirect_project_slug', name='redirect_project_slug'),
    # Just for reversing URL's for now
    url((r'^(?P<lang_slug>{lang_slug})/'
         r'(?P<version_slug>{version_slug})/'
         r'(?P<filename>{filename_slug})$'.format(**pattern_opts)),
        'readthedocs.core.views.serve.serve_docs',
        name='docs_detail'),
)

groups = [subdomain_urls]

# Needed to serve media locally
if getattr(settings, 'DEBUG', False):
    groups.insert(0, static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

urlpatterns = reduce(add, groups)