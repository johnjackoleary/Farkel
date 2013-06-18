####################
### Farkel Game ####
####################

import dice

dice_list = [dice.Dice() for i in range(6)]

for i in range(6):
	print dice_list[i].roll()
