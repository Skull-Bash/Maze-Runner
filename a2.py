from __future__ import annotations
from typing import Optional
from a2_support import UserInterface, TextInterface
from constants import *
import abc

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
    """ It represents and handles the functionalities of the Tiles in the maze 

    Parameters:


    Functionalities:
        This class is the parent class of Wall,Empty,Lava,Door tiles
        and sets an initial tile representation.
    """

    @abc.abstractmethod
    def is_blocking(self):
        """ Creates a blocked tile which the player can't move into 

        Parameters:


        Returns:
            It returns boolean representing functionality of a tile (of Subclasses)
        """
        return False

    @abc.abstractmethod
    def damage(self):
        """ The damage (reduce HP) caused for different tiles (of subclasses)

        Parameters:


        Return:
            It returns Damage for the instance of tile(of subclasses)
        """
        return 0

    @abc.abstractmethod
    def get_id(self):
        """ It specifies the tile type (for subclasses)

        Parameters:


        Return:
            It returns ID of the tile (of subclasses)
        """
        return ABSTRACT_TILE

    def __str__(self):
        """ It represent String for the tile (subclasses)

        Parameters:


        Return:
            It returns string representation for the tile
        """
        return self.get_id()

    def __repr__(self):
        """ It returns a text that would create a new instance of the class (of subclasses) if required

        Parameters:


        Return:
            It returns string which creates instances
        """
        return type(self).__name__ + "()"


class Wall(Tile):
    """ It represents Wall and it is a blocking tile 

    Inherits from:
        Tile class

    Parameters:


    functionalities:
        The Wall tile work as a blocked tile 
        which resist the movement of the player 
        in to the tile
    """

    def damage(self):
        """ It represents damage of the Wall tile (which is None or 0) 

        Parameters:


        functionalities:
            No functionalities for this tile
        Return:
            return 0
        
        """
        return 0

    def is_blocking(self):
        """ It represents blocking(which is the main functionality of the wall tile) 

        Parameters:


        functionalities:
            It returns boolean True value which enables the wall tile as a blocking tile
        Return:
            return boolean true value
        """
        return True

    def get_id(self):
        return WALL


class Empty(Tile):
    """ It represents Empty tile where the player can move  

    Inherits from:
        Tile class

    Parameters:


    functionalities:
        It not consist of no damage or blocking tile which
        represents a movable tile for the player
    """

    def damage(self):
        """ It represents damage of the Empty tile (which is None or 0)

        Parameters:


        functionalities:
            No functionalities for this tile
        Return:
            return 0
        """
        return 0

    def is_blocking(self):
        """ It represents blocking of the Empty tile (which is false)

        Parameters:


        functionalities:
            It returns boolean false value which disables the blocking func of empty tile
        Return:
            return boolean false value
        """
        return False

    def get_id(self):
        """ It represents the ID of the empty tile

        Parameters:


        functionalities:
            It specifies the empty tile returning the Constant value of EMPTY
        Return:
            return EMPTY (single character ' '(white space) as per constants)
        """
        return EMPTY


class Lava(Tile):
    """ It represents lava tile where the player can move but will get damage
        however the function doesn't occur in this class
    Inherits from:
        Tile class

    Parameters:


    functionalities:
        The Lava tile work as an unblocked tile 
        which does not resist the movement of the player 
        in to the tile but apply damage (reduce HP) to the player
        when on the tile.
    """

    def is_blocking(self):
        """ It represents blocking of the Lava tile (which is false)

        Parameters:


        functionalities:
            It returns boolean false value which disables the blocking function of Lava tile
        Return:
            return boolean false value
        """
        return False

    def damage(self):
        """ It represents damage of the Lava tile
        (which is the main functionality of the lava tile) 
        but the application does not occur in this function
        Parameters:


        functionalities:
            It returns constant value of the LAVA_DAMAGE 
            which caused damage (reduce hp) to the player 
            for stepping into the lava tile,however the 
            functionality doesn't occur in this function
        Return:
            returns constant LAVA_DAMAGE value (integer)
        """
        return LAVA_DAMAGE

    def get_id(self):
        """ It represents the ID of the LAVA tile

        Parameters:


        functionalities:
            It specifies the Lava tile returning the Constant value of LAVA
        Return:
            return LAVA (single character 'L' as per constants)
        """
        return LAVA


class Door(Tile):
    """ It represents door tile which is initially blocked for the player
        but unblocks(by the unlock func) as per game criteria 

    Inherits from:
        Tile class

    Parameters:


    functionalities:
        The Door tile work as an blocked tile 
        which does resist the movement of the player 
        through the tile but can be unblocked by unlock function
    """
    status = True  # a local boolean variable for the unlock door status
    id = DOOR  # a local variable for changing the id of the tile as per door status

    def damage(self):
        """ It represents damage of the Door tile (which is None or 0)

        Parameters:


        functionalities:
            No functionalities for this tile
        Return:
            return 0
        """
        return 0

    def is_blocking(self):
        """ It represents blocking of the Door tile which is initially
        true or blocked but can change thorough the unlock function

        Parameters:


        functionalities:
            It returns boolean value which enables or disables the 
            blocking function of the tile accordingly
        Return:
            return self.status ,local boolean variable
        """
        return self.status

    def get_id(self):
        """ It represents the ID of the Door tile
            it changes the ID according to the 
            blocking or unblocking events of the tiles

        Parameters:


        functionalities:
            It returns the ID of the tile which depends of the unlock function event
            and specifies the blocked or unblocked functions of the tiles.
            (it returns constant Door & Empty for blocked & unblocked tiles respectively)
        Return:
            return self.id , local string variable
        """
        return self.id

    def unlock(self):
        self.status = False  # changing for unblocking the tile
        self.id = EMPTY  # changing the id for applying the changes (unblocked tile)


class Entity:
    """ It handles the positions of the Entities present 
        & sets up the entities in the maze 

        Parameters:


        functionalities:
            This class is the parent class of DynamicEntity,Item
            and handles the positions of the entities with ID's anf name
            and sets the positions of the entity in the maze
    """

    def __init__(self, position):
        """ A constructor for assigning positions

        Parameters:
            Position as a Tuple

        functionalities:
            assign positions
        Return:
            None
        """
        self.position = position

    def get_position(self):
        """ A functions which return and set the 
            position of the entity (of subclasses)

        Parameters:


        functionalities:
            return positions and help setting up entities
        Return:
            returns self.position , a local Tuple
            referenced from the position parameter
        """
        return self.position

    def get_name(self):
        """ A functions which return the name of the 
            entities from the constants

        Parameters:


        functionalities:
            return name of the entities referencing from the ID
        Return:
            return the type of self.__name__
        """

        return type(self).__name__

    @abc.abstractmethod
    def get_id(self):
        """ A functions which returns the ID of the entity from the constants

        Parameters:


        functionalities:
            return id of the entities (of the subclass)
        Return:
            return string type
        """
        return "E"

    def __str__(self):
        """ It returns the string representation of the ID

        Parameters:


        functionalities:
            return id of the current entity
        Return:
            return self.get_id string type
        """
        return self.get_id()

    def __repr__(self):
        """ It returns the string that would make 
            a instance of the class if required

        Parameters:


        functionalities:
            return the string with the position 
            of the entity for making instance of the class

        Return:
            return string type
        """
        return type(self).__name__ + "(" + str(self.get_position()) + ")"


class DynamicEntity(Entity):
    """ It represents and handle entity's which are dynamic in nature

    Inherits from:
        Entity class

    Parameters:


    functionalities:
        It updates the position of the 
        Dynamic entities and returns the ID of the entity
    """

    def set_position(self, new_position):
        """ It updates the Entity's current position 

        Parameters:
           new_position as a Tuple

        functionalities:
            it takes the new position and 
            updates the positions of entity, assuming the position is valid

        Return:
            None
        """
        self.position = new_position

    def get_id(self):
        """ A functions which returns the ID of the DynamicEntity

        Parameters:


        functionalities:
            return id of the DynamicEntity (of the subclass)
        Return:
            return DYNAMIC_ENTITY, string type
        """
        return DYNAMIC_ENTITY


class Player(DynamicEntity):
    """ It represents player and handle all the 
         changes in the player Dynamic entity

        Inherits from:
        DynamicEntity class

        Parameters:


        functionalities:
        handles , represent and update player Dynamic entity
    """

    def __init__(self, position):
        """ A constructor for assigning values for the player entity

        Parameters:
            Position as a Tuple

        functionalities:
            assign & initialize positions,hunger, thirst,health,inventory
        Return:
            None
        """
        super().__init__(position)
        self.hunger = 0
        self.thirst = 0
        self.health = MAX_HEALTH
        self.inventory = Inventory()  # Creating a inventory instance for a player

    def get_id(self):
        """ It represents the ID of the player Dynamic entity

        Parameters:


        functionalities:
            It specifies the player & returning the Constant value of Player entity
        Return:
            return PLAYER (single character 'p' as per constants)
        """
        return PLAYER

    def get_hunger(self):
        """ It returns the current hunger value 

        Parameters:


        functionalities:
            It return the hunger value of the current player entity
        Return:
            return self.hunger,local 
        """
        return self.hunger

    def get_thirst(self):
        """ It returns the current thirst value 

        Parameters:


        functionalities:
            It return the thirst value of the current player entity
        Return:
            return self.thirst,local 
        """
        return self.thirst

    def get_health(self):
        """ It returns the current health value 

        Parameters:


        functionalities:
            It return the health value of the current player entity
        Return:
            return self.health,local 
        """
        return self.health

    def change_hunger(self, amount: int):
        """ It change the hunger value by amount 
            according to the occurred event

        Parameters:
            amount (integer)

        functionalities:
            It changes the hunger value as per the amount and event occurred
            of the current player entity
        Return:
            None
        """
        self.hunger += amount  # changing the hunger amount by increasing

        if self.hunger > MAX_HUNGER:  # thresh holding the hunger value by the MAX_HUNGER constant up to max limit
            self.hunger = MAX_HUNGER
        elif self.hunger < 0:  # thresh holding the hunger value by 0 till min limit
            self.hunger = 0

    def change_thirst(self, amount: int):
        """ It change the thirst value by amount 
            according to the occurred event

        Parameters:
            amount (integer)

        functionalities:
            It changes the thirst value as per the amount and event occurred
            of the current player entity
        Return:
            None
        """
        self.thirst += amount  # changing the thirst amount by increasing

        if self.thirst > MAX_THIRST:  # thresh holding the thirst value by the MAX_THIRST constant up to max limit
            self.thirst = MAX_THIRST
        elif self.thirst < 0:  # thresh holding the thirst value by 0 till min limit
            self.thirst = 0

    def change_health(self, amount: int):
        """ It change the health value by amount 
            according to the occurred event

        Parameters:
            amount (integer)

        functionalities:
            It changes the health value as per the amount and event occurred
            of the current player entity
        Return:
            None
        """
        self.health += amount  # changing the health amount by increasing (negative value as amount parameter)

        if self.health > MAX_HEALTH:  # thresh holding the health value by the MAX_HEALTH constant up to max limit
            self.health = MAX_HEALTH
        elif self.health < 0:  # thresh holding the health value by 0 till min limit
            self.health = 0

    def get_inventory(self):
        """ It returns inventory of the player entity 

        Parameters:


        functionalities:
            It returns the inventory instance 
            of the current player entity for dynamic usage
        Return:
            returns self.inventory 
        """
        return self.inventory

    def add_item(self, item: Item):
        """ It adds the item to the player's inventory instance

        Parameters:
            item

        functionalities:
            takes the item as a parameter and adds 
            to the inventory instance of the player entity
        Return:
            None
        """
        self.inventory.add_item(item)


class Item(Entity):
    """ It represents item(subclasses) & 
        apply the events as per item 
        to the player entity

        Inherits from:
        Entity class

        Parameters:


        functionalities:
        represent and apply event of items(subclasses) to the player entity 
    """

    def get_id(self):
        """ A functions which returns the ID of the ITEM

        Parameters:


        functionalities:
            return id of the items (of the subclass)
        Return:
            return ITEM, string type
        """
        return ITEM

    @abc.abstractmethod
    def apply(self, player: Player):
        """ the method apply the items to the player entity

        Parameters:


        functionalities:
            its a abstract method for 
            applying the items to the player 
            entity,initially Notimplemented
        Return:
            return NotImplementError 
        """
        raise NotImplementedError


class Potion(Item):
    """ It represent and apply potion as an item entity

        Inherits from:
        Item class

        Parameters:


        functionalities:
        represent and apply potion event to the player entity 
    """

    def get_id(self):
        """ A functions which returns the ID of the POTION

        Parameters:


        functionalities:
            return id of the POTION from the constants
        Return:
            return POTION, string type
        """
        return POTION

    def apply(self, player: Player):
        """ the method apply the potion to the player entity

        Parameters:
           Instance of a player

        functionalities:
            it apply the potion to the player 
            and change the health value of the current player instance
        Return:
            None 
        """
        player.change_health(POTION_AMOUNT)


class Coin(Item):
    """ It represent and add coin as an item entity

        Inherits from:
        Item class

        Parameters:


        functionalities:
        represent and collect coin event to the player instance 
    """

    def get_id(self):
        """ A functions which returns the ID of the COIN
        Parameters:


        functionalities:
            return id of the COIN from the constants
        Return:
            return COIN, string type
        """
        return COIN

    def apply(self, player: Player):
        """ the method does not apply the anything to the player entity
        Parameters:
           player

        functionalities:
            it does not apply anything to the player
        Return:
            None 
        """
        pass


class Water(Item):
    """ It represent and apply water as an item entity

        Inherits from:
        Item class

        Parameters:


        functionalities:
        represent and apply water event to the player instance
    """

    def get_id(self):
        """ A functions which returns the ID of the water
        Parameters:


        functionalities:
            return id of the WATER from the constants
        Return:
            return WATER, string type
        """
        return WATER

    def apply(self, player: Player):
        """ the method apply the potion to the player entity

        Parameters:
           Instance of a Player

        functionalities:
            it apply the water to the player 
            and change the thirst value of the current player instance
        Return:
            None 
        """
        player.change_thirst(WATER_AMOUNT)


class Food(Item):
    """ It is an abstract class for food subclasses (apple, honey)

        Inherits from:
        Item class

        Parameters:


        functionalities:
        it takes the foods items, apply to player 
        and change the hunger value of the current player instance
    """

    def get_id(self):
        """ A functions which returns the ID of the food
        Parameters:


        functionalities:
            return id of the FOOD (of the subclasses)
        Return:
            return FOOD, string type
        """
        return FOOD

    def apply(self, player: Player):
        """ the method apply the food to the player entity

        Parameters:
           Instance of a Player

        functionalities:
            it apply the food(sub classes) to the player 
            and change the hunger value of the current player instance
        Return:
            None 
        """
        player.change_hunger(0)


class Apple(Food):
    """ It is an subclass of food which applies to player

        Inherits from:
        food class

        Parameters:


        functionalities:
        it applies to the and change the players hunger accordingly
    """

    def get_id(self):
        """ A functions which returns the ID of the Apple
        Parameters:


        functionalities:
            return id of the APPLE
        Return:
            return APPLE, string type
        """
        return APPLE

    def apply(self, player: Player):
        """ the method apply the apple to the player entity

        Parameters:
           Instance of a Player

        functionalities:
            it apply the apple to the player 
            and change the hunger value of the current player instance
        Return:
            None 
        """
        player.change_hunger(APPLE_AMOUNT)


class Honey(Food):
    """ It is an subclass of food which applies to player

        Inherits from:
        food class

        Parameters:


        functionalities:
        it applies to the and change the players hunger accordingly
    """

    def get_id(self):
        """ A functions which returns the ID of the Honey
        Parameters:


        functionalities:
            return id of the HONEY
        Return:
            return HONEY, string type
        """
        return HONEY

    def apply(self, player: Player):
        """ the method apply the honey to the player entity

        Parameters:
           Instance of a Player

        functionalities:
            it apply the honey to the player 
            and change the hunger value of the current player instance
        Return:
            None 
        """
        player.change_hunger(HONEY_AMOUNT)


class Inventory:
    """ It represents and handle all the operation of
    inventory of a player instance

        Inherits from:
        None

        Parameters:


        functionalities:
        handles , represent and update Inventory 
        of a player instance
    """

    def __init__(self, initial_items=None):
        """ A constructor for initializing a 
        Inventory of a player instance

        Parameters:
            initial_items

        functionalities:
            Initialize and handles the inventory 
            instance of the player instance
        Return:
            None
        """
        self.inv = {}
        if initial_items:  # Adding all the initial items to players inventory
            for i in initial_items:
                self.add_item(i)

    def add_item(self, item: Item):
        """ the method adds or append the items to the player

        Parameters:
           item

        functionalities:
            it takes the item and add items 
            to the inventory instance of the 
            current player instance
        Return:
            None
        """
        if item.get_name() in self.inv:
            self.inv[item.get_name()].append(item)
        else:
            self.inv[item.get_name()] = [item]

    def get_items(self):
        """ it returns of the dictionary mapping of the items

        Parameters:


        functionalities:
            the method returns the dictionary 
            mapping the names of all the items 
            in the inventory instance
        Return:
            returns self.inv , dictionary
        """
        return self.inv

    def remove_item(self, item_name: str):
        """ it remove items 

        Parameters:
           item_name

        functionalities:
            it takes the name of the 
            item and remove from the 
            inventory instance of a player instance
        Return:
           Removed Item
        """
        if item_name in self.inv:
            popped_item = self.inv[item_name].pop(0)
            if len(self.inv[item_name]) == 0:
                self.inv.pop(item_name)
            return popped_item
        return None

    '''remove_item(self, item_name: str) -> Optional[Item] (method)
        Removes and returns the first instance of the item with the 
        given item_name from the inventory. If no item exists in 
        the inventory with the given name, then this method returns None.'''

    def __str__(self):
        """ It returns the quantity of the inventory items

        Parameters:


        Functionalities:
            It returns the quantity of 
            each times of the current inventory instance
        Return:
            returns s, string
        """
        s = ""
        for i in self.inv:
            s += i + ": " + str(len(self.inv[i])) + "\n"
        return s[0:len(s) - 1]

    def __repr__(self):
        """ It returns a text that would 
        create a new instance for inventory

        Parameters:


        functionalities:
            It returns string which creates 
            instances of a new inventory of 
            same items as the current inventory contains
        Return:
            returns string
        """
        lst = []
        for i in self.inv:
            lst += self.inv[i]
        return type(self).__name__ + "(" + str(lst) + ")"


class Maze:
    """ It represents, creates & handle all the operation of Maze

        Inherits from:
        None

        Parameters:


        functionalities:
        handle the operations, create the maze from dimensions given
        represent and update Inventory 
        of a player instance
    """

    def __init__(self, dimensions):
        """ A constructor for initializing 
        empty maze of the given dimensions

        Parameters:
            dimensions

        functionalities:
            initialize and construct 
            the maze according to the dimensions
        Return:
            None
        """
        self.dimension = dimensions
        self.maze = []  # crating the maze as a 2d matrix/list
        self.door = None  # A variable to store door coordinates

    def get_dimensions(self):
        """ it returns the dimensions of the maze

        Parameters:


        functionalities:
            the method returns the 
            row and columns of the maze
        Return:
            returns self.inv , dictionary
        """
        return self.dimension

    def add_row(self, row: str):
        """ it makes the entire maze by adding rows

        Parameters:
           row

        functionalities:
            it makes the maze by taking the row, 
            place the characters as id's for the 
            tiles instance and fill the empty space
            by empty tiles

        Return:
            None
        """
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

    def get_tiles(self):
        """ it returns the current tile 
            instances in the maze

        Parameters:


        functionalities:
            the method returns the tile 
            instances by the id's in the maze 
        Return:
            returns self.maze, local list
        """
        return self.maze

    def unlock_door(self):
        """ it unlocks the door

        Parameters:


        functionalities:
           it unlocks or unblock the door tile in the current maze
        Return:
           None
        """
        self.maze[self.door[0]][self.door[1]].unlock()

    def get_tile(self, position):
        """ it gives the tile instance of a position
        Parameters:
           position

        functionalities:
            the method returns the tile 
            instance of the given position 
            in the current maze
        Return:
           None
        """
        return self.maze[position[0]][position[1]]

    def __str__(self):
        """ It returns the string representation of the current maze

        Parameters:

        functionalities:
            the method returns a string 
            representation of the maze which 
            consist of the tile instances by its ID's
        Return:
            string
        """
        s = ""
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                s += self.maze[i][j].get_id()
            s += "\n"
        return s[0:len(s) - 1]

    def __repr__(self):
        """ It returns a text that would create a new instance for inventory

        Parameters:


        functionalities:
            It returns string which creates 
            a new maze of same dimensions as 
            the current maze dimensions

        Return:
            return string
        """
        return type(self).__name__ + "(" + str(self.dimension) + ")"


class Level:
    """ It tracks player /non-player entity, 
        creates & handle Levels of the entire game

        Inherits from:
        None

        Parameters:


        functionalities:
        handle the operations, create the levels,fetch the maze , fetch inventory 
        of a player instance
    """

    def __init__(self, dimensions):
        """ A constructor for initializing a new level
        empty maze of the given dimensions

        Parameters:
            dimensions

        functionalities:
            initialize and construct 
            the a new maze for the new level according to the dimensions
        Return:
            None
        """
        self.maze = Maze(dimensions)
        self.player_start = None
        self.entities = {}

    def get_maze(self):
        """ it returns the maze instance

        Parameters:

        functionalities:
            the method returns the maze instance for the current level
        Return:
            returns self.maze
        """
        return self.maze

    def attempt_unlock_door(self):
        """ it unlock the door if no 
            coins remains in the current maze 

        Parameters:


        functionalities:
            the method unlocks the door 
            if the re no coin remaining in the current maze
        Return:
            None
        """
        for i in self.entities:
            if isinstance(self.entities[i], Coin):
                return
        self.maze.unlock_door()

    def add_row(self, row: str):
        """ it adds the tiles and entities 
            from the row to the current level

        Parameters:
            row

        functionalities:
            it makes the maze by adding 
            the tiles and entities from 
            the row to this level
        Return:
            None
        """
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

    def add_entity(self, position, entity_id: str):
        """ it adds the entities by the entity_id in 
            the current level by the given position

        Parameters:
           position,entity_id

        functionalities:
            the method add the 
            entities in the maze 
            by the entity_id's to 
            the current level
        Return:
           None
        """
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

    def get_dimensions(self):
        """ it returns the position of of the maze

        Parameters:


        functionalities:
            the method returns the rows and columns for the current level maze
        Return:
            returns self.maze.dimension
        """
        return self.maze.dimension

    def get_items(self):
        """ it returns the mapping from 
        the position to the item in the current maze

        Parameters:


        functionalities:
            the method  returns a mapping from position to the Item at that 
        position for all items currently in this level

        Return:
            returns self.entities
        """
        return self.entities

    def remove_item(self, position):
        """ it remove the item from the given position

        Parameters:
            position

        functionalities:
            the method  remove the entities 
            from the given position if present,
            from the current maze

        Return:
            None
        """
        self.entities.pop(position)

    def add_player_start(self, position):
        """ it add the player's starting 
            position to start the game

        Parameters:


        functionalities:
            the method  Adds the start position for the player in this level
        Return:
            returns self.entities
        """
        self.player_start = position

    def get_player_start(self):
        """ it return the starting position of the player 

        Parameters:


        functionalities:
            the method  returns the starting 
            position of the player for the current 
            level if no player detects it returns none
        Return:
            returns self.player_start
        """
        return self.player_start

    def __str__(self):
        """ it returns the string 
            representation of the current level

        Parameters:


        functionalities:
            the method  return the string representation
        Return:
            returns string
        """
        return "Maze: " + self.maze.__str__() + "\nItems: " + str(self.entities) + "\nPlayer start: " + str(
            self.get_player_start())

    def __repr__(self):
        """ it returns a string that would construct a level

        Parameters:


        functionalities:
            the method  returns a 
            string which creates a 
            new level instance of 
            the current level with 
            the same dimension
        Return:
            returns string
        """
        return type(self).__name__ + "(" + str(self.get_dimensions()) + ")"


class Model:
    """ It initialize & loads the entire model from the game file

        Inherits from:
        None

        Parameters:


        functionalities:
        Loads model of the entire game from the game path including levels, maze, entities
    """

    def __init__(self, game_file: str):
        """ A constructor for initializing 
            and load levels ,mazes and verification variables

        Parameters:
            game_file

        functionalities:
            Loads the game file and verify the game events
        Return:
            None
        """
        self.file = game_file
        self.levels = load_game(game_file)
        self.won = False
        self.lost = False
        self.level = 0  # signifies the current level count
        self.current_level = self.levels[self.level]  # represent the current level instance
        self.just_level_up = False
        self.valid_move = 0  # keeps track of the number of moves made by user
        self.player = Player(self.get_level().get_player_start())
        self.last_move = False  # a variable to keep track if the player has
        # reached the door and needs one more move to win

    def has_won(self):
        """ it verifies the wining of the game

        Parameters:


        functionalities:
            it returns true if the game has been won (if all levels has been successfully completed)
        Return:
           returns self.won ,boolean
        """
        return self.won

    def has_lost(self):
        """ it verifies the losing of the game

        Parameters:


        functionalities:
            it returns true if the game has been lost 
            otherwise returns False (HP too low or 
            hunger or thirst too high)

        Return:
           returns self.lost ,boolean
        """
        if self.get_player().get_health() == 0 or self.get_player().get_thirst() == MAX_THIRST or self.get_player().get_hunger() == MAX_HUNGER:
            self.lost = True
        return self.lost

    def get_winning_move(self):
        """ it ensures winning 
        Parameters:


        functionalities:
            the method confirms the wins
        Return:
           None
        """
        x, y = self.get_level().get_maze().door[0], self.get_level().get_maze().door[1]
        m, n = self.get_level().get_maze().get_dimensions()[0] - 1, self.get_level().get_maze().get_dimensions()[0] - 1
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
        """ it gives the current level

        Parameters:


        functionalities:
            it returns the current level
        Return:
           returns self.current_level
        """
        return self.current_level

    def level_up(self):
        """ it change the level to the next level

        Parameters:


        functionalities:
           Changes the level to the next 
           level in the game. If no more levels remain,
           the player has won the game.
        Return:
           returns self.won ,boolean
        """
        if self.level + 1 < len(self.levels):
            self.level += 1
            self.just_level_up = True
            self.current_level = self.levels[self.level]
            self.last_move = False
            self.get_player().set_position(self.current_level.get_player_start())

        else:
            self.won = True

    def did_level_up(self):
        """ it returns true if the player just moved to the next level

        Parameters:


        functionalities:
           Returns True if the player just 
           moved to the next level on the 
           previous turn, otherwise returns False.
        Return:
           returns self.just_level_up
        """
        return self.just_level_up

    def move_player(self, delta):
        """ Move the player , Update the players hunger, 
            Update players health,Update the players position,
            Attempt to collect any item that is on the players new position

        Parameters:
            delta

        functionalities:
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
        Levels up if the player finishes the maze by making the move.
        """
        cur_loc = self.get_player().get_position()
        new_loc = (cur_loc[0] + delta[0], cur_loc[1] + delta[1])

        if (new_loc[0] >= self.get_current_maze().get_dimensions()[0] or
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
                    self.valid_move = 0
                    self.get_player().change_hunger(1)
                    self.get_player().change_thirst(1)

                self.just_level_up = False

            if self.last_move:
                self.last_move = False
                if delta == self.get_winning_move():
                    return self.level_up()

    def attempt_collect_item(self, position):
        """ it collects the items if exist in the given position
            & unlocks the door if no coin exist

        Parameters:
            position

        functionalities:
           the method Collects the item at 
           the given position if one exists. 
           Unlocks the door if all coins have been collected.
        Return:
           None
        """
        if position in self.get_level().get_items():
            self.get_player().add_item(self.get_level().get_items()[position])
            self.get_level().remove_item(position)
        self.get_level().attempt_unlock_door()

    def get_player(self):
        """ the returns the player instance

        Parameters:


        functionalities:
           the method returns the player instance in the game
        Return:
           returns self.player
        """
        return self.player

    def get_player_stats(self):
        """ it returns the the player stats (HP,Hunger,Thirst)

        Parameters:


        functionalities:
           the method returns the stats of the current player instance
        Return:
           returns stat
        """
        stat = (self.get_player().health, self.get_player().hunger, self.get_player().thirst)
        return stat

    def get_player_inventory(self):
        """ it returns the  players inventory

        Parameters:


        functionalities:
           the method returns the inventory instance of the current player
        """
        return self.get_player().get_inventory()

    def get_current_maze(self):
        """ it returns the maze for the level

        Parameters:


        functionalities:
           it returns the current maze for the current level
        Return:
           returns self.get_level().get_maze()
        """
        return self.get_level().get_maze()

    def get_current_items(self):
        """ it returns the items of the current level

        Parameters:


        functionalities:
           Returns a dictionary mapping tuple 
           positions to the item that currently 
           exists at that position on the maze.
            Only positions at which an item exists s
            could be included in the result
        Return:
           returns self.get_level().get_items()
        """
        return self.get_level().get_items()

    def __str__(self):
        """ it returns the string 
            for constructing a instance of a model

        Parameters:


        functionalities:
            Returns the text required 
            to construct a new instance 
            of Model with the same game 
            file used to construct self
        Return:
            returns string
        """
        return type(self).__name__ + "('" + self.file + "')"

    def __repr__(self):
        """ it does the same thing as the above __str__

        Parameters:


        functionalities:
           Returns the text required 
            to construct a new instance 
            of Model with the same game 
            file used to construct self
        Return:
            returns string
        """
        return type(self).__name__ + "('" + self.file + "')"


class MazeRunner:
    """ MazeRunner is the controller class, which should
     maintain instances of the model and view, collect user input
    and facilitate communication between the model and view
    """

    def __init__(self, game_file: str, view: TextInterface):
        """ A constructor which crates a new Maze Runner game loading  the games
        Parameters:
            game_file, view

        functionalities:
            Creates a new MazeRunner game with the given view and a 
            new Model instantiated using the given game_file.
        Return:
            None
        """
        self.game = Model(game_file)
        self.view = view

        self.play()

    def play(self):
        """ This function manages all the inputs from user and operates other classes
        Parameters:
            game_file, view

        functionalities:
            Draws the game state using TextInterface, Takes user input, and according to that
            the game moves forward.
        Return:
            None
        """
        self.view.draw(self.game.get_current_maze(), self.game.get_current_items(),
                       self.game.get_player().get_position(), self.game.get_player_inventory(),
                       self.game.get_player_stats())  # Draws the game state

        while True:

            inp = input("\nEnter a move: ")  # Takes the user input

            if inp[0:2] == "i ":  # The item using scenario
                item = inp[2:]
                if item in self.game.get_player_inventory().get_items():
                    self.game.get_player_inventory().get_items()[item][0].apply(self.game.get_player())
                    self.game.get_player_inventory().remove_item(item)
                else:
                    print(ITEM_UNAVAILABLE_MESSAGE)
            elif inp.lower() == UP:  # Player movement
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

        if self.game.get_level().get_maze().door is not None and \
                self.game.get_level().get_maze().door == self.game.get_player().get_position():
            self.game.last_move = True  # Marks if the player need one more
            # move to go to next level

        if self.game.has_lost():
            print(LOSS_MESSAGE)
        elif self.game.has_won():
            print(WIN_MESSAGE)
        else:
            self.play()


def main():
    inp = input("Enter game file: ")
    MazeRunner(inp, TextInterface())


if __name__ == '__main__':
    main()
