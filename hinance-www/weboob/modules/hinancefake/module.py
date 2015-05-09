from weboob.capabilities.bank import CapBank, CapShop
from weboob.tools.backend import Module

__all__ = ['HinanceFakeModule']

class HinanceFakeModule(Module, CapBank, CapShop):
    NAME = 'hinancefake'
    MAINTAINER = u'Fake Maintainer'
    EMAIL = 'contact@hinance.org'
    VERSION = '1.1'
    LICENSE = 'AGPLv3+'
    DESCRIPTION = u'Fake module for Hinance examples'

    def iter_accounts(self):
        #TODO
        return []

    def get_account(self, id_):
        #TODO
        return None

    def iter_history(self, account):
        #TODO
        return []

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
