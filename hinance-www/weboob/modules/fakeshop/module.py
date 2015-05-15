from weboob.capabilities.shop import CapShop
from weboob.tools.backend import Module

__all__ = ['FakeShopModule']

class FakeShopModule(Module, CapShop):
    NAME = 'fakeshop'
    MAINTAINER = u'Fake Maintainer'
    EMAIL = 'contact@hinance.org'
    VERSION = '1.1'
    LICENSE = 'AGPLv3+'
    DESCRIPTION = u'Fake shop module for Hinance examples'

    def _data(self):
        if not hasattr(self, '_dataCache'):
            with open('/hinance-www/weboob/fakedata.py') as f:
                self._dataCache = eval(f.read())
        return self._dataCache

    def get_currency(self):
        #TODO
        return 'USD'

    def get_order(self, id_):
        #TODO
        return None

    def iter_orders(self):
        #TODO
        return []

    def iter_payments(self, order):
        #TODO
        return []

    def iter_items(self, order):
        #TODO
        return []
