####################
### Farkel Game ####
####################

import dice

dice_list = [dice.Dice() for i in range(6)]

print "How many players?"
number_of_players = input()

player_list = [p]

for i in range(6):
	print dice_list[i].roll()

game_over = False

while not game_over:
	
	print "hi"
	game_over = True