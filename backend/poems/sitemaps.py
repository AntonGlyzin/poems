from django.contrib.sitemaps import Sitemap
from .models import Poem

class PoemSitemap(Sitemap):
    priority = 0.9
    def items(self):
        return Poem.published.order_by('-time_create')
    def lastmod(self, obj):
        return obj.time_update
    def location(self, item):
        return f'/poems/poem/{item.slug}'
    def get_domain(self, site=None):
        return 'antonio-poems.web.app'
    def get_protocol(self, protocol=None):
        return 'https'