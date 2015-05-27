module Hinance.User.Data (
  addtagged, canmerge, canxfer, patched,
  planfrom, planto, planned, slices, tagged
) where
import Hinance.User.Tag
import Hinance.User.Type
import Hinance.Bank.Type
import Hinance.Shop.Type
import Hinance.Currency
import Text.Printf
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
  | all' [TagAsset, Tag6PM]         = [TagExpense, TagClothes]
  | all' [TagAsset, Tag7Eleven]     = [TagExpense, TagCar, TagGas]
  | all' [TagAsset, TagAbeBooks]    = [TagExpense, TagBooks]
  | all' [TagAsset, TagAldi]        = [TagExpense, TagFood]
  | all' [TagAsset, TagAmtrak]      = [TagExpense, TagTravel, TagTransport]
  | all' [TagAsset, TagArboretum]   = [TagExpense, TagGoingOut]
  | all' [TagAsset, TagATnT]        = [TagExpense, TagPhone]
  | all' [TagAsset, TagAwesomeDgt]  = [TagExpense, TagMovies]
  | all' [TagAsset, TagAwesomeWeb]  = [TagExpense, TagHobby, TagProjects]
  | all' [TagAsset, TagBenderCar]   = [TagExpense, TagCar, TagCarMtn]
  | all' [TagAsset, TagCafe]        = [TagExpense, TagEatingOut]
  | all' [TagAsset, TagCheck]       = [TagIncome, TagOther]
  | all' [TagAsset, TagCheckDep]    = [TagIncome, TagOther]
  | all' [TagAsset, TagContacts]    = [TagExpense, TagDrugs]
  | all' [TagAsset, TagCstmHous]    = [TagExpense, TagTravel, TagTravHous]
  | all' [TagAsset, TagDPS]         = [TagExpense, TagCar, TagCarPaper]
  | all' [TagAsset, TagFee]         = [TagExpense, TagOther]
  | all' [TagAsset, TagGeico]       = [TagExpense, TagCar, TagCarInsur]
  | all' [TagAsset, TagHomeDepot]   = [TagExpense, TagHousehold]
  | all' [TagAsset, TagInstyle]     = [TagExpense, TagClothes]
  | all' [TagAsset, TagInsurance]   = [TagExpense, TagInsurance]
  | all' [TagAsset, TagNamaste]     = [TagExpense, TagHobby, TagYoga]
  | all' [TagAsset, TagNintendo]    = [TagExpense, TagGames]
  | all' [TagAsset, TagOcius]       = [TagExpense, TagRent]
  | all' [TagAsset, TagOpening]     = [TagIncome, TagOther]
  | all' [TagAsset, TagParking]     = [TagExpense, TagCar, TagParking]
  | all' [TagAsset, TagPlanetEx]    = [TagIncome, TagSalary]
  | all' [TagAsset, TagRei]         = [TagExpense, TagHobby, TagOutdoor]
  | all' [TagAsset, TagReliant]     = [TagExpense, TagEnergy]
  | all' [TagAsset, TagSephora]     = [TagExpense, TagHygiene]
  | all' [TagAsset, TagSprouts]     = [TagExpense, TagFood]
  | all' [TagAsset, TagUniversal]   = [TagExpense, TagTravel, TagTravGoOut]
  | all' [TagAsset, TagWvSecur]     = [TagAsset, TagOther]
  | all' [TagAsset, TagYosemRtl]    = [TagExpense, TagTravel, TagTravShop]
  | all' [TagAsset, TagZoidberg]    = [TagExpense, TagMedSvc]
  | otherwise            = []
  where all' = all (flip elem $ ts)

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

canmerge tsg tsng
  | both [TagAwesome, TagAwesome1875] = ng [TagAwesomeCard]
  | both [TagAwesome, TagAwsGiftAcc]  = ng [TagAwsGiftBnk]
  | both [TagAwesome, TagMaster8385]  = ng [TagCrispyBills]
  | both [TagAwesome, TagVisa4933]    = ng [TagWindyVault]
  | both [TagAwesome, TagVisa8394]    = ng [TagWindyVault]
  | both [TagAwesome, TagVisa4307]    = ng [TagWindyVault]
  | both [TagAwesome, TagVisa0375]    = ng [TagArpaBank]
  | both [TagAwesome, TagVisa3950]    = ng [TagBigApple]
  | both [TagItchyBack] && g [TagPayment] =
                                      (ng [TagMaster8385] || ng [TagVisa4307]
                                    || ng [TagVisa4933]   || ng [TagVisa0375])
  | both [TagMegaRags, TagMaster8385] = ng [TagCrispyBills]
  | both [TagMegaRags, TagVisa4933]   = ng [TagWindyVault]
  | both [TagMegaRags, TagVisa8394]   = ng [TagWindyVault]
  | both [TagMegaRags, TagVisa4307]   = ng [TagWindyVault]
  | both [TagVioGor, TagMaster8385]   = ng [TagCrispyBills]
  | both [TagVioGor, TagVioGor7260]   = ng [TagVioGorCard]
  | both [TagVioGor, TagVisa4933]     = ng [TagWindyVault]
  | both [TagVioGor, TagVisa8394]     = ng [TagWindyVault]
  | both [TagVioGor, TagVisa4307]     = ng [TagWindyVault]
  | otherwise                         = False
  where g = all (flip elem $ tsg)
        ng = all (flip elem $ tsng)
        both ts = g ts && ng ts

instance Taggable (Bank, BankAcc, BankTrans) where
  tagged (Bank{bid=b}, BankAcc{baid=a}, BankTrans{btlabel=l}) t
    | t==TagAsset        = True
    -- Banks
    | t==TagArpaBank     = a=~"^arpa:"
    | t==TagAwesomeCard  = b=="awesomecard"
    | t==TagAwsGiftBnk   = a=="awesomegift"
    | t==TagBigApple     = a=~"^bab:" || l=~"BIG APPLE BANK"
    | t==TagCrispyBills  = b=="crispybills"
    | t==TagVioGorCard   = b=="viogorcard"
    | t==TagWindyVault   = b=="windyvault"
    -- Accounts
    | t==TagAwesome1875  = a=="1875"
    | t==TagAwsGiftAcc   = a=="awesomegift"
    | t==TagCash         = a=="walletl" || a=="walletp" || a=="reserve"
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
    | t==TagAwesome      = l=~("(^| )AWESOME.COM"++
                               "|AWESOME (MKTPLACE|MARKETPLACE|RETAIL)")
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
    | t==TagItchyBack    = l=~"ITCHY?.COM"
    | t==TagMegaRags     = l=~"MEGARAGS"
    | t==TagNamaste      = l=~"NAMASTE AWAY"
    | t==TagNintendo     = l=~"NINTENDO"
    | t==TagOcius        = l=~"^OCIUS ACH PMT"
    | t==TagOpening      = l=~"OPENING (BALANCE|DEPOSIT)"
    | t==TagParking      = l=~"PARKING"
    | t==TagPlanetEx     = l=~("PLANET EXPRESS DIR DEP|PLANET EX DIRECT PAY")
    | t==TagRei          = l=~"REI COM SUMNER"
    | t==TagReliant      = l=~"RELIANT ENERGY"
    | t==TagSephora      = l=~"SEPHORA"
    | t==TagSprouts      = l=~"SPROUTS"
    | t==TagUniversal    = l=~"^UNIVERSAL STUDIOS"
    | t==TagVioGor       = l=~"VIOLENTLY GORGEOUS"
    | t==TagWvSecur      = l=~"WINDY VAULT FOPS SECUREDCAR"
    | t==TagYosemRtl     = l=~"YOSEMITE VLG RETAIL"
    | t==TagZoidberg     = l=~"ZOIDBERG"
    | otherwise          = False

taggedshop Shop{sid=s} t
  | t==TagAwesome   = s=~"awesome"
  | t==TagItchyBack = s=~"itchyback"
  | t==TagMegaRags  = s=~"megarags"
  | t==TagVioGor    = s=~"viogor"
  | otherwise       = False

instance Taggable (Shop, ShopOrder, String) where
  tagged (s, _, l) t = (taggedshop s t) || tagged' where
    tagged'
      | t==TagExpense  = l=="shipping" || l=="tax"
      | t==TagIncome   = l=="discount"
      | t==TagDiscount = l=="discount"
      | t==TagShipping = l=="shipping"
      | t==TagTax      = l=="tax"
      | otherwise      = False

instance Taggable (Shop, ShopOrder, ShopPayment) where
  tagged (s, _, ShopPayment{spmethod=m}) t = (taggedshop s t) || tagged' where
    tagged'
      | t==TagAwesome1875 = m=~"(Awesome.com Store Card|AWESOMEPLCC) 1875"
      | t==TagAwsGiftAcc  = m=="GIFT CARD"
      | t==TagMaster8385  = m=~"(MASTERCARD|MasterCard).* 8385$"
      | t==TagPayment     = m=="DEFAULT PAYMENT"
      | t==TagVioGor7260  = m=~"Violently.* 7260$"
      | t==TagVisa4933    = m=="VISA 4933"
      | t==TagVisa8394    = m=~"(VISA|Visa).* 8394$"
      | t==TagVisa4307    = m=~"(VISA|Visa).* 4307$"
      | t==TagVisa0375    = m=="VISA 0375"
      | t==TagVisa3950    = m=="VISA 3950"
      | t==TagIncome      = discount
      | t==TagDiscount    = discount
      | otherwise         = False
      where discount = m=~"eGift|Rebate|Refund Credit|Shipping.*Credit"

instance Taggable (Shop, ShopOrder, ShopItem) where
  tagged (s, _, ShopItem{silabel=l}) t = (taggedshop s t) || tagged' where
    tagged'
      | t==TagExpense   = True
      | t==TagBooks     = books
      | t==TagClothes   = clothes && not (outdoor || yoga)
      | t==TagDrugs     = drugs
      | t==TagElectronics = electr
      | t==TagFood      = food
      | t==TagGames     = games
      | t==TagGrow      = grow
      | t==TagHobby     = grow || outdoor || weight || yoga
      | t==TagHousehold = household
      | t==TagHygiene   = hygiene && not (drugs || household)
      | t==TagKitchen   = kitchen
      | t==TagOther     = other
      | t==TagOutdoor   = outdoor
      | t==TagWeight    = weight
      | t==TagYoga      = yoga
      | otherwise       = False
    books     = l=~"(^The (Art|Structure|Elements) of|Little Book)"
    clothes   = l=~"(Jacket|Hoodie|Pants|Shirt|Socks|Tank|Top)"
    drugs     = l=~"(Congestion|Explosion|Itchiness|Pain|Soreness)"
    electr    = l=~"(Monitor|Headphones|Phone|Laptop|Camera|Speakers)"
    food      = l=~"(Bacon|Chips|Cookie|Frog|Juice|Pie|Slug|Syrup)"
    games     = l=~"(Playstation|Nintendo|Vita|Wii|PC DVD)"
    grow      = l=~"(Growing|Seeds|Plant|in a Pot|Hydroponics)"
    household = l=~"(Carpet|Closet|Dishes|Fridge|Machine Gun|Robot)"
    hygiene   = l=~("(Body|Cleanser|Claws|Enlarger|Eye|Face|Lotion"++
                    "|Moisturizer|Nails|Polish|Softener|Tail|Teeth|Tentacle)")
    kitchen   = l=~"(Blender|Chopper|Cooker|Grinder|Slicer|Steamer)"
    other     = l=~"(Bag|Duster|Journal|Lockpick|Map|Pencil|Ribbon|Unknown)"
    outdoor   = l=~"(Tactical|Outdoor|Survival|Wilderness|Hillbilly)"
    weight    = l=~"(Free Weights|Barbell|Dumbbell)"
    yoga      = l=~"Yoga"

instance Patchable Shop where
  patched shops = (map patcheds shops) ++ [
    Shop {sid="awesome'", scurrency=USD, sorders=[
      refund 1411689600 2110 "MASTERCARD 8385",
      refund 1394841600 2616 "VISA 4933",
      refund 1376524800 2470 "VISA 4933",
      refund 1369785600 1557 "VISA 4933",
      refund 1359763200 2649 "VISA 8394"]},
    Shop {sid="itchyback'", scurrency=USD, sorders=[
      refund 1419897600 2554 "DEFAULT PAYMENT",
      refund 1391472000 1930 "DEFAULT PAYMENT",
      refund 1371859200 1635 "DEFAULT PAYMENT",
      refund 1369526400 1545 "DEFAULT PAYMENT",
      refund 1357430400 1182 "DEFAULT PAYMENT"]},
    Shop {sid="megarags'", scurrency=USD, sorders=[
      refund 1384300800 2538 "VISA 8394",
      refund 1371945600 2424 "VISA 8394",
      refund 1362873600 1591 "VISA 8394",
      refund 1355788800 1121 "VISA 8394",
      refund 1352764800 2083 "VISA 8394"]},
    Shop {sid="viogor'", scurrency=USD, sorders=[
      refund 1406505600 1245 "MASTERCARD 8385",
      refund 1391385600 2716 "VISA 4933",
      refund 1371600000 1845 "VISA 4933",
      refund 1371340800 1537 "VISA 4933",
      refund 1351555200 2656 "VISA 4933"]}]
    where
      refund t a m=ShopOrder {soid=printf "refund-%i" t, sotime=t, sotax=0,
                              soshipping=0, sodiscount=0,
        soitems=[ShopItem{silabel="Unknown refund", siprice= -a, siurl=""}],
        sopayments=[ShopPayment{sptime=t, spmethod=m, spamount= -a}]}
      patcheds s = s {sorders=map patchedo $ sorders s} where
        patchedo o@ShopOrder{soid=oi} = o {sopayments=concatMap patchedp $
                                                          sopayments o} where
          patchedp payment@ShopPayment{spamount=pa}
            | oi=="209302" && pa==2276 = split [112, 170, 239, 796, 959]
            | oi=="331038" && pa==2174 = split [75, 265, 523, 1311]
            | oi=="336473" && pa==2888 = split [37, 151, 742, 1958]
            | oi=="353794" && pa==3235 = split [253, 597, 1176, 1209]
            | oi=="604180" && pa==4070 = split [311, 3759]
            | oi=="850732" && pa==1282 = split [38, 151, 174, 366, 553]
            | oi=="910114" && pa==2198 = split [385, 1813]
            | otherwise = split [pa]
            where split parts = map (\x -> payment{spamount=x}) parts

instance Patchable Bank where
  patched banks = (map patchedb banks) ++ [Bank {bid="virtual", baccs=[
    BankAcc {baid="walletl", balabel="Leela's wallet", babalance=9600,
             bacurrency=USD, bacard=False, balimit=Nothing, bapaymin=Nothing,
             bapaytime=Nothing, batrans=[
      cashto   1430870400   9600]},
    BankAcc {baid="walletp", balabel="Phillip's wallet", babalance=2000,
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
      dep     1341600000 100000 "CASH OPENING BALANCE"]},
    BankAcc {baid="awesomegift",balabel="Awesome Stuff Gift Cards",babalance=0,
             bacurrency=USD, bacard=False, balimit=Nothing, bapaymin=Nothing,
             bapaytime=Nothing, batrans=[
      aws 1429920000  107, aws 1417132800  209, aws 1415145600  223,
      aws 1411257600 1847, aws 1408492800  424, aws 1408492800   73,
      aws 1404000000 5752, aws 1403913600   62, aws 1403481600  548,
      aws 1401148800   86, aws 1401062400  850, aws 1397001600 1604,
      aws 1396828800 2539, aws 1394150400  353, aws 1390521600    1,
      aws 1383868800  773, aws 1383609600 3816, aws 1382745600  188,
      aws 1381795200 1584, aws 1378598400 4778, aws 1377648000 2653,
      aws 1373846400  614, aws 1373760000  169, aws 1368230400  198,
      aws 1368057600  453, aws 1366675200 1904, aws 1363392000 1074,
      aws 1362873600 1757, aws 1362096000 2018, aws 1360886400  925,
      aws 1359417600 1265, aws 1357948800 3153, aws 1354924800  561,
      aws 1353542400  989, aws 1350604800 1733, aws 1345420800  943,
      aws 1345161600    9, aws 1342915200 3805,
      BankTrans {btlabel="OPENING BALANCE",
                 btamount=50040, bttime=1341600000}]},
    BankAcc {baid="bab:visa3950", balabel="Big Apple Bank: Visa 3950",
             babalance=0, bacurrency=USD, bacard=False, balimit=Nothing,
             bapaymin=Nothing, bapaytime=Nothing, batrans=[
      aws 1353542400 1550,
      aws 1345420800  221,
      aws 1345161600 1762,
      BankTrans {btlabel="OPENING BALANCE",
                 btamount=3533, bttime=1341600000}]}]}] where
    cashdep t a = BankTrans{bttime=t, btamount= -a,
                            btlabel="ATM CASH DEPOSIT"}
    cashwdw t a = BankTrans{bttime=t, btamount=a,
                            btlabel="ATM CASH WITHDRAWAL"}
    cashfrom t a = BankTrans{bttime=t, btamount= -a, btlabel="CASH TO CASH"}
    cashto t a = BankTrans{bttime=t, btamount=a, btlabel="CASH TO CASH"}
    dep t a l = BankTrans{bttime=t, btamount=a, btlabel=l}
    wdw t a l = BankTrans{bttime=t, btamount= -a, btlabel=l}
    aws t a = BankTrans{bttime=t, btamount= -a, btlabel="AWESOME MARKETPLACE"}
    patchedb b = b {baccs=map patcheda $ baccs b} where
      patcheda a = a {batrans=map patchedt $ batrans a} where
        patchedt trans@BankTrans{bttime=t, btlabel=l, btamount=m}
          | t==1416960000 && m==  -87300 = pl "BENDER'S CAR REPAIR"
          | t==1410480000 && m== -163500 = pl "BENDER'S CAR REPAIR"
          | t==1397865600 && m==  -42400 = pl "BENDER'S CAR REPAIR"
          | t==1381536000 && m==  -35400 = pl "BENDER'S CAR REPAIR"
          | t==1372809600 && m== -153000 = pl "BENDER'S CAR REPAIR"
          | otherwise = trans
            where pl x = trans{btlabel=x}

planfrom = 1406937600
planto = 1438387200
planned = recur ++ car ++ med ++ hhold ++ electronics ++ salary ++
          fun ++ hobbies ++ clothes ++ food ++ hygiene ++ other where
  recur = rent ++ energy ++ ins ++ phone
  car = carins ++ carpap ++ carmtn ++ gas
  med = dentist ++ drugs
  fun = movies ++ games
  hobbies = projects ++ yoga ++ outdoor ++ weight
  ins = insphillip ++ insleela
  rent = concat [chpair a t "Rent"
    [TagExpense, TagRent] [TagAsset, TagChecking1042] | (t, a) <-
    [(1438387200, 90000), (1435708800, 90000), (1433116800, 90000),
     (1430438400, 90000), (1427846400, 90000), (1425168000, 90000),
     (1422748800, 90000), (1420070400, 90000), (1417478400, 90000),
     (1414886400, 90000), (1412294400, 90000), (1409702400, 90000),
     (1407110400, 90000)]]
  insphillip = concat [chpair a t "Phillip's medical insurance"
    [TagExpense, TagInsurance] [TagAsset, TagChecking1042] | (t, a) <-
    [(1435881600, 50000), (1431648000, 50000),
     (1418083200, 44965), (1409270400, 46638)]]
  insleela = concat [chpair a t "Leela's medical insurance"
    [TagExpense, TagInsurance] [TagAsset, TagChecking1042] | (t, a) <-
    [(1437609600, 30000), (1433116800, 30000),
     (1420070400, 33519), (1415491200, 11975)]]
  phone = concat [chpair 7000 t "Mobile phones"
    [TagExpense, TagPhone] [TagAsset, TagChecking1042] | t <- monthly]
  energy = concat [chpair 5000 t "Electricity"
    [TagExpense, TagEnergy] [TagAsset, TagChecking1042] | t <- monthly]
  carins = concat [chpair a t "Car insurance"
    [TagExpense, TagCar, TagCarInsur] [TagAsset, TagChecking1042] | (t, a) <-
    [(1435708800, 40000), (1429401600, 42730)]]
  carpap = concat [chpair 2000 t "Car state inspection"
    [TagExpense, TagCar, TagCarPaper] [TagAsset, TagChecking1042]|t <- monthly]
  carmtn = concat [chpair 20000 t "Car maintenance"
    [TagExpense, TagCar, TagCarMtn] [TagAsset, TagChecking1042] | t <- monthly]
  gas = concat [chpair 2000 t "Gas"
    [TagExpense, TagCar, TagGas] [TagAsset, TagChecking1042] | t <- monthly]
  salary = concat [chpair 260000 t "Phillip's salary"
    [TagAsset, TagChecking1042] [TagIncome, TagSalary] | t <- monthly]
  food = concat [chpair 70000 t "Food"
    [TagExpense, TagFood] [TagAsset, TagChecking1042] | t <- monthly]
  dentist = concat [chpair 20000 t "Dental services"
    [TagExpense, TagMedSvc] [TagAsset, TagChecking1042] | t <- monthly]
  drugs = concat [chpair 2000 t "Drugs and contacts"
    [TagExpense, TagDrugs] [TagAsset, TagChecking1042] | t <- monthly]
  hhold = concat [chpair 5000 t "Household"
    [TagExpense, TagHousehold] [TagAsset, TagChecking1042] | t <- monthly]
  electronics = concat [chpair 3000 t "Electronics"
    [TagExpense, TagElectronics] [TagAsset, TagChecking1042] | t <- monthly]
  movies = concat [chpair 3000 t "Movies"
    [TagExpense, TagMovies] [TagAsset, TagChecking1042] | t <- monthly]
  games = concat [chpair 3000 t "Games"
    [TagExpense, TagGames] [TagAsset, TagChecking1042] | t <- monthly]
  projects = concat [chpair 3000 t "Projects"
    [TagExpense,TagHobby,TagProjects] [TagAsset,TagChecking1042] | t<-monthly]
  yoga = concat [chpair 5000 t "Yoga"
    [TagExpense,TagHobby,TagYoga] [TagAsset,TagChecking1042] | t<-monthly]
  outdoor = concat [chpair 5000 t "Outdoor"
    [TagExpense,TagHobby,TagOutdoor] [TagAsset,TagChecking1042] | t<-monthly]
  weight = concat [chpair 2000 t "Weight lifting"
    [TagExpense,TagHobby,TagWeight] [TagAsset,TagChecking1042] | t<-monthly]
  clothes = concat [chpair 10000 t "Clothes"
    [TagExpense, TagClothes] [TagAsset, TagChecking1042] | t <- monthly]
  hygiene = concat [chpair 10000 t "Hygiene"
    [TagExpense, TagHygiene] [TagAsset, TagChecking1042] | t <- monthly]
  other = concat [chpair 2000 t "Other"
    [TagExpense, TagOther] [TagAsset, TagChecking1042] | t <- monthly]
  monthly = [planfrom, planfrom+3600*2*365 .. planto]
  chpair amount time label tagspos tagsneg = [
    Change {camount=amount, ctime=time, clabel=label, ccur=USD, curl="",
            cgroup=(printf "Planned %s on %i" label time), ctags=tagspos},
    Change {camount= -amount, ctime=time, clabel=label, ccur=USD, curl="",
            cgroup=(printf "Planned %s on %i" label time), ctags=tagsneg}]
