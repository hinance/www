class FakeBank:
  def iter_accounts(self):
    #TODO
    return []
  def get_account(self, id_):
    #TODO
    return None
  def iter_history(self, account):
    #TODO
    return []

class FakeShop:
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

crispybills = FakeBank()
windyvault = FakeBank()
awesome = FakeShop()
awesomecard = FakeBank()
viogor = FakeShop()
viogorcard = FakeBank()
megarags = FakeShop()
itchyback = FakeShop()
