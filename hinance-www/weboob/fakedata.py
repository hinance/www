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

seed(37944)

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
  label=u'Crispy Bills Bank MasterCard Credit Card ***8385',
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
# Opening deposits.
#

seed(26111)
checking1042.add(transaction(
  date=datetime(2012,8,1),
  label=u'CHECKING OPENING DEPOSIT',
  amount=Decimal(100)))
savings2453.add(transaction(
  date=datetime(2012,8,1),
  label=u'SAVINGS OPENING DEPOSIT',
  amount=Decimal(100)))

#
# Transfers.
#

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

# Check deposits to Windy Vault Bank.
seed(69043)
for account in [checking1042, savings2453]:
  account.add(*[transaction(
    date=date,
    amount=Decimal(randint(20, 300)),
    label=choice([
      u'ATM CHECK DEPOSIT ON %s' % date,
      u'ATM CHECK DEPOSIT - %s MACH ID %i' % (date, randint(10000,99999))]))
    for date in sample(list(datesrange((2012,10,10), (2015,5,1))), 5)])

# Overdraft protection for Windy Vault Bank.
seed(58720)
for date in sample(list(datesrange((2012,10,10), (2015,5,1))), 5):
  amount = Decimal(randint(10,100))
  savings2453.add(transaction(date=date, amount=-amount,
    label=u'OVERDRAFT PROTECTION TO %i1042' % randint(10000,99999)))
  checking1042.add(
    transaction(date=date, amount=amount,
      label=u'OVERDRAFT PROTECTION FROM %i2453' % randint(10000,99999)),
    transaction(date=date, amount=Decimal('-15.50'),
      label=u'OVERDRAFT TRANSFER FEE'))

# Transfers from checking to savings for Windy Vault Bank.
seed(68697)
for date in sample(list(datesrange((2012,10,10), (2015,5,1))), 5):
  amount = Decimal(randint(1,10)*100)
  savings2453.add(transaction(date=date, amount=amount,
    label=u'ONLINE TRANSFER FROM ALISON HENDRIX CHECKING XXXXXX1042 '
          u'REF #%i ON %s' % (randint(10000,99999), date)))
  checking1042.add(
    transaction(date=date, amount=-amount,
      label=u'ONLINE TRANSFER REF #%i TO QUICKSAVE SAVINGS XXXXXX2453 ON %s' \
            % (randint(10000,99999), date)))

# Transfers from savings to checking for Windy Vault Bank.
seed(73916)
for date in sample(list(datesrange((2012,10,10), (2015,5,1))), 5):
  amount = Decimal(randint(1,10)*100)
  savings2453.add(transaction(date=date, amount=-amount,
    label=u'ONLINE TRANSFER TO ALISON HENDRIX CHECKING XXXXXX1042 '
          u'REF #%i ON %s' % (randint(10000,99999), date)))
  checking1042.add(
    transaction(date=date, amount=amount,
      label=u'ONLINE TRANSFER REF #%i FROM QUICKSAVE SAVINGS XXXXXX2453 ON %s'\
            % (randint(10000,99999), date)))

# Payments for Windy Vault Bank credit card.
seed(40726)
for date in sample(list(datesrange((2012,11,1), (2015,5,1))), 10):
  amount = Decimal(randint(300,1500))
  visa8394.add(transaction(date=date, amount=amount,
    label=u'ONLINE PAYMENT'))
  checking1042.add(transaction(date=date, amount=-amount, label=choice([
    u'ONLINE TRANSFER REF #%i TO SECURED CARD XXXXXXXXXXXX8394 ON %s' % (
      randint(10000,99999), date),
    u'ONLINE TRANSFER REF #%i TO VISA XXXXXXXXXXXX8394 ON %s' % (
      randint(10000,99999), date)])))

# Check payments for Crispy Bills Bank credit card.
seed(95162)
for date in sample(list(datesrange((2013,12,1), (2015,5,1))), 5):
  amount = Decimal(randint(300,2000))
  master8385.add(transaction(date=date, amount=amount,
    label=u'ONLINE PAYMENT, THANK YOU'))
  checking1042.add(transaction(date=date, amount=-amount, label=choice([
    u'%i CHECK' % randint(1000,2000)])))

# Online payments for Crispy Bills Bank credit card.
seed(88798)
for date in sample(list(datesrange((2013,12,1), (2015,5,1))), 15):
  amount = Decimal(randint(300,2000))
  master8385.add(transaction(date=date, amount=amount,
    label=u'ONLINE PAYMENT, THANK YOU'))
  checking1042.add(transaction(date=date, amount=-amount, label=choice([
    u'CRISPY CARD ONLINE PAYMENT %s %i ALISON HENDRIX' % (
      date, randint(10000,99999))])))

# Payments for Awesome Stuff store card.
seed(97051)
for date in sample(list(datesrange((2014,5,1), (2015,5,1))), 10):
  amount = Decimal(randint(100,1000))
  awesome1875.add(transaction(date=date, amount=amount,
    label=u'ONLINE PAYMENT'))
  checking1042.add(transaction(date=date, amount=-amount, label=choice([
    u'PAYMENT FOR AWS STORECARD %s %i1875' % (date, randint(10000,99999)),
    u'AWESOME CREDIT AWSC EPAY %s %i1875' % (date, randint(10000,99999))])))

# Payments for Violently Gorgeous store card.
seed(42732)
for date in sample(list(datesrange((2014,2,1), (2015,5,1))), 15):
  amount = Decimal(randint(50,500))
  viogor7260.add(transaction(date=date, amount=amount,
    label=u'PAYMENT - THANK YOU'))
  checking1042.add(transaction(date=date, amount=-amount, label=choice([
    u'CELESTIAL PAY VI WEB PYMT %s %i7260 ALISON HENDRIX' % (
      date, randint(10000,99999)),
    u'CELESTIAL PAY WFN WEB PYMT %s %i7260 ALISON HENDRIX' % (
      date, randint(10000,99999))])))

#
# Purchases.
#

#
# 6PM
#
seed(42732)
# Purchases via Windy Vault Bank debit card.
for date in sample(list(datesrange((2012,10,10), (2013,12,1))), 10):
  amount = Decimal(randint(20,100))
  checking1042.add(transaction(date=date, amount=-amount, label=choice([
    u'CHECK CRD PURCHASE %s PAYPAL *6PM COM 402-935-7733 NV XXXXXXXXXXXX4933'
    u' %i' % (date, randint(10000,99999)),
    u'CHECK CRD PURCHASE %s PAYPAL *6PM COM LL 402-935-7733 CA XXXXXXXXXX4933'
    u' %i' % (date, randint(10000,99999)),
    u'CHECK CRD PURCHASE %s ZAP*DEV 6PM.COM 888-676-2660 NV XXXXXXXXXXXX4933'
    u' %i' % (date, randint(10000,99999)),
    u'CHECK CRD PURCHASE %s ZAP*6PM.COM 888-676-2660 NV XXXXXXXXXXXX4933'
    u' %i' % (date, randint(10000,99999))])))
# Returns to Windy Vault Bank checking account.
for date in sample(list(datesrange((2012,10,10), (2015,5,1))), 5):
  amount = Decimal(randint(20,100))
  checking1042.add(transaction(date=date, amount=amount, label=choice([
    u'CHECK CRD PUR RTRN %s PAYPAL *6PM COM 402-935-7733 NV XXXXXXXXXXXX4933'
    u' %i' % (date, randint(10000,99999)),
    u'CHECK CRD PUR RTRN %s ZAP*6PM.COM 888-676-2660 NV XXXXXXXXXXXX4933'
    u' %i' % (date, randint(10000,99999))])))
# Purchases via Crispy Bills Bank credit card.
for date in sample(list(datesrange((2013,12,1), (2015,5,1))), 10):
  amount = Decimal(randint(20,100))
  master8385.add(transaction(date=date, amount=-amount,
    label=u'ZAP*6PM.COM 888-676-2660 NV'))

#
# 7 ELEVEN
#
seed(85941)
for date in sample(list(datesrange((2013,5,1), (2015,5,1))), 20):
  amount = Decimal(randint(20,40))
  checking1042.add(transaction(date=date, amount=-amount, label=choice([
    u'PURCHASE AUTHORIZED ON %s 7-ELEVEN %i DALLAS TX CARD 4933' \
    % (date, randint(10000,99999)),
    u'POS PURCHASE - %s MACH ID 000000 7 ELEVEN DALLAS TX 4933 %i' \
    % (date, randint(10000,99999))])))

#
# ABEBOOKS.COM
#
seed(17040)
# Purchases via Windy Vault Bank debit card.
for date in sample(list(datesrange((2012,10,10), (2013,12,1))), 5):
  amount = Decimal(randint(5,20))
  checking1042.add(transaction(date=date, amount=-amount, label=
    u'CHECK CRD PURCHASE %s ABEBOOKS.COM 800-315-5335 WA XXXXXXXXXXXX4933 %i' \
    % (date, randint(10000,99999))))
# Purchases via Windy Vault Bank or Crispy Bills Bank credit cards.
for date in sample(list(datesrange((2013,12,1), (2015,5,1))), 10):
  amount = Decimal(randint(5,20))
  account = choice([visa8394, master8385])
  account.add(transaction(date=date, amount=-amount,
    label=u'ABEBOOKS.COM 800-315-5335 WA'))

#
# ALDI
#
seed(13383)
# Purchases via Windy Vault Bank debit card.
for date in sample(list(datesrange((2013,12,1), (2015,5,1))), 20):
  amount = Decimal(randint(50,100))
  checking1042.add(transaction(date=date, amount=-amount, label=choice([
    u'PURCHASE AUTHORIZED ON %s ALDI 75432 1234 DALLAS TX P%i CARD 4933' \
    % (date, randint(10000,99999)),
    u'POS PURCHASE - %s MACH ID 000000 ALDI 75432 1234 DALLAS TX 4933 %i' \
    % (date, randint(10000,99999))])))

#
# AWESOME DIGITAL SERVICES
#
seed(28943)
# Purchases via Windy Vault Bank debit card.
for date in sample(list(datesrange((2014,8,1), (2015,5,1))), 40):
  amount = Decimal(randint(1,10))
  awesome1875.add(transaction(date=date, amount=-amount,
    label=u'AWESOME DIGITAL SEATTLE WA'))
