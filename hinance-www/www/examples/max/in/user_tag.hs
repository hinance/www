module Hinance.User.Tag where

data Tag = TagAsset | TagExpense | TagIncome
  -- Accounts
  | TagAwesome1875 | TagAwsGiftAcc | TagCash | TagChecking1042 | TagMaster8385
  | TagSavings2453 | TagVioGor7260 | TagVisa4933 | TagVisa8394 | TagVisa4307
  | TagVisa0375 | TagVisa3950
  -- Helpers
  | Tag6PM | Tag7Eleven | TagAbeBooks | TagAldi | TagAmtrak | TagArboretum
  | TagArpaBank | TagATnT | TagAwesome | TagAwesomeCard | TagAwesomeDgt
  | TagAwesomeWeb | TagAwsGiftBnk | TagBenderCar | TagBigApple | TagCafe
  | TagContacts | TagCrispyBills | TagCstmHous | TagDPS | TagFee | TagGeico
  | TagHomeDepot | TagInstyle | TagItchyBack | TagMegaRags | TagNamaste
  | TagNintendo | TagOcius | TagOpening | TagPlanetEx | TagRei | TagReliant
  | TagSephora | TagSprouts | TagUniversal | TagVioGor | TagVioGorCard
  | TagWindyVault | TagWvSecur | TagYosemRtl | TagZoidberg
  -- Transfers
  | TagCash2Cash | TagCashWdw | TagCashDep | TagCheck | TagCheckDep
  | TagOdftFr2453 | TagOdftTo1042 | TagPayment | TagPayment8394
  | TagPaymentAwsm | TagPaymentCrsp | TagPaymentVG | TagXferFrChk
  | TagXferFrSav | TagXferToChk | TagXferToSav
  -- Categories
  | TagBooks | TagCar | TagCarInsur | TagCarMtn | TagCarPaper | TagClothes
  | TagDiscount | TagDrugs | TagEatingOut | TagElectronics | TagEnergy
  | TagFood | TagGames | TagGas | TagGoingOut | TagGrow | TagHobby
  | TagHousehold | TagHygiene | TagInsurance | TagKitchen | TagMedSvc
  | TagMovies | TagOther | TagOutdoor | TagParking | TagPhone | TagProjects
  | TagRent | TagShipping | TagSalary | TagTax | TagTransport | TagTravel
  | TagTravGoOut | TagTravHous | TagTravShop | TagWeight | TagYoga
  deriving (Read, Show, Enum, Bounded, Eq, Ord)
