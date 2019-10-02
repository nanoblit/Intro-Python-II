from room import Room
from player import Player
from item import Item

# Declare all the rooms

room = {
  'outside':  Room("Outside Cave Entrance",
                   "North of you, the cave mount beckons",
                   [Item("Key", "An old, mysterious key"), Item("Orb", "A glowing orb")]),

  'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

  'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

  'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

  'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south."""),
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

def move(dir):
  next_room = None
  current_room = player.current_room

  if dir == 'n':
    next_room = current_room.n_to
  elif dir == 's':
    next_room = current_room.s_to
  elif dir == 'e':
    next_room = current_room.e_to
  elif dir == 'w':
    next_room = current_room.w_to
  else:
    return False

  if next_room == None:
    print("You can't move in this direction.")
  else:
    player.current_room = next_room

  return True

def quit_game(cmd):
  if cmd == "q":
    quit()
    return True
  else:
    return False

def take_item(cmd):
  cmd = cmd.split(" ")
  
  if len(cmd) < 2 or not (cmd[0] == 'take' or cmd[0] == 'get'):
    return False

  item_to_take = None
  for item in player.current_room.items:
    if item.name.lower() == cmd[1]:
      item_to_take = item
      break
  
  if item_to_take == None:
    print("There is no such item")
  else:
    player.current_room.items.remove(item_to_take)
    player.items.append(item_to_take)

    item_to_take.on_take()

  return True

def drop_item(cmd):
  cmd = cmd.split(" ")
  
  if len(cmd) < 2 or not (cmd[0] == 'drop'):
    return False

  item_to_drop = None
  for item in player.items:
    if item.name.lower() == cmd[1]:
      item_to_drop = item
      break
  
  if item_to_drop == None:
    print("There is no such item")
  else:
    player.items.remove(item_to_drop)
    player.current_room.items.append(item_to_drop)

    item_to_drop.on_drop()

  return True

def show_inventory(cmd):
  if not (cmd == "inventory" or cmd == "i"):
    return False

  if (len(player.items) == 0):
    print("You have no items")
  else:
    print("You have ", end = "")
    for idx, item in enumerate(player.items):
      print(f"{item.name}", end = "")
      if idx != len(player.items) - 1:
        print(", ", end ="")
    print()

  return True

def print_items_on_the_ground():
  items_on_the_ground = player.current_room.items

  if len(items_on_the_ground) > 0:
    print("You see some items lying around: ", end = "")
    for idx, item in enumerate(items_on_the_ground):
      print(f"{item.name}", end = "")
      if idx != len(items_on_the_ground) - 1:
        print(", ", end ="")
    print()
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
  print(f"You are in {player.current_room.name}.")
  print(f"{player.current_room.description}.")

  print_items_on_the_ground()

  print("---------------------------------------------------------------")
  print("|[n] - go north, [s] - go south, [e] - go east, [w] - go west.|")
  print("|[take/get] [item name] - pick up an item.                    |")
  print("|[drop] [item name] - drop an item.                           |")
  print("|[i/inventory] - see items in your inventory.                 |")
  print("---------------------------------------------------------------")
  cmd = input("Give a command: ").lower()

  print("============")

  if not move(cmd) and not take_item(cmd) and \
     not drop_item(cmd) and not quit_game(cmd) and \
     not show_inventory(cmd):
    print("Invalid command.")
