module Hinance.User.Tag where

data Tag = TagAsset | TagExpense | TagIncome
  -- Accounts
  | TagAmazon1875 | TagAmzGiftAcc | TagCash | TagChecking1042 | TagMaster8385
  | TagSavings2453 | TagVicSec7260 | TagVisa4933 | TagVisa8394 | TagVisa4307
  | TagVisa0375 | TagVisa9950
  -- Categories
  | TagBooks | TagCar | TagCarInsur | TagCarMtn | TagCarPaper | TagClothes
  | TagDiscount | TagDrugs | TagEatingOut | TagElectronics | TagEnergy
  | TagFood | TagGames | TagGas | TagGoingOut | TagGrow | TagHobby
  | TagHousehold | TagHygiene | TagInsurance | TagKitchen | TagMedSvc
  | TagMovies | TagOther | TagOutdoor | TagParking | TagPhone | TagProjects
  | TagRent | TagShipping | TagSalary | TagTax | TagTransport | TagTravel
  | TagTravGoOut | TagTravHous | TagTravShop | TagWeight | TagYoga
  deriving (Read, Show, Enum, Bounded, Eq, Ord)
