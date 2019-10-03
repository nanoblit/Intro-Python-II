from room import Room
from player import Player
from item import Item
from light_source import Light_Source

# Declare all the rooms

room = {
  'outside':  Room("Outside Cave Entrance",
                   "North of you, the cave mount beckons",
                   True,
                   [
                     Item("Key", "An old, mysterious key"), 
                     Item("Orb", "A glass orb"), 
                     Light_Source("Torch", "It throws light on your surroundings")
                   ]),

  'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east.""", False),

  'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm.""", True),

  'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air.""", False),

  'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south.""", False),
}


# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

#
# Main
#

# Make a new player object that is currently in the 'outside' room.
player = Player('Sam', room['outside'])
# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.

while True:
  if player.current_room.is_light or player.is_light_source_in_inventory():
    print(f"You are in {player.current_room.name}.")
    print(f"{player.current_room.description}.")

    player.print_items_on_the_ground()
  else:
    print("It's too dark to see anything.")

  print("---------------------------------------------------------------")
  print("|[n] - go north, [s] - go south, [e] - go east, [w] - go west.|")
  print("|[take/get] [item name] - pick up an item.                    |")
  print("|[drop] [item name] - drop an item.                           |")
  print("|[i/inventory] - see items in your inventory.                 |")
  print("---------------------------------------------------------------")
  cmd = input("Give a command: ").strip().lower()

  print("============")

  if not player.move(cmd) and not player.take_item(cmd) and \
     not player.drop_item(cmd) and not player.quit_game(cmd) and \
     not player.show_inventory(cmd):
    print("Invalid command.")
