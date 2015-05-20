module Hinance.User.Data (
  addtagged, canmerge, canxfer, patched,
  planfrom, planto, planned, slices, tagged
) where
import Hinance.User.Tag
import Hinance.User.Type
import Hinance.Bank.Type
import Hinance.Shop.Type
import Hinance.Currency
import Text.Regex.TDFA

blue = "#337AB7"
cyan = "#5BC0DE"
green = "#5CB85C"
grey = "#777"
red = "#D9534F"
white = "#FFF"
yellow = "#F0AD4E"

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
      sctags=[TagAwesome1875, TagAwsGiftAcc, TagVioGor7260]},
    SliceCateg {scname="Checking and Debit", scbg=green, scfg=white,
      sctags=[TagChecking1042, TagVisa0375, TagVisa3950]},
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

addtagged ts
  | ast [Tag6PM]         = exp [TagClothes]
  | ast [Tag7Eleven]     = exp [TagCar, TagGas]
  | ast [TagAbeBooks]    = exp [TagBooks]
  | ast [TagAldi]        = exp [TagFood]
  | ast [TagAmtrak]      = exp [TagTravel, TagTransport]
  | ast [TagArboretum]   = exp [TagGoingOut]
  | ast [TagATnT]        = exp [TagPhone]
  | ast [TagAwesomeDgt]  = exp [TagMovies]
  | ast [TagAwesomeWeb]  = exp [TagHobby, TagProjects]
  | ast [TagBenderCar]   = exp [TagCar, TagCarMtn]
  | ast [TagCafe]        = exp [TagEatingOut]
  | ast [TagCheck]       = inc [TagOther]
  | ast [TagCheckDep]    = inc [TagOther]
  | ast [TagContacts]    = exp [TagDrugs]
  | ast [TagCstmHous]    = exp [TagTravel, TagTravHous]
  | ast [TagDPS]         = exp [TagCar, TagCarPaper]
  | ast [TagFee]         = exp [TagOther]
  | ast [TagGeico]       = exp [TagCar, TagCarInsur]
  | ast [TagHomeDepot]   = exp [TagHousehold]
  | ast [TagInstyle]     = exp [TagClothes]
  | ast [TagInsurance]   = exp [TagInsurance]
  | ast [TagNintendo]    = exp [TagGames]
  | ast [TagOcius]       = exp [TagRent]
  | ast [TagOpening]     = inc [TagOther]
  | ast [TagParking]     = exp [TagCar, TagParking]
  | ast [TagRei]         = exp [TagHobby, TagOutdoor]
  | ast [TagReliant]     = exp [TagEnergy]
  | ast [TagZoidberg]    = exp [TagMedSvc]
  | otherwise            = []
  where ast = all (flip elem $ ts) . (++) [TagAsset]
        exp = (++) [TagExpense]
        inc = (++) [TagIncome]

canxfer tsa tsb
  | a [TagCashDep, TagWindyVault]      = b [TagCashDep, TagCash]
  | a [TagCashWdw, TagWindyVault]      = b [TagCashWdw, TagCash]
  | a [TagOdftFr2453, TagChecking1042] = b [TagOdftTo1042, TagSavings2453]
  | a [TagCheck, TagChecking1042]      = b [TagPayment, TagMaster8385]
  | a [TagPaymentCrsp]                 = b [TagPayment, TagMaster8385]
  | a [TagPayment8394]                 = b [TagPayment, TagVisa8394]
  | a [TagXferFrSav, TagChecking1042]  = b [TagXferToChk, TagSavings2453]
  | a [TagXferToSav, TagChecking1042]  = b [TagXferFrChk, TagSavings2453]
  | a [TagPaymentAwsm]                 = b [TagPayment, TagAwesome1875]
  | a [TagPaymentVG]                   = b [TagPayment, TagVioGor7260]
  | a [TagCash, TagCash2Cash]          = b [TagCash, TagCash2Cash]
  | otherwise                          = False
  where a = all (flip elem $ tsa)
        b = all (flip elem $ tsb)

canmerge _ _ = False

instance Taggable (Bank, BankAcc, BankTrans) where
  tagged (Bank{bid=b}, BankAcc{baid=a}, BankTrans{btlabel=l}) t
    | t==TagAsset        = True
    -- Banks
    | t==TagArpaBank     = a=~"^arpa:"
    | t==TagAwesomeCard  = b=="awesomecard"
    | t==TagAwsGiftBnk   = a=="awesomegift"
    | t==TagBankOfMo     = a=~"^bom:" || l=~"BANK OF MORDOR"
    | t==TagCrispyBills  = b=="crispybills"
    | t==TagVioGorCard   = b=="viogorcard"
    | t==TagWindyVault   = b=="windyvault"
    -- Accounts
    | t==TagAwesome1875  = a=="1875"
    | t==TagAwsGiftAcc   = a=="awesomegift"
    | t==TagCash         = a=="walleta" || a=="walletd" || a=="reserve"
    | t==TagChecking1042 = a=="1042"
    | t==TagMaster8385   = a=="8385"
    | t==TagSavings2453  = a=="2453"
    | t==TagVioGor7260   = a=="7260"
    | t==TagVisa4933     = a=="1042" -- debit card
    | t==TagVisa8394     = a=="8394"
    | t==TagVisa4307     = a=="1042" -- debit card
    | t==TagVisa0375     = a=~"visa0375"
    | t==TagVisa3950     = a=~"visa3950"
    -- Transfers
    | t==TagCash2Cash    = l=="CASH TO CASH"
    | t==TagCashWdw      = l=~"^(ATM )?(CASH )?E?WITHDRAWAL"
    | t==TagCashDep      = l=~"^(ATM CASH )?DEPOSIT"
    | t==TagCheck        = l=~"^([0-9]+ )?CHECK( # [0-9]+)?$"
    | t==TagCheckDep     = l=~"^ATM CHECK DEPOSIT"
    | t==TagOdftFr2453   = l=~"^OVERDRAFT PROTECTION FROM.*2453$"
    | t==TagOdftTo1042   = l=~"^OVERDRAFT PROTECTION TO.*1042$"
    | t==TagPayment      = l=~"^(ONLINE )?(PAYMENT|PYMT)[, -]*(THANK YOU)?"
    | t==TagPaymentAwsm  = l=~"PAYMENT FOR AWS STORECARD|AWESOME CREDIT"
    | t==TagPayment8394  = l=~"TRANSFER.*TO (SECURED CARD|VISA).*X8394 "
    | t==TagPaymentCrsp  = l=~"^CRISPY CARD ONLINE PAYMENT"
    | t==TagPaymentVG    = l=~"CELESTIAL PAY"
    | t==TagXferFrChk    = l=~"ONLINE TRANSFER.* FROM .*CHECKING"
    | t==TagXferFrSav    = l=~"ONLINE TRANSFER.* FROM .*SAVINGS"
    | t==TagXferToChk    = l=~"ONLINE TRANSFER.* TO .*CHECKING"
    | t==TagXferToSav    = l=~"ONLINE TRANSFER.* TO .*SAVINGS"
    -- Labels
    | t==Tag6PM          = l=~"6PM.COM"
    | t==Tag7Eleven      = l=~"7[- ]ELEVEN"
    | t==TagAbeBooks     = l=~"ABEBOOKS.COM"
    | t==TagAldi         = l=~" ALDI "
    | t==TagAmtrak       = l=~"^AMTRAK"
    | t==TagArboretum    = l=~"ARBORETU"
    | t==TagATnT         = l=~"VESTA \\*AT&T"
    | t==TagAwesomeDgt   = l=~"AWESOME DIGITAL"
    | t==TagAwesomeWeb   = l=~"AWESOME WEB SERVICE"
    | t==TagBenderCar    = l=~"BENDER'S CAR REPAIR"
    | t==TagCafe         = l=~"CAFE"
    | t==TagContacts     = l=~"CONTACT(S| LEN)"
    | t==TagCstmHous     = l=~"CUSTOM HOUSE LTD"
    | t==TagDPS          = l=~"^TX DPS"
    | t==TagFee          = l=~" FEE( .*)?$"
    | t==TagGeico        = l=~"GEICO"
    | t==TagHomeDepot    = l=~"HOME DEPOT"
    | t==TagInstyle      = l=~"INSTYLE"
    | t==TagInsurance    = l=~"INSURANCE"
    | t==TagNintendo     = l=~"NINTENDO"
    | t==TagOcius        = l=~"^OCIUS ACH PMT"
    | t==TagOpening      = l=~"OPENING (BALANCE|DEPOSIT)"
    | t==TagParking      = l=~"PARKING"
    | t==TagRei          = l=~"REI COM SUMNER"
    | t==TagReliant      = l=~"RELIANT ENERGY"
    | t==TagZoidberg     = l=~"ZOIDBERG"
    | otherwise          = False where

instance Taggable (Shop, ShopOrder, String) where
  tagged _ _ = False

instance Taggable (Shop, ShopOrder, ShopPayment) where
  tagged _ _ = False

instance Taggable (Shop, ShopOrder, ShopItem) where
  tagged _ _ = False

instance Patchable Shop where
  patched = id

instance Patchable Bank where
  patched banks = (map patchedb banks) ++ [Bank {bid="virtual", baccs=[
    BankAcc {baid="walleta", balabel="Alison's wallet", babalance=9600,
             bacurrency=USD, bacard=False, balimit=Nothing, bapaymin=Nothing,
             bapaytime=Nothing, batrans=[
      cashto   1430870400   9600]},
    BankAcc {baid="walletd", balabel="Donnie's wallet", babalance=2000,
             bacurrency=USD, bacard=False, balimit=Nothing, bapaymin=Nothing,
             bapaytime=Nothing, batrans=[
      cashfrom 1430870400   9600,
      cashwdw  1428624000 142000, cashwdw  1427155200  88000,
      cashdep  1426204800  72000, cashwdw  1423958400 112000,
      cashwdw  1421452800 100000,
      wdw      1418417750   1000 "PARKING",
      wdw      1418099950   1000 "PARKING",
      wdw      1416918998   1000 "PARKING",
      cashdep  1416096000 146000,
      cashwdw  1412121600  74000, cashdep  1410393600 194000,
      cashdep  1409875200 156000, cashdep  1405900800 102000,
      wdw      1404395020   1000 "PARKING",
      cashdep  1402617600  94000, cashwdw  1400112000 150000,
      cashwdw  1394150400 168000, cashdep  1394150400  64000,
      wdw      1381851879   1000 "PARKING",
      cashwdw  1378684800 190000, cashdep  1369353600 156000,
      cashwdw  1361923200  26000, cashdep  1361491200  20000,
      cashdep  1360454400 200000, cashwdw  1359417600  22000,
      dep      1341600000 148600 "CASH OPENING BALANCE"]},
    BankAcc {baid="reserve", balabel="Cash reserve", babalance=100000,
             bacurrency=USD, bacard=False, balimit=Nothing, bapaymin=Nothing,
             bapaytime=Nothing, batrans=[
      dep     1341600000 100000 "CASH OPENING BALANCE"]}]}] where
    cashdep t a = BankTrans{bttime=t, btamount= -a,
                            btlabel="ATM CASH DEPOSIT"}
    cashwdw t a = BankTrans{bttime=t, btamount=a,
                            btlabel="ATM CASH WITHDRAWAL"}
    cashfrom t a = BankTrans{bttime=t, btamount= -a, btlabel="CASH TO CASH"}
    cashto t a = BankTrans{bttime=t, btamount=a, btlabel="CASH TO CASH"}
    dep t a l = BankTrans{bttime=t, btamount=a, btlabel=l}
    wdw t a l = BankTrans{bttime=t, btamount= -a, btlabel=l}
    patchedb b = b {baccs=map patcheda $ baccs b} where
      patcheda a = a {batrans=map patchedt $ batrans a} where
        patchedt trans@BankTrans{bttime=t, btlabel=l, btamount=m}
          | t==1416960000 && m== -183700 = pl "BENDER'S CAR REPAIR"
          | t==1410480000 && m==  -93900 = pl "BENDER'S CAR REPAIR"
          | t==1397865600 && m==  -41000 = pl "BENDER'S CAR REPAIR"
          | t==1381536000 && m==  -35400 = pl "BENDER'S CAR REPAIR"
          | t==1372809600 && m==  -42400 = pl "BENDER'S CAR REPAIR"
          | otherwise = trans
            where pl x = trans{btlabel=x}

planfrom = 0
planto = 0
planned = []
