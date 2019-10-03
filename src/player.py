# Write a class to hold player information, e.g. what room they are in
# currently.
from light_source import Light_Source

class Player:

  def __init__(self, name, current_room, items = []):
    self.name = name
    self.current_room = current_room
    self.items = items

  def move(self, dir):
    next_room = None
    current_room = self.current_room

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
      self.current_room = next_room

    return True

  def quit_game(self, cmd):
    if cmd == "q":
      quit()
      return True
    else:
      return False

  def take_item(self, cmd):
    cmd = cmd.split(" ")
    
    if len(cmd) < 2 or not (cmd[0] == 'take' or cmd[0] == 'get'):
      return False

    if not self.current_room.is_light and not self.is_light_source_in_inventory():
      print("Good luck finding that in the dark!")
      return True

    item_to_take = None
    for item in self.current_room.items:
      if item.name.lower() == cmd[1]:
        item_to_take = item
        break
    
    if item_to_take == None:
      print("There is no such item")
    else:
      self.current_room.items.remove(item_to_take)
      self.items.append(item_to_take)

      item_to_take.on_take()

    return True

  def drop_item(self, cmd):
    cmd = cmd.split(" ")
    
    if len(cmd) < 2 or not (cmd[0] == 'drop'):
      return False

    item_to_drop = None
    for item in self.items:
      if item.name.lower() == cmd[1]:
        item_to_drop = item
        break
    
    if item_to_drop == None:
      print("There is no such item")
    else:
      self.items.remove(item_to_drop)
      self.current_room.items.append(item_to_drop)

      item_to_drop.on_drop()

    return True

  def show_inventory(self, cmd):
    if not (cmd == "inventory" or cmd == "i"):
      return False

    if (len(self.items) == 0):
      print("You have no items")
    else:
      print("You have ", end = "")
      for idx, item in enumerate(self.items):
        print(f"{item.name}", end = "")
        if idx != len(self.items) - 1:
          print(", ", end ="")
      print()

    return True

  def print_items_on_the_ground(self):
    items_on_the_ground = self.current_room.items

    if len(items_on_the_ground) > 0:
      print("You see some items lying around: ", end = "")
      for idx, item in enumerate(items_on_the_ground):
        print(f"{item.name}", end = "")
        if idx != len(items_on_the_ground) - 1:
          print(", ", end ="")
      print()

  def is_light_source_in_inventory(self):
    for item in self.items:
      if isinstance(item, Light_Source):
        return True
    return False

