module Hinance.User.Tag where

data Tag = TagAsset | TagExpense | TagIncome
  -- Categories
  | TagBooks | TagCar | TagCarInsur | TagCarMtn | TagCarPaper | TagClothes
  | TagDiscount | TagDrugs | TagEatingOut | TagElectronics | TagEnergy
  | TagFood | TagGames | TagGas | TagGoingOut | TagGrow | TagHobby
  | TagHousehold | TagHygiene | TagInsurance | TagKitchen | TagMedSvc
  | TagMovies | TagOther | TagOutdoor | TagParking | TagPhone | TagProjects
  | TagRent | TagShipping | TagSalary | TagTax | TagTransport | TagTravel
  | TagTravGoOut | TagTravHous | TagTravShop | TagWeight | TagYoga
  deriving (Read, Show, Enum, Bounded, Eq, Ord)
