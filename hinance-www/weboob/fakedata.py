from weboob.capabilities.bank import Account
from datetime import datetime
from decimal import Decimal

class FakeBank:
  def __init__(self):
    self._accounts = []
  def add(self, account):
    self._accounts.append(account)
  def iter_accounts(self):
    return self._accounts
  def get_account(self, id_):
    for a in self._accounts:
      if a.id() == id_:
        return a
  def iter_history(self, account):
    #TODO
    return []

class FakeShop:
  def __init__(self, cur):
    self._cur = cur
  def get_currency(self):
    return self._cur
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

class FakeAccount:
  def __init__(self, **kwArgs):
    self._fields = kwArgs
  def id(self):
    return self._fields['id']
  def account(self):
    a = Account()
    for k, v in self._fields.values():
      setattr(a, k, v)
    a.balance = Decimal(0) #TODO
    return a

crispybills = FakeBank()
windyvault = FakeBank()
awesome = FakeShop('USD')
awesomecard = FakeBank()
viogor = FakeShop('USD')
viogorcard = FakeBank()
megarags = FakeShop('USD')
itchyback = FakeShop('USD')

awesome1875 = FakeAccount(
  id='1875',
  type=Account.TYPE_CARD,
  label=u'Awesome Stuff Store Card ***1875',
  currency='USD',
  paydate=datetime(2015,5,25),
  paymin=Decimal(25),
  cardlimit=Decimal(3000))
master8385 = FakeAccount(
  id='8385',
  type=Account.TYPE_CARD,
  label=u'Crispy Bills Bank Mastercard Credit Card ***8385',
  currency='USD',
  paydate=datetime(2015,6,12),
  paymin=Decimal(15),
  cardlimit=Decimal(1000))
checking1042 = FakeAccount(
  id='1042',
  type=Account.TYPE_CHECKING,
  label=u'Windy Vault Bank Checking Account ***1042',
  currency='USD')
savings2453 = FakeAccount(
  id='2453',
  type=Account.TYPE_SAVINGS,
  label=u'Windy Vault Bank Savings Account ***2453',
  currency='USD')
viogor7260 = FakeAccount(
  id='7260',
  type=Account.TYPE_CARD,
  label=u'Violently Gorgeous Store Card ***7260',
  currency='USD',
  paydate=datetime(2015,6,20),
  paymin=Decimal(0),
  cardlimit=Decimal(1500))
visa8394 = FakeAccount(
  id='8394'
  type=Account.TYPE_CARD,
  label=u'Windy Vault Bank Visa Credit Card ***8394',
  currency='USD',
  paydate=datetime(2015,6,10),
  paymin=Decimal(0),
  cardlimit=Decimal(2000))

awesomecard.add(awesome1875)
crispybills.add(master8385)
windyvault.add(checking1042)
windyvault.add(savings2453)
windyvault.add(visa8394)
viogorcard.add(viogor7260)
