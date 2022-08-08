# LRCDiceGame.py
#
# Created by Sarah Kerr for CS499
# Created on PyCharm Community 2021.2.1, Python version 3.9
#
# Console-based dice rolling game using playing chips that players pass left and right,
# or into a center pot, based on dice roll. The Player class constructs players and stores
# them in a list. The game loops through the list with each player taking their turn rolling
# dice. After each player's turn, a winner is checked by comparing the player's chips with
# the number of chips in the Center Pot.


#  Global variables
MIN_NUM_OF_PLAYERS = 3
MAX_NUM_OF_PLAYERS = 20
BEGINNING_CHIPS = 3  # Each player will start with 3 chips


class Player:
    """ Class for game player information.

    :param name: Player's name
    :type name: string
    :param chips: Number of chips player has.
    :type chips: int
    """
    def __init__(self, name, chips):
        """ Constructor for the Player class. """
        self.name = name
        self.chips = chips


class Dice:
    """ Class representing dice. """
    @staticmethod
    def roll():
        """ Rolling dice.

        :return: A random number 1-6.
        :rtype: int
        """
        import random as random_dice_num
        return random_dice_num.randint(1, 6)


class CenterPot:
    """ Class representing center pot holding discarded player chips.

    This will be compared to the total chips in play to determine if there's been
    a winner.

    :param chips: Chips in the center pot.
    :type chips: int
    """
    def __init__(self, chips):
        """ Constructor for the CenterPot class. """
        self.chips = chips


def main():
    """ Game setup here, then begin game loop. """
    display_rules()
    players = enter_num_of_players()
    list_of_players = create_player_list(players)

    total_chips = total_chips_in_play(players) # This will keep track of total chips in play

    center_pot = CenterPot(0)  # Initialize center pot to hold discarded chips, start at 0

    game_loop(list_of_players, total_chips, center_pot)


def display_rules():
    """ Opens and reads from .txt file. Displays error message if no such file """
    try:
        with open('LRCRules.txt') as f:
            rules = f.read()
            print(rules)
            print("")
        f.close()
    except IOError:
        print("Error opening file to read rules")


def enter_num_of_players():
    """ Takes number of players. Must be within min/max bounds. This will be used to create list of players.

    :return num_players: Total number of players in game.
    :rtype num_players: int
    """
    ask_for_players = "Enter the number of players " + str(MIN_NUM_OF_PLAYERS) + " to " + str(MAX_NUM_OF_PLAYERS)

    num_players = int(input(ask_for_players))
    while num_players < MIN_NUM_OF_PLAYERS or num_players > MAX_NUM_OF_PLAYERS:
        print("Error, incorrect number of players")
        num_players = int(input(ask_for_players))

    return num_players


def create_player_list(players):
    """ Adds player objects to a list, asking each player to enter their name first.

    :param players: Number of players in game. The program will loop through this many
        times asking for the player's names.
    :type players: int
    :return player_list: List holding the player objects.
    :rtype player_list: list of Player objects
    """
    player_list = []  # creates empty list to hold players
    for i in range(0, players):
        player_name = input("Enter your name: ")
        player_chips = BEGINNING_CHIPS
        player_list.append(Player(player_name, player_chips))

    return player_list


def total_chips_in_play(players):
    """ Takes the number of players and multiplies by number of starting to chips
    to get the total number of chips in play.

    :param players: Number of players in game.
    :type players: Int
    :return: Total chips in the game.
    :rtype: Int
    """
    return players * BEGINNING_CHIPS


def game_loop(list_of_players, total_chips, center_pot):
    """ Loops through each player to take their turn. Checks for winner after each turn and continues
    loop if there is no winner.

    :param list_of_players: List holding player objects
    :type list_of_players: List
    :param total_chips: Total chips in the game
    :type total_chips: Int
    :param center_pot: Center pot holding discarded chips
    :type center_pot: CenterPot object
    """
    winner = False  # Game starts with no winner

    while not bool(winner):
        for i in list_of_players:
            current_player_chips = check_chips(i)
            if current_player_chips > 0:
                # Number of turns is determined by how many chips the player has
                turns = determine_turns(current_player_chips)
                # Returns T or F if there is a winner after player's turn
                winner = take_turn(i, turns, list_of_players, center_pot, total_chips)

                if bool(winner):  # Game ends if there's a winner
                    break

            else:
                print("No chips. Turn skipped")


def check_chips(index):
    """ Displays how many chips the current player has.

    :param index: The index of the current player object in the list
    :type index:
    :return index.chips: Number of chips of the player at given index.
    :rtype index.chips: Int
    """
    print("")
    print("Checking player chips...")

    if index.chips == 1:
        print(index.name, "has", index.chips, "chip")
    else:
        print(index.name, "has", index.chips, "chips")
    return index.chips


def determine_turns(chips):
    """ Returns how many turns the player can take based on how many chips they have.

    :param chips: Number of chips the player has
    :type chips: Int
    :return: The number of turns player can take
    :rtype: Int
    """
    if chips >= 3:
        return 3
    if chips == 2:
        return 2
    else:
        return 1


def take_turn(i, turns, list_of_players, center_pot, total_chips):
    """ Player rolls dice for each turn they have and moves their chips based on
    outcome of dice roll. Then checks for winner and returns T or F

    :param i: The index of the current player object.
    :type: index
    :param turns: Number of turns (dice roll) player can take.
    :type turns: Int
    :param list_of_players: Player list needed to get adjacent players when moving chips
    :type list_of_players: List
    :param center_pot: Holds discarded chips.
    :type center_pot: Object
    :return winner: After player takes their turn, winner is checked and returns T or F.
    :rtype winner: Bool
    """
    print(i.name, "takes", turns, "turns")
    for num in range(turns):
        roll = roll_dice()
        move_chips(roll, i, list_of_players, center_pot)
    winner = check_for_winner(list_of_players, center_pot, total_chips)
    return winner


def roll_dice():
    """ Calls on Dice class to represent dice roll and gets random number.

    :return roll: Random number 1-6.
    :rtype roll: Int
    """
    dice_roll = Dice()
    roll = dice_roll.roll()
    return roll


def get_next_player(curr_player, p_list):
    """ Function to get player to the right.

    :param curr_player: Index of current player in player list.
    :type curr_player: Index
    :param p_list: List of player objects.
    :type p_list: List
    :return np: Index of next player in list (represents player to the right).
    :rtype np: Index
    """
    cpi = p_list.index(curr_player)  # Numerical representation of current player index

    if cpi + 1 < len(p_list):
        np = p_list[cpi + 1]
    else:
        np = p_list[0]

    return np


def get_previous_player(curr_player, p_list):
    """Function to get player to the left.

    :param curr_player: Index of current player in player list.
    :type curr_player: Index
    :param p_list: List of player objects.
    :type p_list: List
    :return pp: Index of previous player in list (represents player to the left).
    :rtype pp: Index
    """
    cpi = p_list.index(curr_player)  # Numerical representation of current player index

    if cpi > 0:
        pp = p_list[cpi - 1]
    else:
        pp = p_list[len(p_list) - 1]

    return pp


def display_updated_chips(player_one, player_two):
    """ Displays how many chips players have after chips have moved.

    :param player_one: Player whose current turn it is.
    :type player_one: Player Object
    :param player_two: Player who had chips moved to them.
    :type player_two: Player Object
    """
    print(player_one.name, "now has", player_one.chips, "and",
          player_two.name, "now has", player_two.chips)


def move_chips(dice, player_index: object, player_list, center_pot):
    """ Chips are moved based on dice roll of current player.

    :param dice: Result of random dice roll determines how chips are moved.
    :type dice: Int
    :param player_index: The current player.
    :type player_index: Player Object
    :param player_list: List of players
    :type player_list: List
    :param center_pot: Holds discarded chips
    :type center_pot: CenterPot Object
    """
    dice_num = dice

    cp = player_index  # current player
    np = get_next_player(player_index, player_list)  # next player
    pp = get_previous_player(player_index, player_list)  # previous player

    if dice_num == 1:
        print("You rolled an 'L'. Move one chip to player on left")

        cp.chips = cp.chips - 1  # decrement current player's chips
        pp.chips = pp.chips + 1  # increment previous player's chips

        display_updated_chips(cp, pp)

    elif dice_num == 2:
        print("You rolled a 'C'. Move one chip to the center pot")

        cp.chips = cp.chips - 1  # decrement current player's chips
        center_pot.chips = center_pot.chips + 1

        print("Center pot has", center_pot.chips, "and", cp.name, "has", cp.chips)

    elif dice_num == 3:
        print("You rolled an 'R'. Move one chip to player on right")

        cp.chips = cp.chips - 1  # decrement current player's chips
        np.chips = np.chips + 1  # increment next player's chips (player to right)

        display_updated_chips(cp, np)

    else:
        print("You rolled an '*'. No chips move")


def check_for_winner(list_of_players, center_pot, total_chips):
    """ Loops through player list checking if player chips plus chips in center
    pot is equal to chips in play. If so, we have a winner.

    :param list_of_players: List of player objects
    :type list_of_players: List
    :param center_pot: Holds discarded chips
    :type center_pot: CenterPot Object
    :param total_chips: Total chips in play
    :type total_chips: Int
    :return: Returns T if there is a winner, F otherwise.
    :rtype: bool
    """
    for i in list_of_players:
        if i.chips + center_pot.chips == total_chips:
            print(i.name, "is the winner!")
            return True
    return False


main()
