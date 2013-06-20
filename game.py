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

def choosing_dice(dice_list):	# Sets aside any dice that are pulled out.
	tempList = raw_input("Which dice would you like to pull out? ")
	dice_to_keep = map(int, tempList.split())
 
	for i in range(len(dice_to_keep)):
		for j in range(len(dice_list)):
			if dice_list[j].current_side == dice_to_keep[i]:
				dice_list[j].set_aside = True
				break

current_player = 0
while not game_over:
	print player_list[current_player].name+"'s turn."

	print "\n=== Roll ==="
	for i in range(6):
		if not dice_list[i].set_aside:
			print dice_list[i].roll()
		else:
			print dice_list[i].current_side

	choosing_dice(dice_list)



