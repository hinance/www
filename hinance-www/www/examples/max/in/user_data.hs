module Hinance.User.Data (
  addtagged, canmerge, canxfer, patched,
  planfrom, planto, planned, slices, tagged
) where
import Hinance.User.Tag
import Hinance.User.Type
import Hinance.Bank.Type
import Hinance.Shop.Type
import Hinance.Currency

blue = "#337AB7"
cyan = "#5BC0DE"
green = "#5CB85C"
grey = "#777"
red = "#D9534F"
white = "#FFF"
yellow = "#F0AD4E"

addtagged _ = [] :: [Tag]
canxfer _ _ = False
canmerge _ _ = False

slices = [
  Slice {sname="Expenses", stags=[TagExpense], scategs=[
    SliceCateg {scname="Rent, Car and Recurring", scbg=red, scfg=white,
      sctags=[TagCar, TagEnergy, TagInsurance, TagPhone, TagRent,
              TagShipping, TagTax]},
    SliceCateg {scname="Food", scbg=yellow, scfg=white,
      sctags=[TagFood, TagEatingOut]},
    SliceCateg {scname="Medicine and Hygiene", scbg=green, scfg=white,
      sctags=[TagMedSvc, TagDrugs, TagHygiene]},
    SliceCateg {scname="Household and Electronics", scbg=cyan, scfg=white,
      sctags=[TagElectronics, TagHousehold, TagKitchen]},
    SliceCateg {scname="Clothes, Books, Fun and Travel", scbg=blue, scfg=white,
      sctags=[TagBooks, TagClothes, TagGames, TagGoingOut,
              TagHobby, TagMovies, TagTravel]},
    SliceCateg {scname="Other", scbg=grey, scfg=white,
      sctags=[TagOther]}]},

  Slice {sname="Hobbies", stags=[TagHobby], scategs=[
    SliceCateg {scname="Outdoor", scbg=green, scfg=white,
      sctags=[TagOutdoor]},
    SliceCateg {scname="Yoga", scbg=cyan, scfg=white,
      sctags=[TagYoga]},
    SliceCateg {scname="Weight Lifting", scbg=blue, scfg=white,
      sctags=[TagWeight]},
    SliceCateg {scname="Projects", scbg=yellow, scfg=white,
      sctags=[TagProjects]},
    SliceCateg {scname="Growing", scbg=red, scfg=white,
      sctags=[TagGrow]}]},

  Slice {sname="Car", stags=[TagCar], scategs=[
    SliceCateg {scname="Gas", scbg=green, scfg=white,
      sctags=[TagGas]},
    SliceCateg {scname="Insurance and Paperwork", scbg=cyan, scfg=white,
      sctags=[TagCarInsur, TagCarPaper]},
    SliceCateg {scname="Parking", scbg=blue, scfg=white,
      sctags=[TagParking]},
    SliceCateg {scname="Maintenance", scbg=yellow, scfg=white,
      sctags=[TagCarMtn]}]},

  Slice {sname="Travel", stags=[TagTravel], scategs=[
    SliceCateg {scname="Transport", scbg=green, scfg=white,
      sctags=[TagTransport]},
    SliceCateg {scname="Going Out", scbg=cyan, scfg=white,
      sctags=[TagTravGoOut]},
    SliceCateg {scname="Shopping", scbg=blue, scfg=white,
      sctags=[TagTravShop]},
    SliceCateg {scname="Housing", scbg=yellow, scfg=white,
      sctags=[TagTravHous]}]},

  Slice {sname="Income", stags=[TagIncome], scategs=[
    SliceCateg {scname="Salary", scbg=green, scfg=white, sctags=[TagSalary]},
    SliceCateg {scname="Discounts", scbg=blue,scfg=white,sctags=[TagDiscount]},
    SliceCateg {scname="Other", scbg=grey, scfg=white, sctags=[TagOther]}]},

  Slice {sname="Assets", stags=[TagAsset], scategs=[
    SliceCateg {scname="Cash", scbg=red, scfg=white,
      sctags=[TagCash]},
    SliceCateg {scname="Shopping Credit", scbg=yellow, scfg=white,
      sctags=[TagAmazon1875, TagAmzGiftAcc, TagVicSec7260]},
    SliceCateg {scname="Checking and Debit", scbg=green, scfg=white,
      sctags=[TagChecking1042, TagVisa0375, TagVisa9950]},
    SliceCateg {scname="Savings", scbg=cyan, scfg=white,
      sctags=[TagSavings2453]},
    SliceCateg {scname="Credit Cards", scbg=blue, scfg=white,
      sctags=[TagMaster8385, TagVisa8394]},
    SliceCateg {scname="Other", scbg=grey, scfg=white,
      sctags=[TagOther]}]},

  Slice {sname="All", stags=[], scategs=[
    SliceCateg {scname="Assets", scbg=green, scfg=white, sctags=[TagAsset]},
    SliceCateg {scname="Income", scbg=blue, scfg=white, sctags=[TagIncome]},
    SliceCateg {scname="Expenses",scbg=red,scfg=white,sctags=[TagExpense]}]}]

instance Taggable (Bank, BankAcc, BankTrans) where
  tagged _ _ = False

instance Taggable (Shop, ShopOrder, String) where
  tagged _ _ = False

instance Taggable (Shop, ShopOrder, ShopPayment) where
  tagged _ _ = False

instance Taggable (Shop, ShopOrder, ShopItem) where
  tagged _ _ = False

instance Patchable Shop where
  patched = id

instance Patchable Bank where
  patched = id

planfrom = 0
planto = 0
planned = []
