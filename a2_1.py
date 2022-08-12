from __future__ import annotations

from re import T
import abc
from typing import Optional
from a2_support import UserInterface, TextInterface
from constants import *

# Replace these <strings> with your name, student number and email address.
__author__ = "<Your Name>, <Your Student Number>"
__email__ = "<Your Student Email>"

# Before submission, update this tag to reflect the latest version of the
# that you implemented, as per the blackboard changelog. 
__version__ = 1.0


# Uncomment this function when you have completed the Level class and are ready
# to attempt the Model class.

def load_game(filename: str):
    """ Reads a game file and creates a list of all the levels in order.

    Parameters:
        filename: The path to the game file

    Returns:
        A list of all Level instances to play in the game
    """
    levels = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('Maze'):
                _, _, dimensions = line[5:].partition(' - ')
                dimensions = [int(item) for item in dimensions.split()]
                levels.append(Level(dimensions))
            elif len(line) > 0 and len(levels) > 0:
                levels[-1].add_row(line)
    return levels


# Write your classes here
class Tile:

    @abc.abstractmethod
    def is_blocking(self):
        return False

    ''' is_blocking(self) -> bool
        Returns the ID of the tile. For non-abstract subclasses,
        the ID should be a single character representing the
        type of Tile it is. See constants.py for the ID value 
        of all tiles and entities.'''

    @abc.abstractmethod
    def damage(self):
        return 0

    ''' damage(self) -> int 
        Returns the damage done to a player if they 
        step on this tile. For instance, if a tile has a damage
        of 3, the player’s HP would be reduced by 3 if they step 
        onto the tile. By default, tile’s should do no damage to a
        player.'''

    @abc.abstractmethod
    def get_id(self):
        return ABSTRACT_TILE

    '''get_id(self) -> str
        Returns the ID of the tile. For non-abstract subclasses, 
        the ID should be a single character representing the
        type of Tile it is. See constants.py for the ID value of
        all tiles and entities.'''

    def __str__(self):
        return self.get_id()

    '''__str__(self) -> str (method)
        Returns the string representation
        for this Tile.'''

    def __repr__(self):
        return type(self).__name__ + "()"

    '''__repr__(self) -> str (method)
        Returns the text that would be required to create a new instance of this class'''


class Wall(Tile):

    def damage(self):
        return 0

    def is_blocking(self):
        return True

    def get_id(self):
        return WALL


'''Inherits from Tile
    Wall is a type of Tile that is blocking.'''


class Empty(Tile):

    def damage(self):
        return 0

    def is_blocking(self):
        return False

    def get_id(self):
        return EMPTY


'''Inherits from TileEmpty is a type of Tile that 
    does not contain anything special. A player can move 
    freely over empty tiles without taking any damage. 
    Note that the ID for an empty tile is a single space (not an empty string).'''


class Lava(Tile):

    def is_blocking(self):
        return False

    def damage(self):
        return LAVA_DAMAGE

    def get_id(self):
        return LAVA


'''Inherits from Tile Lava is a type of Tile that is 
    not blocking, but does a damage of 5 to the player’s 
    HP when stepped on. Note: This damage is in addition
    to any other damage sustained. For example, if the player’s
    HP is also reduced by 1 for making a successful move,
    then the total reduction to the player’s HP will be 6.
    However, the application of the damage for each move should 
    not be handled within this class.'''


class Door(Tile):
    status = True
    id = DOOR

    def damage(self):
        return 0

    def is_blocking(self):
        return self.status

    def get_id(self):
        return self.id

    def unlock(self):
        self.status = False
        self.id = EMPTY

    '''Unlocks the door.'''


'''Inherits from Tile Door is a type of Tile 
    that starts as locked (blocking). Once the player 
    has collected all coins in a given maze, the door 
    is ‘unlocked’ (becomes non-blocking and has its ID 
    change to that of an empty tile), and the player can 
    move through the square containing the unlocked door 
    to complete the level. In order to facilitate this 
    functionality in later classes, the Door class must 
    provide a method through which to ‘unlock’ a door.'''


class Entity:

    def __init__(self, position):
        self.position = position

    '''__init__(self, position: tuple[int, int]) -> None (method)
        Sets up this entity at the given (row, column) position.'''

    def get_position(self):
        return self.position

    '''get_position(self) -> tuple[int, int] (method)
        Returns this entities (row, column) position.'''

    def get_name(self):
        return type(self).__name__

    '''get_name(self) -> str (method)
        Returns the name of the class to which this entity belongs.'''

    @abc.abstractmethod
    def get_id(self):
        return "E"

    '''get_id(self) -> str (method) Returns the ID of this entity.
        For all non-abstract subclasses, this should be a single character
        representing the type of the entity.'''

    def __str__(self):
        return self.get_id()

    '''__str__(self) -> str (method)
        Returns the string representation for this entity (the ID).'''

    def __repr__(self):
        return type(self).__name__ + "(" + str(self.get_position()) + ")"

    '''__repr__(self) -> str (method) Returns the text 
        that would be required to make a new instance of this 
        class that looks identical (where possible) to self.'''


class DynamicEntity(Entity):

    def set_position(self, new_position):
        self.position = new_position

    '''set_position(self, new_position: tuple[int, int]) -> None (method)
        Updates the DynamicEntity’s position to new_position, assuming it is a valid position.'''

    def get_id(self):
        return DYNAMIC_ENTITY


'''Inherits from Entity DynamicEntity is an 
    abstract class which provides base functionality 
    for special types of Entities that are dynamic 
    (e.g. can move from their original position).'''


class Player(DynamicEntity):

    def __init__(self, position):
        super().__init__(position)
        self.hunger = 0
        self.thirst = 0
        self.health = MAX_HEALTH
        self.inventory = Inventory()

    def get_id(self):
        return PLAYER

    def get_hunger(self):
        return self.hunger

    '''get_hunger(self) -> int (method)
        Returns the player’s current hunger level.'''

    def get_thirst(self):
        return self.thirst

    '''get_thirst(self) -> int (method)
        Returns the player’s current thirst level.'''

    def get_health(self):
        return self.health

    '''get_health(self) -> int (method)
        Returns the player’s current HP.'''

    def change_hunger(self, amount: int):
        self.hunger += amount

        if self.hunger > MAX_HUNGER:
            self.hunger = MAX_HUNGER
        elif self.hunger < 0:
            self.hunger = 0

    '''change_hunger(self, amount: int) -> None (method)
        Alters the player’s hunger level by the given amount.
        You must cap the player’s hunger to be between 0 and 10 (inclusive).'''

    def change_thirst(self, amount: int):
        self.thirst += amount

        if self.thirst > MAX_THIRST:
            self.thirst = MAX_THIRST
        elif self.thirst < 0:
            self.thirst = 0
        '''change_thirst(self, amount: int) -> None (method) 
        Alters the player’s thirst level by the given amount.
        You must cap the player’s thirst to be between 0 and 10(inclusive).'''

    def change_health(self, amount: int):
        self.health += amount

        if self.health > MAX_HEALTH:
            self.health = MAX_HEALTH
        elif self.health < 0:
            self.health = 0
        '''change_health(self, amount: int) -> None (method)
        Alters the player’s health level by the given amount.
        You must cap the player’s health to be between 0 and 100(inclusive).'''

    def get_inventory(self):
        return self.inventory

    '''get_inventory(self) -> Inventory (method)
        Returns the player’s Inventory instance.'''

    def add_item(self, item: Item):
        self.inventory.add_item(item)

    '''add_item(self, item: Item) -> None (method)
        Adds the given item to the player’s Inventory instance'''


class Item(Entity):

    def get_id(self):
        return ITEM

    @abc.abstractmethod
    def apply(self, player: Player):
        return NotImplementedError

    '''apply(self, player: Player) -> None (abstract method)
        Applies the items effect, if any, to the given player.'''


class Potion(Item):

    def get_id(self):
        return POTION

    def apply(self, player: Player):
        player.change_health(POTION_AMOUNT)

    '''apply(self, player: Player) -> None (abstract method)
    Applies the items effect, if any, to the given player.'''


class Coin(Item):

    def get_id(self):
        return COIN

    def apply(self, player: Player):
        pass

    '''Inherits from Item 
    A coin is an item that has no effect when applied to a player.
    Note: The purpose of a coin is to be collected and stored in 
    a players inventory. However, the act of adding the coin to
    the players inventory is not done within this class.'''


class Water(Item):

    def get_id(self):
        return WATER

    def apply(self, player: Player):
        player.change_thirst(WATER_AMOUNT)

    '''Inherits from Item
    Water is an item that will decrease the 
    player’s thirst by 5 when applied.'''


class Food(Item):
    def get_id(self):
        return FOOD

    def apply(self, player: Player):
        player.change_hunger(0)


'''Inherits from Item
    Food is an abstract class. Food subclasses 
    implement an apply method that decreases the 
    players hunger by a certain amount, depending
    on the type of food. The examples below describe 
    the usage of the two foodsubclasses (Honey and Apple)
    described in the next two sections.'''


class Apple(Food):

    def get_id(self):
        return APPLE

    def apply(self, player: Player):
        player.change_hunger(APPLE_AMOUNT)


'''Inherits from Food Apple is a type
    of food that decreases the player’s hunger 
    by 1 when applied'''


class Honey(Food):
    def get_id(self):
        return HONEY

    def apply(self, player: Player):
        player.change_hunger(HONEY_AMOUNT)


'''Inherits from Food
    Honey is a type of food that decreases
    the player’s hunger by 5 when applied'''


class Inventory:
    def __init__(self, initial_items=None):
        self.inv = {}
        if initial_items:
            for i in initial_items:
                self.add_item(i)

    ''' __init__(self, initial_items: Optional[list[Item,...]] = None) -> None (method)
        Sets up initial inventory. If no initial_items is provided, 
        inventory starts with an empty dictionary for the items. 
        Otherwise, the initial dictionary is set up from the initial_items 
        list to be a dictionary mapping item names to a list of 
        item instances with that name.'''

    def add_item(self, item: Item):
        if item.get_name() in self.inv:
            self.inv[item.get_name()].append(item)
        else:
            self.inv[item.get_name()] = [item]

    '''add_item(self, item: Item) -> None (method)
        Adds the given item to this inventory’s collection of items.'''

    def get_items(self):
        return self.inv

    '''get_items(self) -> dict[str, list[Item,...]] (method)
        Returns a dictionary mapping the names of all items in the
        inventory to lists containing each instance of the item with that name.'''

    def remove_item(self, item_name: str):
        self.inv[item_name].pop(0)
        if len(self.inv[item_name]) == 0:
            self.inv.pop(item_name)

    '''remove_item(self, item_name: str) -> Optional[Item] (method)
        Removes and returns the first instance of the item with the 
        given item_name from the inventory. If no item exists in 
        the inventory with the given name, then this method returns None.'''

    def __str__(self):
        s = ""
        for i in self.inv:
            s += i + ": " + str(len(self.inv[i])) + "\n"
        return s

    '''__str__(self) -> str (method)
        Returns a string containing information about quantities 
        of items available in the inventory.'''

    def __repr__(self):
        lst = []
        for i in self.inv:
            lst += self.inv[i]
        return type(self).__name__ + "(" + str(lst) + ")"

    '''__repr__(self) -> str (method)
        Returns a string that could be used to construct 
        a new instance of Inventory containing the same items as
        self currently contains. Note that the order of the 
        initial_items is not important for this method.'''


class Maze:

    def __init__(self, dimensions):
        self.dimension = dimensions
        self.maze = []
        self.door = None

    '''__init__(self, dimensions: tuple[int, int]) -> None (method)
        Sets up an empty maze of given dimensions 
        (a tuple of the number of rows and number of columns).'''

    def get_dimensions(self):
        return self.dimension

    '''get_dimensions(self) -> tuple[int, int] (method)
        Returns the (#rows, #columns) in the maze.'''

    def add_row(self, row: str):
        if len(self.maze) == self.dimension[0]:
            return
        j = 0
        lst = []
        for s in row:
            if j == self.dimension[1]:
                break
            if s == LAVA:
                lst.append(Lava())
            elif s == WALL:
                lst.append(Wall())
            elif s == DOOR:
                lst.append(Door())
                self.door = (len(self.maze), j)
            else:
                lst.append(Empty())
            j += 1
        self.maze.append(lst)

    '''add_row(self, row: str): -> None (method)
        Adds a row of tiles to the maze. Each character in 
        row is a Tile ID which can be used to construct the
        appropriate Tile instance to place in that position 
        of the row of tiles. A precondition of this method 
        is that the addition of a row must not violate the 
        maze dimensions. Note: if a row string contains an 
        empty space or an invalid or unknown Tile ID, an 
        Empty tile should be placed in that position.'''

    def get_tiles(self):
        return self.maze

    '''get_tiles(self) -> list[list[Tile]] (method)
        Returns the Tile instances in this maze. Each element is a row (list of Tile instances in order).'''

    def unlock_door(self):
        self.maze[self.door[0]][self.door[1]].unlock()

    '''unlock_door(self) -> None (method)
        Unlocks any doors that exist in the maze.'''

    def get_tile(self, position):
        return self.maze[position[0]][position[1]]

    '''get_tile(self, position: tuple[int, int]) -> Tile (method)
        Returns the Tile instance at the given position.'''

    def __str__(self):
        s = ""
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                s += self.maze[i][j].get_id()
            s += "\n"
        return s[0:len(s) - 1]

    '''__str__(self): -> str (method)
        Returns the string representation of this maze. Each 
        line in the output is a row in the maze (each Tile instance is represented by its ID).'''

    def __repr__(self):
        return type(self).__name__ + "(" + str(self.dimension) + ")"

    '''__repr__(self) -> str (method)
        Returns a string that could be copied and pasted to 
        construct a new Maze instance with the same dimensions
        as this Maze instance.'''


'''A Maze instance represents the space in 
    which a level takes place. The maze does not 
    know what entities are placed on it or where 
    the entities are; it only knows what tiles it 
    contains and what dimensions it has.'''


class Level:

    def __init__(self, dimensions):
        self.maze = Maze(dimensions)
        self.player_start = None
        self.entities = {}

    '''__init__(self, dimensions: tuple[int, int]) -> None (method)
    Sets up a new level with empty maze using the 
    given dimensions. The level is set up initially
    with no items or player.'''

    def get_maze(self):
        return self.maze

    '''get_maze(self) -> Maze (method)
    Returns the Maze instance for this level.'''

    def attempt_unlock_door(self):
        for i in self.entities:
            if isinstance(self.entities[i], Coin):
                return
        self.maze.unlock_door()

    '''attempt_unlock_door(self) -> None (method)
    Unlocks the doors in the maze if there 
    are no coins remaining.'''

    def add_row(self, row: str):
        i = len(self.maze.maze)
        if i > self.get_dimensions()[0]:
            return
        j = 0
        for entity_id in row:
            if j > self.get_dimensions()[1]:
                break
            self.add_entity((i, j), entity_id)
            j += 1
        self.maze.add_row(row)

    '''add_row(self, row: str) -> None (method)
    Adds the tiles and entities from the row to
    this level. row is a string containing the Tile IDs 
    and Entity IDs to place in this row.'''

    def add_entity(self, position, entity_id: str):
        if entity_id == POTION:
            self.entities[position] = Potion(position)
        if entity_id == PLAYER:
            self.add_player_start(position)
        elif entity_id == COIN:
            self.entities[position] = Coin(position)
        elif entity_id == WATER:
            self.entities[position] = Water(position)
        elif entity_id == APPLE:
            self.entities[position] = Apple(position)
        elif entity_id == HONEY:
            self.entities[position] = Honey(position)

    '''add_entity(self, position: tuple[int, int], entity_id: str) -> None (method)
    Adds a new entity to this level in the given position. 
    Entity type is determined by the entity_id. The information 
    you store from this method may differ depending on the 
    specific type of the entity requested. If the entity is 
    an item, you should store it with its position in such 
    a way that, if an item existed at that position previously, 
    this new item will replace it.'''

    def get_dimensions(self):
        return self.maze.dimension

    '''get_dimensions(self) -> tuple[int, int] (method)
    Returns the (#rows, #columns) in the level maze.'''

    def get_items(self):
        return self.entities

    '''get_items(self) -> dict[tuple[int, int], Item] (method)
    Returns a mapping from position to the Item at that 
    position for all items currently in this level.'''

    def remove_item(self, position):
        self.entities.pop(position)

    '''remove_item(self, position: tuple[int, int]) -> None (method)
    Deletes the item from the given position. A 
    precondition of this method is that there is an 
    Item instance at the position.'''

    def add_player_start(self, position):
        self.player_start = position

    '''add_player_start(self, position: tuple[int, int]) -> None (method)
    Adds the start position for the player in this level.'''

    def get_player_start(self):
        return self.player_start

    '''get_player_start(self) -> Optional[tuple[int, int]] (method)
    Returns the starting position of the player for this level. If no player start has been defined yet, this method
    returns None.'''

    def __str__(self):
        return "Maze: " + self.maze.__str__() + "\nItems: " + str(self.entities) + "\nPlayer start: " + str(
            self.get_player_start())

    '''__str__(self) -> str (method)
    Returns a string representation of this level.'''

    def __repr__(self):
        return type(self).__name__ + "(" + str(self.get_dimensions()) + ")"

    ''' __repr__(self) -> str (method)
    Returns a string that could be copied and pasted to construct a new Level instance with the same dimensions
    as this Level instance.'''


'''A Level instance keeps track of both the 
    maze and the non-player entities placed 
    on the maze for a single level.'''


class Model:

    def __init__(self, game_file: str):
        self.file = game_file
        self.levels = load_game(game_file)
        self.won = False
        self.lost = False
        self.level = 0
        self.current_level = self.levels[self.level]
        self.just_level_up = False
        self.valid_move = 0
        self.player = Player(self.get_level().get_player_start())
        self.last_move = False

    def has_won(self):
        return self.won

    '''has_won(self) -> bool (method)
    Returns True if the game has been won, otherwise 
    returns False. A game has been won if all the 
    levels have been successfully completed.'''

    def has_lost(self):
        return self.lost

    '''has_lost(self) -> bool (method)
        Returns True if the game has been lost, 
        otherwise returns False (HP too low or hunger or thirst too high).'''

    def get_winning_move(self):
        x,y = self.get_level().get_maze().door[0],self.get_level().get_maze().door[1]
        m,n = self.get_level().get_maze().get_dimensions()[0]-1,self.get_level().get_maze().get_dimensions()[0]-1
        if x == m:
            return MOVE_DELTAS[DOWN]
        elif x == 0:
            return MOVE_DELTAS[UP]
        elif y == n:
            return MOVE_DELTAS[RIGHT]
        elif y == 0:
            return MOVE_DELTAS[LEFT]
        else:
            return None



    def get_level(self):
        return self.current_level

    ''' get_level(self): -> Level (method)
        Returns the current level.'''

    def level_up(self):
        if self.level + 1 < len(self.levels):
            self.level += 1
            self.just_level_up = True
            self.current_level = self.levels[self.level]
            self.last_move = False
            self.get_player().set_position(self.current_level.get_player_start())

        else:
            self.won = True

    '''level_up(self): -> None (method)
        Changes the level to the next level in the game. If no more levels remain, the player has won the game.'''

    def did_level_up(self):
        return self.just_level_up

    '''did_level_up(self): -> bool (method)
        Returns True if the player just moved to the next level on the previous turn, otherwise returns False.'''

    def move_player(self, delta):
        cur_loc = self.get_player().get_position()
        new_loc = (cur_loc[0] + delta[0], cur_loc[1] + delta[1])

        if (new_loc[0] >= self.get_current_maze().get_dimensions()[0] or \
                new_loc[1] >= self.get_current_maze().get_dimensions()[1]) and self.last_move:
            self.last_move = False
            if delta == self.get_winning_move():
                self.level_up()
        else:
            tile = self.get_level().get_maze().get_tile(new_loc)

            if not tile.is_blocking():
                self.get_player().change_health(-1 * tile.damage())
                self.get_player().change_health(-1)
                self.get_player().set_position(new_loc)

                self.attempt_collect_item(new_loc)

                self.valid_move += 1

                if self.valid_move >= 5:
                    self.valid_move = 1
                    self.get_player().change_hunger(1)
                    self.get_player().change_thirst(1)

                self.just_level_up = False


            if self.get_player().get_health() == 0 or self.get_player().get_hunger() == 10 \
                    or self.get_player().get_thirst() == 10:
                self.lost = True

            if self.last_move:
                self.last_move = False
                if delta == self.get_winning_move():
                    return self.level_up()

    '''move_player(self, delta: tuple[int, int]) -> None (method)
        Tries to move the player by the requested (row, column) change 
        (delta). This method should also level up if the player finished
        the maze by making the move. If the player did not level up and 
        the tile that the player is moving into is non-blocking, this method should:
            • Update the players hunger, thirst based on the number 
                of moves made.
            • Update players health based on the successful movement 
                and the damage caused by the tile the player
                has moved onto.
            • Update the players position.
            • Attempt to collect any item that is on the players new position.
        Levels up if the player finishes the maze by making the move. This 
        function should also handle'''

    def attempt_collect_item(self, position):
        if position in self.get_level().get_items():
            self.get_player().add_item(self.get_level().get_items()[position])
            self.get_level().remove_item(position)
        self.get_level().attempt_unlock_door()

    '''attempt_collect_item(self, position: tuple[int, int]): -> None (method)
        Collects the item at the given position if one exists. Unlocks the door if all coins have been collected.'''

    def get_player(self):
        return self.player

    '''get_player(self) -> Player (method)
        Returns the player in the game.'''

    def get_player_stats(self):
        stat = (self.get_player().health, self.get_player().hunger, self.get_player().thirst)
        return stat

    '''get_player_stats(self) -> tuple[int, int, int] (method)
        Returns the player’s current stats as (HP, hunger, thirst).'''

    def get_player_inventory(self):
        return self.get_player().get_inventory()

    '''get_player_inventory(self) -> Inventory (method)
        Returns the players inventory.'''

    def get_current_maze(self):
        return self.get_level().get_maze()

    '''get_current_maze(self): -> Maze (method)
        Returns the Maze for the current level.'''

    def get_current_items(self):
        return self.get_level().get_items()

    '''get_current_items(self) -> dict[tuple[int, int], Item] (method)
        Returns a dictionary mapping tuple positions to the item that currently exists at that position on the maze.
        Only positions at which an item exists should be included in the result.'''

    def __str__(self):
        return type(self).__name__+"('"+self.file+"')"

    ''' __str__(self) -> str (method)
            Returns the text required to construct a new instance of Model with the same game file used to construct
            self.'''

    def __repr__(self):
        return type(self).__name__+"('"+self.file+"')"

    '''__repr__(self) -> str (method)
    Does the same thing as __str__.'''


'''__init__(self, game_file: str) -> None (method)
    Sets up the model from the given game_file, which is 
    a path to a file containing game information (e.g.
    games/game1.txt). Once you have written the Level 
    class, you can uncomment the provided load_game
    function and use it to aid in your implemention of 
    the this method.'''


class MazeRunner:

    def __init__(self, game_file: str, view: TextInterface):
        self.game = Model(game_file)
        self.view = view

        self.play()

    ''' __init__(self, game_file: str, view: UserInterface) -> None (method)
    Creates a new MazeRunner game with the given view and a 
    new Model instantiated using the given game_file.'''

    def play(self):
        self.view.draw(self.game.get_current_maze(), self.game.get_current_items(),
                       self.game.get_player().get_position(), self.game.get_player_inventory(),
                       self.game.get_player_stats())

        while True:

            inp = input("\nEnter a move: ")

            if inp[0:2] == "i ":
                item = inp[2:]
                if item in self.game.get_player_inventory().get_items():
                    self.game.get_player_inventory().get_items()[item][0].apply(self.game.get_player())
                    self.game.get_player_inventory().remove_item(item)
                else:
                    print(ITEM_UNAVAILABLE_MESSAGE)
            elif inp.lower() == UP:
                self.game.move_player(MOVE_DELTAS[UP])
            elif inp.lower() == LEFT:
                self.game.move_player(MOVE_DELTAS[LEFT])
            elif inp.lower() == RIGHT:
                self.game.move_player(MOVE_DELTAS[RIGHT])
            elif inp.lower() == DOWN:
                self.game.move_player(MOVE_DELTAS[DOWN])
            else:
                continue
            break

        if self.game.get_level().get_maze().door is not None and\
                self.game.get_level().get_maze().door == self.game.get_player().get_position():
            self.game.last_move = True

        if self.game.has_lost():
            print(LOSS_MESSAGE)
            exit(0)
        elif self.game.has_won():
            print(WIN_MESSAGE)
            exit(0)

        self.play()

    # '''play(self): -> None (method)
    #     Executes the entire game until a win or loss occurs. When the a2.py file is run, a MazeRunner instance is
    #     created and this method is run. As such, this method should cause all of the program output. For examples
    #     of how this method should operate, see the gameExamples/ folder, which contains example outputs of full
    #     MazeRunner games.'''


''' MazeRunner is the controller class, which should
     maintain instances of the model and view, collect user input
    and facilitate communication between the model and view. The 
    methods you must implement are outlined below, but you are 
    strongly encouraged to implement your own helper methods where possible.'''


def main():
    inp = input("Enter game file: ")
    MazeRunner('games/game3.txt', TextInterface())


if __name__ == '__main__':
    main()
