from weboob.capabilities.bank import CapBank
from weboob.tools.backend import Module

__all__ = ['FakeBankModule']

class FakeBankModule(Module, CapBank):
    NAME = 'fakebank'
    MAINTAINER = u'Fake Maintainer'
    EMAIL = 'contact@hinance.org'
    VERSION = '1.1'
    LICENSE = 'AGPLv3+'
    DESCRIPTION = u'Fake bank module for Hinance examples'

    def iter_accounts(self):
        #TODO
        return []

    def get_account(self, id_):
        #TODO
        return None

    def iter_history(self, account):
        #TODO
        return []
