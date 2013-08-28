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
def check_validity_of_selection(choosen_dice):
	if len(choosen_dice) == 0:
		return False

	for i in range(len(choosen_dice)):
		if choosen_dice[i] > 6 or choosen_dice[i] < 1:
			return False

	amounts_of_dice = [[0]*6,[0]*6]	# First list is values of dice_list. Second is from choosen dice.
	for i in range(len(dice_list)):
		if not dice_list[i].set_aside:
			amounts_of_dice[0][dice_list[i].current_side-1] += 1
	for i in range(len(choosen_dice)):
		amounts_of_dice[1][choosen_dice[i]-1] += 1

	for i in range(6):
		if amounts_of_dice[0][i] < amounts_of_dice[1][i]:
			return False

	return True;

## This needs to be seriously flushed out
def score_dice(choosen_dice):
	running_score = 0
	amounts_of_dice = [0]*6

	## Stores amount of each side show.
	for i in range(len(choosen_dice)):
		amounts_of_dice[choosen_dice[i]-1] += 1

	## Check for special patterns
	groupsOfThree = 0;
	groupsOfTwo = 0;
	straight = 0;
	for i in range(6):
		if amounts_of_dice[i] == 3:
			groupsOfThree += 1
		if amounts_of_dice[i] == 2:
			groupsOfTwo += 1
		if amounts_of_dice[i] == 1:
			straight += 1;
	# Add this in later
	if groupsOfThree == 2:
		pass
	elif groupsOfTwo == 3:
		pass
	elif straight == 6:
		pass

	for i in range(6):
		if amounts_of_dice[i] == 6:
			if i == 0:
				running_score += 1000*2
			else:
				running_score += (i+1)*100*2
			amounts_of_dice[i] = amounts_of_dice[i] - 6
		if amounts_of_dice[i] >= 3:
			if i == 0:
				running_score += 1000
			else:
				running_score += (i+1)*100
			amounts_of_dice[i] = amounts_of_dice[i] - 3

	running_score += 100*amounts_of_dice[0]
	running_score += 50*amounts_of_dice[4]


	return running_score

def choose_dice(dice_list):	# Sets aside any dice that are pulled out.
	
	valid_entry = False
	while not valid_entry:
		tempList = raw_input("Which dice would you like to pull out? ")
		dice_to_keep = map(int, tempList.split())
		valid_entry = check_validity_of_selection(dice_to_keep)
		if not valid_entry:
			print "I'm sorry, that is not a valid entry. Try again."


 	# Going to need a way to check that the choosen dice can be legally choosen... #
	for i in range(len(dice_to_keep)):
		for j in range(len(dice_list)):
			if dice_list[j].current_side == dice_to_keep[i] and not dice_list[j].set_aside:
				dice_list[j].set_aside = True
				break
	return dice_to_keep

def run_turn(player, starting_score):
	this_rounds_score = starting_score
	print player_list[player].name+"'s turn."

	print "\n=== Roll ==="

	dice_aside = 0
	for i in range(6):
		if not dice_list[i].set_aside:
			print dice_list[i].roll()
		else:
			dice_aside += 1
	if dice_aside > 0:
		print "--- Set Aside ---"
		for i in range(6):
			if dice_list[i].set_aside:
				print dice_list[i].current_side

	temp_score = score_dice(choose_dice(dice_list))
	this_rounds_score += temp_score

	if temp_score > 0:

		dice_remaining = 0
		for i in range(6):
			if not dice_list[i].set_aside:
				dice_remaining += 1

		if dice_remaining == 0:
			print "You must roll again for removing all dice. Good luck!"
			for i in range(6):
				dice_list[i].set_aside = False
			run_turn(player, this_rounds_score)
		else:
			if 0 == input("Type 1 to continue rolling, type 0 to stop. "):
				player_list[player].current_score += this_rounds_score
			else:
				run_turn(player, this_rounds_score)
	else:
		print "That's unfortunate."

current_player = 0
final_round = False
final_round_countdown = number_of_players	# Used to allow each player to get one more chance to play after someone gets 5000

###### Main Loop ######
while not game_over:
	## Loop for each turn
	run_turn(current_player, 0)
	print player_list[current_player].name+" has a total of "+str(player_list[current_player].current_score)+" points."

	## Check if a player has enough points to win
	if player_list[current_player].current_score >= 5000:
		final_round = True

	## Prepare everything for the next iteration
	if final_round:
		final_round_countdown -= 1
		if final_round_countdown <= 0:
			game_over = True

	current_player += 1
	current_player = current_player % number_of_players	## To cycle through the players

	for i in range(6):
		dice_list[i].set_aside = False


### Finish the Game ###
winning_player_idx = -1
top_score = 0
for i in range(number_of_players):
	if player_list[i].current_score > top_score:
		winning_player_idx = i
		top_score = player_list[i].current_score
	# Need to figure out how to handle a tie

print player_list[winning_player_idx].name+" wins with "+str(top_score)+" points!"







