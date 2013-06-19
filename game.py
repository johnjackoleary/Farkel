####################
### Farkel Game ####
####################

import dice
import player

dice_list = [dice.Dice() for i in range(6)]

### Set up players ###
number_of_players = input("How many players? ")
player_list = []
for i in range(number_of_players):
	player_list.append(player.Player(raw_input("What is player "+str(i+1)+"'s name?\n")))
	print player_list[0].name


### Set up variables for game play ###
game_over = False


##########
## GAME ##
##########
while not game_over:
	for i in range(6):
		print dice_list[i].roll()

	game_over = True
	for i in range(6):
		if dice_list[i].current_side != 6:
			game_over = False