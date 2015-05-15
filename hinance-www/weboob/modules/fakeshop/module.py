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
