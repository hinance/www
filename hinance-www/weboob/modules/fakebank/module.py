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

    def _data(self):
        if not hasattr(self, '_dataCache'):
            with open('/hinance-www/weboob/fakedata.py') as f:
                self._dataCache = {}
                exec f.read() in self._dataCache
        return self._dataCache[self.name]

    def iter_accounts(self):
        return self._data().iter_accounts()

    def get_account(self, id_):
        return self._data().get_account(id_)

    def iter_history(self, account):
        return self._data().iter_history(account)
