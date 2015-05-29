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
                self._dataCache = {}
                exec f.read() in self._dataCache
        return self._dataCache[self.name]

    def get_currency(self):
        return self._data().get_currency()

    def get_order(self, id_):
        return self._data().get_order(id_)

    def iter_orders(self):
        return self._data().iter_orders()

    def iter_payments(self, order):
        return self._data().iter_payments(order)

    def iter_items(self, order):
        return self._data().iter_items(order)
