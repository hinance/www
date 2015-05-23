from weboob.capabilities.bank import Account, Transaction
from weboob.capabilities.shop import Order, Payment, Item
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_UP
from random import seed, sample, randint, choice, random
from urllib import urlencode

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
    self._orders = []
  def add(self, *orders):
    self._orders += orders
  def get_currency(self):
    return self._cur
  def get_order(self, id_):
    for o in self.iter_orders():
      if o.id == id_:
        return o
  def iter_orders(self):
    return sorted([o.order() for o in self._orders],
      cmp=lambda o1, o2: cmp(o2.date, o1.date))
  def iter_payments(self, order):
    for o in self._orders:
      if o.id() == order.id:
        return o.payments()
  def iter_items(self, order):
    for o in self._orders:
      if o.id() == order.id:
        return o.items()

class FakeAccount:
  def __init__(self, **kwArgs):
    self._fields = kwArgs
    self._transactions = []
  def add(self, *transactions):
    self._transactions += transactions
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

class FakeOrder:
  def __init__(self, **kwArgs):
    self._fields = kwArgs
    self._payments = []
    self._items = []
  def add_payments(self, *payments):
    self._payments += payments
  def add_items(self, *items):
    self._items += items
  def id(self):
    return self._fields['id']
  def order(self):
    o = Order()
    for k, v in self._fields.items():
      setattr(o, k, v)
    return o
  def payments(self):
    return self._payments
  def items(self):
    return self._items

def transaction(**kwArgs):
  t = Transaction()
  for k, v in kwArgs.items():
    setattr(t, k, v)
  return t

def payment(**kwArgs):
  p = Payment()
  for k, v in kwArgs.items():
    setattr(p, k, v)
  return p

def item(**kwArgs):
  i = Item()
  for k, v in kwArgs.items():
    setattr(i, k, v)
  return i

def itemurl(label, price, shopname):
  shop = globals()[shopname]
  return u'../../../fakeshop.html?%s' % urlencode({'shopname': shopname,
    'label': label, 'price': '%.2f' % price, 'cur': shop.get_currency()})

def datesrange(tuplefrom, tupleto):
  dtfrom, dtto = datetime(*tuplefrom), datetime(*tupleto)
  return (dtfrom + timedelta(days=d) for d in xrange(0, (dtto-dtfrom).days))

def randwords(parts):
  return u' '.join(filter(None, (choice(part) for part in parts)))

def randsum(total, n):
  points = sorted(sample(xrange(1,total), n-1) + [0, total])
  return [points[i+1]-points[i] for i in xrange(len(points)-1)]

def matchingaccs(date, anytags=None, alltags=None):
  ACCDATES = [
    (visa0375,     datetime(2012, 7,1), datetime(2012,11,1),
                   {'manual', 'arpa', 'awesome', 'itchyback'}),
    (visa3950,     datetime(2012, 7,1), datetime(2012,12,1),
                   {'manual', 'bom', 'awesome'}),
    (checking1042, datetime(2012, 7,1), datetime(2015, 5,1),
                   {'auto', 'wv', 'awesome', 'itchyback','megarags','viogor'}),
    (visa8394,     datetime(2012,11,1), datetime(2015, 5,1),
                   {'auto', 'wv', 'awesome', 'megarags', 'viogor'}),
    (master8385,   datetime(2013,12,1), datetime(2015, 5,1),
                   {'auto','cb','awesome','itchyback','megarags','viogor'}),
    (viogor7260,   datetime(2014, 2,1), datetime(2015, 5,1),
                   {'auto', 'viogor'}),
    (awesome1875,  datetime(2014, 4,1), datetime(2015, 5,1),
                   {'auto', 'awesome'}),
    (awesomegift,  datetime(2012, 7,1), datetime(2015, 5,1),
                   {'manual', 'awesome'}),
    (viogorgift,   datetime(2012, 7,1), datetime(2015, 5,1),
                   {'manual', 'viogor'})]
  return [a for a, dfrom, dto, ts in ACCDATES
          if dfrom <= date <= dto
          and ((anytags and any((t in ts) for t in anytags)) or
               (alltags and all((t in ts) for t in alltags)))]

def randacc(*args, **kwArgs):
  return choice(matchingaccs(*args, **kwArgs))

def paymethod(account):
  if account == visa0375:
    return u'VISA 0375'
  elif account == visa3950:
    return u'VISA 3950'
  elif account == checking1042:
    return choice([u'VISA 4933', u'VISA 4307', u'Visa | Last 4 digits: 4307'])
  elif account == visa8394:
    return choice([u'VISA 8394', u'Visa | Last 4 digits: 8394'])
  elif account == master8385:
    return choice([u'MASTERCARD 8385', u'MasterCard | Last 4 digits: 8385'])
  elif account == viogor7260:
    return u'Violently Gorgeous Card ending in 7260'
  elif account == awesome1875:
    return choice([u'AWESOMEPLCC 1875', u'Awesome.com Store Card 1875'])
  elif account == awesomegift:
    return u'GIFT CARD'
  elif account == viogorgift:
    return choice([u'eGift/Gift Cards', u'Rebate', u'Refund Credit',
                   u'Shipping & Handling Credit'])

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
visa0375 = FakeAccount()
visa3950 = FakeAccount()
awesomegift = FakeAccount()
viogorgift = FakeAccount()

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
checking1042.add(transaction(
  date=datetime(2012,11,1),
  label=u'WINDY VAULT FOPS SECUREDCAR 121101 12345678 TURANGA,LEELA',
  amount=Decimal(-1000)))

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
    for date in sample(list(datesrange((2012,7,10), (2015,5,1))), 5)])

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
    for date in sample(list(datesrange((2012,7,10), (2015,5,1))), 5)])

# Check deposits to Windy Vault Bank.
seed(69043)
for account in [checking1042, savings2453]:
  account.add(*[transaction(
    date=date,
    amount=Decimal(randint(20, 300)),
    label=choice([
      u'ATM CHECK DEPOSIT ON %s' % date,
      u'ATM CHECK DEPOSIT - %s MACH ID %i' % (date, randint(10000,99999))]))
    for date in sample(list(datesrange((2012,7,10), (2015,5,1))), 5)])

# Overdraft protection for Windy Vault Bank.
seed(58720)
for date in sample(list(datesrange((2012,7,10), (2015,5,1))), 5):
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
for date in sample(list(datesrange((2012,7,10), (2015,5,1))), 5):
  amount = Decimal(randint(1,10)*100)
  savings2453.add(transaction(date=date, amount=amount,
    label=u'ONLINE TRANSFER FROM LEELA TURANGA CHECKING XXXXXX1042 '
          u'REF #%i ON %s' % (randint(10000,99999), date)))
  checking1042.add(
    transaction(date=date, amount=-amount,
      label=u'ONLINE TRANSFER REF #%i TO QUICKSAVE SAVINGS XXXXXX2453 ON %s' \
            % (randint(10000,99999), date)))

# Transfers from savings to checking for Windy Vault Bank.
seed(73916)
for date in sample(list(datesrange((2012,7,10), (2015,5,1))), 5):
  amount = Decimal(randint(1,10)*100)
  savings2453.add(transaction(date=date, amount=-amount,
    label=u'ONLINE TRANSFER TO LEELA TURANGA CHECKING XXXXXX1042 '
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
    u'%i CHECK' % randint(1000,1100)])))

# Online payments for Crispy Bills Bank credit card.
seed(88798)
for date in sample(list(datesrange((2013,12,1), (2015,5,1))), 15):
  amount = Decimal(randint(300,2000))
  master8385.add(transaction(date=date, amount=amount,
    label=u'ONLINE PAYMENT, THANK YOU'))
  checking1042.add(transaction(date=date, amount=-amount, label=choice([
    u'CRISPY CARD ONLINE PAYMENT %s %i LEELA TURANGA' % (
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
    u'CELESTIAL PAY VI WEB PYMT %s %i7260 LEELA TURANGA' % (
      date, randint(10000,99999)),
    u'CELESTIAL PAY WFN WEB PYMT %s %i7260 LEELA TURANGA' % (
      date, randint(10000,99999))])))

#
# Bank purchases.
#

#
# 6PM, INSTYLE
#
seed(42732)
# Purchases via Windy Vault Bank debit card.
for date in sample(list(datesrange((2012,7,10), (2013,12,1))), 15):
  amount = Decimal(randint(2000,10000))/100
  checking1042.add(transaction(date=date, amount=-amount, label=choice([
    u'TWX*%i*INSTYLE 877-312-1121 NY' % randint(10000,99999),
    u'TME*%i*INSTYLE 855-226-0424 NY' % randint(10000,99999),
    u'TWX*%i*INSTYLE 800-882-6317 NY' % randint(10000,99999),
    u'CHECK CRD PURCHASE %s PAYPAL *6PM COM 402-935-7733 NV XXXXXXXXXXXX4933'
    u' %i' % (date, randint(10000,99999)),
    u'CHECK CRD PURCHASE %s PAYPAL *6PM COM LL 402-935-7733 CA XXXXXXXXXX4933'
    u' %i' % (date, randint(10000,99999)),
    u'CHECK CRD PURCHASE %s ZAP*DEV 6PM.COM 888-676-2660 NV XXXXXXXXXXXX4933'
    u' %i' % (date, randint(10000,99999)),
    u'CHECK CRD PURCHASE %s ZAP*6PM.COM 888-676-2660 NV XXXXXXXXXXXX4933'
    u' %i' % (date, randint(10000,99999))])))
# Returns to Windy Vault Bank checking account.
for date in sample(list(datesrange((2012,7,10), (2015,5,1))), 10):
  amount = Decimal(randint(2000,10000))/100
  checking1042.add(transaction(date=date, amount=amount, label=choice([
    u'TWX*%i*INSTYLE 877-312-1121 NY' % randint(10000,99999),
    u'TME*%i*INSTYLE 855-226-0424 NY' % randint(10000,99999),
    u'TWX*%i*INSTYLE 800-882-6317 NY' % randint(10000,99999),
    u'CHECK CRD PUR RTRN %s PAYPAL *6PM COM 402-935-7733 NV XXXXXXXXXXXX4933'
    u' %i' % (date, randint(10000,99999)),
    u'CHECK CRD PUR RTRN %s ZAP*6PM.COM 888-676-2660 NV XXXXXXXXXXXX4933'
    u' %i' % (date, randint(10000,99999))])))
# Purchases via Crispy Bills Bank credit card.
for date in sample(list(datesrange((2013,12,1), (2015,5,1))), 15):
  amount = Decimal(randint(2000,10000))/100
  master8385.add(transaction(date=date, amount=-amount, label=choice([
    u'TWX*%i*INSTYLE 877-312-1121 NY' % randint(10000,99999),
    u'TME*%i*INSTYLE 855-226-0424 NY' % randint(10000,99999),
    u'TWX*%i*INSTYLE 800-882-6317 NY' % randint(10000,99999),
    u'ZAP*6PM.COM 888-676-2660 NV'])))

#
# 7 ELEVEN
#
seed(85941)
for date in sample(list(datesrange((2013,5,1), (2015,5,1))), 20):
  amount = Decimal(randint(2000,4000))/100
  checking1042.add(transaction(date=date, amount=-amount, label=choice([
    u'PURCHASE AUTHORIZED ON %s 7-ELEVEN %i MARS VEGAS MA CARD 4933' \
    % (date, randint(10000,99999)),
    u'POS PURCHASE - %s MACH ID 000000 7 ELEVEN MARS VEGAS MA 4933 %i' \
    % (date, randint(10000,99999))])))

#
# ABEBOOKS.COM
#
seed(17040)
for date in sample(list(datesrange((2012,7,1), (2013,12,1))), 20):
  amount = Decimal(randint(500,2000))/100
  account = randacc(date, anytags={'wv', 'cb'})
  account.add(transaction(date=date, amount=-amount, label=choice([
    u'CHECK CRD PURCHASE %s ABEBOOKS.COM 800-315-5335 WA XXXXXXXXXXXX1234 %i' \
    % (date, randint(10000,99999)),
    u'ABEBOOKS.COM 800-315-5335 WA'])))

#
# ALDI
#
seed(13383)
for date in sample(list(datesrange((2013,12,1), (2015,5,1))), 20):
  amount = Decimal(randint(5000,10000))/100
  account = randacc(date, anytags={'wv', 'cb'})
  account.add(transaction(date=date, amount=-amount, label=choice([
    u'PURCHASE AUTHORIZED ON %s ALDI 75432 1234 MARS VEGAS MA P%i CARD 4933' \
    % (date, randint(10000,99999)),
    u'POS PURCHASE - %s MACH ID 000000 ALDI 75432 1234 MARS VEGAS MA 4933 %i' \
    % (date, randint(10000,99999))])))

#
# AWESOME DIGITAL SERVICES
#
seed(28943)
for date in sample(list(datesrange((2014,8,1), (2015,5,1))), 40):
  amount = Decimal(randint(100,1000))/100
  awesome1875.add(transaction(date=date, amount=-amount,
    label=u'AWESOME DIGITAL SEATTLE WA'))

#
# AWESOME WEB SERVICES
#
seed(56192)
for date in sample(list(datesrange((2014,7,1), (2015,5,1))), 10):
  amount = Decimal(randint(2000,4000))/100
  checking1042.add(transaction(date=date, amount=-amount, label=choice([
    u'PURCHASE AUTHORIZED ON %s AWESOME WEB SERVICE AWS.AWESOME.CO WA S%i '
    u'CARD 4933' % (date, randint(10000,99999)),
    u'CHECK CRD PURCHASE %s AWESOME WEB SERVICE AWS.AWESOME.CO WA '
    u'XXXXXXXXXXXX4933 %i' % (date, randint(10000,99999))])))

#
# AMTRAK
#
seed(56192)
for date in sample(list(datesrange((2014,3,1), (2014,7,1))), 20):
  amount = Decimal(randint(50,150))
  master8385.add(transaction(date=date, amount=-amount,
    label=u'AMTRAK .%i DC' % randint(100000,999999)))

#
# ARBORETUM
#
seed(44417)
for date in sample(list(datesrange((2013,12,1), (2015,5,1))), 5):
  amount = Decimal(randint(10,30))
  master8385.add(transaction(date=date, amount=-amount, label=choice([
    u'POS PURCHASE - %s MACH ID 000000 MARS ARBORETU MARS VEGAS MA 8385 %i' \
    % (date, randint(100000,999999)),
    u'MARS ARBORETUM MARS VEGAS MA'])))

#
# AT&T
#
seed(64198)
for date in sample(list(datesrange((2012,7,10), (2015,5,1))), 50):
  amount = Decimal(randint(30,50))
  checking1042.add(transaction(date=date, amount=-amount, label=choice([
    u'PURCHASE AUTHORIZED ON %s VESTA *AT&T 866-608-3007 OR S%i CARD 4933' \
    % (date, randint(100000,999999)),
    u'VESTA *AT&T 866-608-3007 OR'])))

#
# CAFE
#
seed(82315)
for date in sample(list(datesrange((2012,7,1), (2015,5,1))), 50):
  amount = Decimal(randint(1000,5000))/100
  account = randacc(date, anytags={'wv', 'cb'})
  account.add(transaction(date=date, amount=-amount, label=choice([
    u'CAFE BRAZIL MARS VEGAS MA',
    u'UDIPI CAFE HOUSTON TX',
    u'COFFEE HOUSE CAFE - DA MARS VEGAS MA',
    u'METEOR CAFE%i MARS VEGAS MA' % randint(10000,99999),
    u'CHECK CRD PURCHASE %s METEOR CAFE1234 MARS VEGAS MA XXXXXXXXXXXX1234 %i'\
    % (date, randint(100000,999999))])))

#
# CONTACTS
#
seed(53637)
for date in sample(list(datesrange((2012,7,10), (2015,5,1))), 10):
  amount = Decimal(randint(50,150))
  checking1042.add(transaction(date=date, amount=-amount, label=choice([
    u'ACL*CONTACT LEN INTRNT 800-822-6853 OH',
    u'COASTALCONTACTS 604-6691555 CA'])))

#
# CUSTOM HOUSE
#
seed(93632)
for date in sample(list(datesrange((2013,3,1), (2014,2,1))), 5):
  amount = Decimal(randint(10000,30000))/100
  account = randacc(date, anytags={'wv', 'cb'})
  account.add(transaction(date=date, amount=-amount, label=
    u'CUSTOM HOUSE LTD CUSTOM FX %i LEELA TURANGA' % randint(100000,999999)))

#
# DPS
#
seed(54927)
for date in sample(list(datesrange((2014,6,1), (2015,5,1))), 5):
  amount = Decimal(randint(2000,8000))/100
  account = randacc(date, anytags={'wv', 'cb'})
  account.add(transaction(date=date, amount=-amount,
    label=u'TX DPS DL OFFICE AUSTIN TX'))

#
# GEICO
#
seed(32640)
for date in sample(list(datesrange((2013,5,1), (2015,5,1))), 3):
  amount = Decimal(randint(30000,70000))/100
  account = randacc(date, anytags={'wv', 'cb'})
  account.add(transaction(date=date, amount=-amount,
    label=u'GEICO *AUTO MACON DC'))

#
# HOME DEPOT
#
seed(27219)
for date in sample(list(datesrange((2012,11,1), (2015,5,1))), 10):
  amount = Decimal(randint(1000,3000))/100
  account = randacc(date, anytags={'wv', 'cb'})
  account.add(transaction(date=date, amount=-amount, label=choice([
    u'PURCHASE AUTHORIZED ON %s THE HOME DEPOT MARS VEGAS MA P%i CARD 1234' \
    % (date, randint(100000,999999)),
    u'POS PURCHASE - %s MACH ID 000000 THE HOME DEPOT MARS VEGAS MA 1234 %i' \
    % (date, randint(100000,999999)),
    u'THE HOME DEPOT %i MARS VEGAS MA' % randint(1000,9999)])))

#
# INSURANCE
#
seed(74679)
for date in sample(list(datesrange((2012,11,1), (2015,5,1))), 10):
  amount = Decimal(randint(10000,70000))/100
  account = randacc(date, anytags={'wv', 'cb'})
  account.add(transaction(date=date, amount=-amount, label=choice([
    u'TRAVEL INSURANCE POLICY RICHMOND VA',
    u'TRAVEL INSURANCE POLICY 800-729-6021 VA'
    u'CHECK CRD PURCHASE %s PSI INSURANCE 000-0000000 VA XXXXXXXXXXXX1234 %i' \
    % (date, randint(100000,999999))])))

#
# ZOIDBERG
#
seed(25061)
for date in sample(list(datesrange((2013,12,1), (2015,5,1))), 10):
  amount = Decimal(randint(10000,50000))/100
  account = randacc(date, anytags={'wv', 'cb'})
  account.add(transaction(date=date, amount=-amount, label=choice([
    u'JOHN A. ZOIDBERG M.D. MARS VEGAS MA',
    u'CHECK CRD PURCHASE %s JOHN A. ZOIDBERG M.D. MARS VEGAS MA XXXXXXXXXX1234'
    u' %i' % (date, randint(100000,999999))])))

#
# BENDER'S CAR REPAIR
#
seed(59270)
# Payments via unsorted checks.
for date in sample(list(datesrange((2013,6,1), (2015,5,1))), 5):
  amount = Decimal(randint(300,2000))
  checking1042.add(transaction(date=date, amount=-amount,
    label=u'%i CHECK' % randint(1100,1200)))

#
# NINTENDO
#
seed(17920)
for date in sample(list(datesrange((2012,7,1), (2015,5,1))), 20):
  amount = Decimal(randint(1000,3000))/100
  account = randacc(date, anytags={'wv', 'cb'})
  account.add(transaction(date=date, amount=-amount, label=choice([
    u'NINTENDO OF EUROPE NIN.3DS.WIIU DEU',
    u'PUR INTL %s NINTENDO OF EUROPE NIN.3DS.WIIU DF XXXXXXXXXXX1234 %i' \
    % (date, randint(100000,999999))])))

#
# OCIUS
#
seed(57920)
for i in xrange(35):
  date = datetime(2012,7,15) + timedelta(days=30*i)
  amount = Decimal(900)
  checking1042.add(transaction(date=date, amount=-amount,
    label=u'OCIUS ACH PMT %i LEELA TURANGA' % randint(100000,999999)))

#
# REI
#
seed(11447)
for date in sample(list(datesrange((2014,4,1), (2015,5,1))), 5):
  amount = Decimal(randint(5000,30000))/100
  account = randacc(date, anytags={'wv', 'cb'})
  account.add(transaction(date=date, amount=-amount,
    label=u'REI COM SUMNER WA'))

#
# RELIANT
#
seed(82347)
for i in xrange(35):
  date = datetime(2012,7,12) + timedelta(days=30*i)
  amount = Decimal(randint(3000,7000))/100
  checking1042.add(transaction(date=date, amount=-amount, label=choice([
    u'BILL PAY RELIANT ENERGY R ON-LINE XXXX%i ON %s' \
    % (randint(10000,99999), date),
    u'RELIANT ENERGY %i LEELA TURANGA' % randint(100000,999999)])))

#
# SEPHORA
#
seed(38064)
for date in sample(list(datesrange((2014,11,1), (2015,5,1))), 20):
  amount = Decimal(randint(500,3000))/100
  account = randacc(date, anytags={'wv', 'cb'})
  account.add(transaction(date=date, amount=-amount,
    label=u'SEPHORA.COM 877-SEPHORA CA'))

#
# SPROUTS
#
seed(75751)
for date in sample(list(datesrange((2012,7,1), (2015,5,1))), 160):
  amount = Decimal(randint(4000,16000))/100
  account = randacc(date, anytags={'wv', 'cb'})
  account.add(transaction(date=date, amount=-amount, label=choice([
    u'SPROUTS FARMERS MARK MARS VEGAS MA',
    u'POS PURCHASE - %s MACH ID 00000 SPROUTS FARMERS MKT#99 MARS VEGAS MA %i'\
    % (date, randint(100000,999999)),
    u'PURCHASE %s SPROUTS FARMERS MA MARS VEGAS MA XXXXXXXXXXXX1234 %i' \
    % (date, randint(100000,999999)),
    u'PURCHASE AUTHORIZED ON %s SPROUTS FARMERS MKT#99 MARS VEGAS MA P%i' \
    % (date, randint(100000,999999))])))

#
# UNIVERSAL STUDIOS
#
seed(38064)
for date in sample(list(datesrange((2014,7,1), (2014,9,1))), 5):
  amount = Decimal(randint(2000,6000))/100
  account = randacc(date, anytags={'wv', 'cb'})
  account.add(transaction(date=date, amount=-amount,
    label=u'UNIVERSAL STUDIOS TICK UNIVERSAL CIT CA'))

#
# "NAMASTE AWAY" YOGA CLUB
#
seed(46335)
for date in sample(list(datesrange((2014,8,1), (2015,5,1))), 5):
  amount = Decimal(randint(2000,6000))/100
  account = randacc(date, anytags={'wv', 'cb'})
  account.add(transaction(date=date, amount=-amount,
    label=u'NAMASTE AWAY CLUB MARS VEGAS MA'))

#
# PLANET EXPRESS SALARY
#
seed(59385)
for i in xrange(34):
  date = datetime(2012,7,23) + timedelta(days=30*i)
  amount = Decimal(3000)
  checking1042.add(transaction(date=date, amount=amount, label=choice([
    u'PLANET EXPRESS DIR DEP %s %i FRY,PHILLIP' \
    % (date, randint(100000,999999)),
    u'PLANET EX DIRECT PAY %s PHILLIP FRY' % randint(100000,999999)])))

#
# YOSEMITE RETAIL STORE
#
seed(16969)
for date in sample(list(datesrange((2014,7,1), (2014,9,1))), 5):
  amount = Decimal(randint(1000,3000))/100
  account = randacc(date, anytags={'wv', 'cb'})
  account.add(transaction(date=date, amount=-amount,
    label=u'YOSEMITE VLG RETAIL 209-372-1245 CA'))

#
# Shop purchases.
#

BOOKS = [
  [u'The Art of', u'The Structure of', u'Little Book of', u'The Elements of'],
  [u'', u'Secret', u'Intelligent', u'Stupid', u'Magic', u'Mindful', u'Divine'],
  [u'Optimization', u'Mathematics', u'Cooking', u'Design', u'Meditation'],
  [u'', u'Theory', u'Practice', u'(4th Edition)']]
CLOTHES = [
  [u'', u'Fitted', u'Zip-Up', u'Yoga', u'Denim', u'Light',u'Outdoor',u'Fancy'],
  [u'V-Neck', u'Racerback', u'Coated', u'Sweat', u'Waist', u'Long Sleeve'],
  [u'Tank', u'Top', u'Pants', u'Hoodie', u'Shirt', u'Socks', u'Jacket'],
  [u'', u'XS', u'S', u'M', u'L', u'XL']]
DRUGS = [
  [u'', u'Instant', u'Splendid', u'Strong', u'Mild', u'Exceptional',u'Mom\'s'],
  [u'Nasal', u'Oral', u'Throat', u'Limbs', u'Back', u'Liver', u'Eye', u'Head'],
  [u'Pain', u'Congestion', u'Soreness', u'Itchiness', u'Explosion'],
  [u'Relief', u'Treatment', u'Killer', u'Remedy'],
  [u'Pills', u'Spray', u'Lozenges', u'Suppository', u'Injections']]
ELECTR = [
  [u'', u'Wireless', u'Handheld', u'Mobile', u'Smart', u'Flying', u'Sneaky'],
  [u'Monitor', u'Headphones', u'Phone', u'Laptop', u'Camera', u'Speakers'],
  [u'', u'Charger', u'Adapter', u'Cable', u'Teleporter', u'Replicator']]
FOOD = [
  [u'', u'', u'Natural', u'Organic', u'Powdered', u'Sun-Dried', u'Canned'],
  [u'', u'', u'', u'', u'', u'Fat-Free', u'Gluten-Free', u'Parasite-Free'],
  [u'', u'Chocolate', u'Apple', u'Banana', u'Potato', u'Neptunian', u'Brain'],
  [u'Cookie', u'Ice Cream', u'Syrup', u'Chips', u'Pie', u'Slug', u'Frog']]
GAMES = [
  [u'', u'', u'Return of the', u'Super', u'Ultimate', u'Angry', u'Raging'],
  [u'', u'Zombie', u'Mutant', u'Aliens', u'Storm Trooper', u'Hamster'],
  [u'Apocalypse', u'Carnage', u'BBQ', u'Tennis', u'Racing', u'Football'],
  [u'', u'in Wonderland', u'from Outer Space', u'under the Sea', u'Plus'],
  [u'(Playstation 3)', u'(Nintendo 3DS)', u'(Vita)', u'(Wii)', u'(PC DVD)']]
GROW = [
  [u'', u'Organic', u'Indoor', u'Office', u'Beginner\'s',u'Miracle',u'Mom\'s'],
  [u'Marijuana', u'Dill', u'Venus Fly Trap', u'Poison Ivy', u'Orchid'],
  [u'Growing Kit', u'Seeds', u'Plant', u'in a Pot', u'Hydroponics Kit']]
HOUSEHOLD = [
  [u'', u'Multi-Purpose', u'Do-It-Yourself', u'Enchanted', u'Mom\'s'],
  [u'Carpet', u'Closet', u'Dishes', u'Fridge', u'Machine Gun', u'Robot'],
  [u'Polish',u'Stain Remover',u'Freshener',u'Organizer',u'Repair Kit',u'Oil']]
HYGIENE = [
  [u'', u'Organic', u'Natural',u'Tibetan',u'Mineral',u'Radioactive',u'Mom\'s'],
  [u'Tail', u'Nails', u'Eye', u'Claws', u'Body', u'Face',u'Tentacle',u'Teeth'],
  [u'Cleanser', u'Polish', u'Enlarger', u'Lotion', u'Moisturizer',u'Softener']]
KITCHEN = [
  [u'', u'', u'Mom\'s', u'Mechanical', u'Electrical', u'Manual', u'Automatic'],
  [u'Vegetable', u'Slow', u'Meat', u'Seafood', u'Pressure', u'Fruit'],
  [u'Chopper', u'Cooker', u'Grinder', u'Slicer', u'Steamer', u'Blender']]
OTHER = [
  [u'', u'Magic', u'Surprise', u'Rainbow', u'Reusable',u'Curling',u'Exotic'],
  [u'Holiday', u'Birthday', u'Treasure', u'Space', u'Party', u'Scientific'],
  [u'Journal', u'Pencil', u'Lockpick', u'Ribbon', u'Map', u'Bag', u'Duster']]
OUTDOOR = [
  [u'Tactical', u'Outdoor', u'Survival', u'Wilderness', u'Hillbilly'],
  [u'Fire Starter', u'Tent', u'Knife', u'Cup',u'Chain Saw',u'Pot',u'Backpack'],
  [u'', u'', u'', u'', u'Repair Kit', u'Parts', u'Case', u'Holder']]
WEIGHT = [
  [u'Free Weights', u'Barbell', u'Dumbbell'],
  [u'Standard', u'Olympic'],
  [u'1.25-Pounds', u'2.5-Pounds', u'5-Pounds', u'10-Pounds', u'25-Pounds'],
  [u'Plate'],
  [u'', u'(Black)', u'(Silver)']]
YOGA = [
  [u'', u'Hatha', u'Jnana', u'Bhakti', u'Karma', u'Laya', u'Raja', u'Tantra'],
  [u'Yoga'],
  [u'Blocks', u'Chalk', u'Illustrated', u'Reference Manual', u'Mat', u'Strap']]

def add_random_order(shopname, date, itemwords, paymtd, acclabel, manchance):
  items = [item(label=label, price=price, url=itemurl(label,price,shopname))
           for i, price, label in zip(xrange(randint(1,5)),
             iter(lambda: Decimal(randint(100,2000))/100, None),
             iter(lambda: randwords(choice(itemwords)), None))]
  discount = -(sum(i.price for i in items) * randint(0,50) / 100
              ).quantize(Decimal('.01'), rounding=ROUND_UP)
  shipping = Decimal(randint(0, 2000))/100
  tax = ((sum(i.price for i in items) + discount + shipping)
         * randint(0,20) / 100
        ).quantize(Decimal('.01'), rounding=ROUND_UP)
  ordersum = sum(i.price for i in items) + discount + shipping + tax
  order = FakeOrder(id=str(randint(100000,999999)), date=date,
                    discount=discount, shipping=shipping, tax=tax)
  order.add_items(*items)
  allaccs = matchingaccs(date, alltags={shopname, 'auto'})
  if random() < manchance:
    allaccs += matchingaccs(date, alltags={shopname, 'manual'})
  payaccs = sample(allaccs, randint(1,len(allaccs)))
  payamts = randsum(int(100*ordersum), len(payaccs))
  for account, amount100 in zip(payaccs, payamts):
    amount = Decimal(amount100)/100
    account.add(transaction(date=date, amount=-amount, label=acclabel(date)))
    order.add_payments(payment(date=date,amount=amount,method=paymtd(account)))
  shop = globals()[shopname]
  shop.add(order)

#
# AWESOME STUFF
#
seed(82630)
for date in sample(list(datesrange((2012,7,1), (2015,5,1))), 250):
  add_random_order(shopname='awesome', date=date, manchance=0.2,
    itemwords=[BOOKS, CLOTHES, DRUGS, ELECTR, FOOD, GAMES, GROW, HOUSEHOLD,
               HYGIENE, KITCHEN, OTHER, OUTDOOR, WEIGHT, YOGA],
    paymtd=paymethod, 
    acclabel=lambda d: choice([
      u'PURCHASE %s AWESOME.COM AWSM.COM/BILL WA XXXXXXXXXXXX1234 %i' \
      % (d, randint(100000,999999)),
      u'PURCHASE %s AWESOME MKTPLACE PM AWSM.COM/BILL WA XXXXXXXXXX1234 %i' \
      % (d, randint(100000,999999)),
      u'AWESOME MARKETPLACE SEATTLE WA',
      u'AWESOME RETAIL SEATTLE WA']))
seed(46460)
for date in sample(list(datesrange((2012,7,1), (2015,5,1))), 5):
  amount = Decimal(randint(10000,30000))/100
  account = randacc(date, alltags={'awesome', 'auto'})
  account.add(transaction(date=date, amount=amount, label=choice([
      u'RETURN %s AWESOME.COM AWSM.COM/BILL WA XXXXXXXXXXXX1234 %i' \
      % (date, randint(100000,999999)),
      u'RETURN %s AWESOME MKTPLACE PM AWSM.COM/BILL WA XXXXXXXXXX1234 %i' \
      % (date, randint(100000,999999)),
      u'AWESOME MARKETPLACE SEATTLE WA',
      u'AWESOME RETAIL SEATTLE WA'])))

#
# ITCHY BACK
#
seed(76605)
for date in sample(list(datesrange((2012,7,1), (2015,5,1))), 50):
  add_random_order(shopname='itchyback', date=date, manchance=0.2,
    itemwords=[CLOTHES, HOUSEHOLD, HYGIENE, KITCHEN],
    paymtd=lambda a: u'DEFAULT PAYMENT',
    acclabel=lambda d: choice([
      u'PURCHASE %s ITCHY.COM 888-835-1719 NY XXXXXXXXXXXX1234 %i' \
      % (d, randint(100000,999999)),
      u'ITCH.COM 888-835-1719 NY']))
seed(69446)
for date in sample(list(datesrange((2012,7,1), (2015,5,1))), 5):
  amount = Decimal(randint(10000,30000))/100
  account = randacc(date, alltags={'itchyback', 'auto'})
  account.add(transaction(date=date, amount=amount, label=choice([
      u'RETURN %s ITCHY.COM 888-835-1719 NY XXXXXXXXXXXX1234 %i' \
      % (date, randint(100000,999999)),
      u'ITCH.COM 888-835-1719 NY'])))

#
# MEGA RAGS
#
seed(57637)
for date in sample(list(datesrange((2012,7,1), (2015,5,1))), 50):
  add_random_order(shopname='megarags', date=date, manchance=0.2,
    itemwords=[CLOTHES, HOUSEHOLD, HYGIENE, KITCHEN],
    paymtd=paymethod, 
    acclabel=lambda d: choice([
      u'PURCHASE %s AWS*MEGARAGS.COM AWSM.COM/BILL WA XXXXXXXXXXXX1234 %i' \
      % (d, randint(100000,999999)),
      u'AWS*MEGARAGS.COM AWSM.COM/BILL WA']))
seed(62693)
for date in sample(list(datesrange((2012,7,1), (2015,5,1))), 5):
  amount = Decimal(randint(10000,30000))/100
  account = randacc(date, alltags={'megarags', 'auto'})
  account.add(transaction(date=date, amount=amount, label=choice([
      u'RETURN %s AWS*MEGARAGS.COM AWSM.COM/BILL WA XXXXXXXXXXXX1234 %i' \
      % (date, randint(100000,999999)),
      u'AWS*MEGARAGS.COM AWSM.COM/BILL WA'])))

#
# VIOLENTLY GORGEOUS
#
seed(45401)
# Purchases
for date in sample(list(datesrange((2012,7,1), (2015,5,1))), 50):
  add_random_order(shopname='viogor', date=date, manchance=0.2,
    itemwords=[CLOTHES, HYGIENE],
    paymtd=paymethod, 
    acclabel=lambda d: choice([
      u'VIOLENTLY GORGEOUS %i HOUSTON TX' % randint(1000,9999),
      u'VIOLENTLY GORGEOUS CATA %i OH' % randint(100000,999999),
      u'VIOLENTLY GORGEOUS PURCHASE']))
seed(62320)
for date in sample(list(datesrange((2012,7,1), (2015,5,1))), 5):
  amount = Decimal(randint(10000,30000))/100
  account = randacc(date, alltags={'viogor', 'auto'})
  account.add(transaction(date=date, amount=amount, label=choice([
      u'VIOLENTLY GORGEOUS %i HOUSTON TX' % randint(1000,9999),
      u'VIOLENTLY GORGEOUS RETURN'])))
