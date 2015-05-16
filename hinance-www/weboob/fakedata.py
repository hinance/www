from weboob.capabilities.bank import Account, Transaction
from datetime import datetime, timedelta
from decimal import Decimal
from random import seed, sample, randint, choice

class FakeBank:
  def __init__(self):
    self._accounts = []
  def add(self, *accounts):
    self._accounts += accounts
  def iter_accounts(self):
    return [a.account() for a in self._accounts]
  def get_account(self, id_):
    for a in self.iter_accounts():
      if a.id == id_:
        return a
  def iter_history(self, account):
    for a in self._accounts:
      if a.id() == account.id:
        return a.transactions()

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
    self._transactions = []
  def add(self, *transactions):
    self._transactions += list(transactions)
  def id(self):
    return self._fields['id']
  def account(self):
    a = Account()
    for k, v in self._fields.items():
      setattr(a, k, v)
    a.balance = Decimal(sum(t.amount for t in self._transactions))
    return a
  def transactions(self):
    return sorted(self._transactions, cmp=lambda t1, t2: cmp(t2.date, t1.date))

def transaction(**kwArgs):
  t = Transaction()
  for k, v in kwArgs.items():
    setattr(t, k, v)
  return t

def datesrange(tuplefrom, tupleto):
  dtfrom, dtto = datetime(*tuplefrom), datetime(*tupleto)
  return (dtfrom + timedelta(days=d) for d in xrange(0, (dtto-dtfrom).days))

seed(10000)

#
# Banks & Shops
#

crispybills = FakeBank()
windyvault = FakeBank()
awesome = FakeShop('USD')
awesomecard = FakeBank()
viogor = FakeShop('USD')
viogorcard = FakeBank()
megarags = FakeShop('USD')
itchyback = FakeShop('USD')

#
# Banking accounts
#

awesome1875 = FakeAccount(
  id='1875',
  type=Account.TYPE_CARD,
  label=u'Awesome Stuff Store Card ***1875',
  currency=u'USD',
  paydate=datetime(2015,5,25),
  paymin=Decimal(25),
  cardlimit=Decimal(3000))
master8385 = FakeAccount(
  id='8385',
  type=Account.TYPE_CARD,
  label=u'Crispy Bills Bank Mastercard Credit Card ***8385',
  currency=u'USD',
  paydate=datetime(2015,6,12),
  paymin=Decimal(15),
  cardlimit=Decimal(1000))
checking1042 = FakeAccount(
  id='1042',
  type=Account.TYPE_CHECKING,
  label=u'Windy Vault Bank Checking Account ***1042',
  currency=u'USD')
savings2453 = FakeAccount(
  id='2453',
  type=Account.TYPE_SAVINGS,
  label=u'Windy Vault Bank Savings Account ***2453',
  currency=u'USD')
viogor7260 = FakeAccount(
  id='7260',
  type=Account.TYPE_CARD,
  label=u'Violently Gorgeous Store Card ***7260',
  currency=u'USD',
  paydate=datetime(2015,6,20),
  paymin=Decimal(0),
  cardlimit=Decimal(1500))
visa8394 = FakeAccount(
  id='8394',
  type=Account.TYPE_CARD,
  label=u'Windy Vault Bank Visa Credit Card ***8394',
  currency=u'USD',
  paydate=datetime(2015,6,10),
  paymin=Decimal(0),
  cardlimit=Decimal(2000))

awesomecard.add(awesome1875)
crispybills.add(master8385)
windyvault.add(checking1042, savings2453, visa8394)
viogorcard.add(viogor7260)

#
# Transactions
#

# Opening deposits.
checking1042.add(transaction(
  date=datetime(2012,8,1),
  label=u'CHECKING OPENING DEPOSIT',
  amount=Decimal(100)))
savings2453.add(transaction(
  date=datetime(2012,8,1),
  label=u'SAVINGS OPENING DEPOSIT',
  amount=Decimal(100)))

# Cash withdrawals from Windy Vault Bank.
seed(10100)
for account in [checking1042, savings2453]:
  account.add(*[transaction(
    date=date,
    amount=Decimal(randint(-100, -10)*20),
    label=choice([
      u'CASH EWITHDRAWAL IN BRANCH/STORE %s' % date,
      u'CASH EWITHDRAWAL IN BRANCH/STORE',
      u'ATM WITHDRAWAL AUTHORIZED ON %s' % date,
      u'ATM WITHDRAWAL - %s MACH ID %i' % (date, randint(10000,99999))]))
    for date in sample(list(datesrange((2012,10,10), (2015,5,1))), 5)])

# Cash deposits to Windy Vault Bank.
seed(10200)
for account in [checking1042, savings2453]:
  account.add(*[transaction(
    date=date,
    amount=Decimal(randint(10, 100)*20),
    label=choice([
      u'ATM CASH DEPOSIT ON %s' % date,
      u'DEPOSIT MADE IN A BRANCH/STORE',
      u'ATM CASH DEPOSIT - %s MACH ID %i' % (date, randint(10000,99999))]))
    for date in sample(list(datesrange((2012,10,10), (2015,5,1))), 5)])
