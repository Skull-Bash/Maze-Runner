import a2_1


# WALL

wall = a2_1.Tile()

# print("ID :",wall.get_id())
# print("Blocked :",wall.is_blocking())
# print("Damage :",wall.damage())
# print("str :",str(wall))
# print("repr :",repr(wall))
#
# print("wall repr :",wall.__repr__())
# print("wall str :",wall.__str__())
wall.__str__()
print(wall)

# ENTITY

# ent = a2.DynamicEntity((3,6))
# print(ent.get_id())
# print(ent.get_name())
# print(ent.get_position())
# ent.set_position((6,8))
# print(ent.get_position())
# print(ent.__repr__())
# print(ent.__str__())


# ITEM

# pl = a2.Player((4,5))
# item = a2.Potion((1,4))
# print(
# pl.get_id(),
# pl.get_position(),
# pl.hunger,
# pl.health,
# pl.thirst)
# pl.change_health(-25)
# item.apply(pl)
# print(
# pl.get_id(),
# pl.get_position(),
# pl.hunger,
# pl.health,
# pl.thirst)

# Inv
#
# inv = a2.Inventory([a2.Water((2,5)),a2.Apple((5,1)),a2.Coin((4,6)),a2.Honey((4,6)),a2.Apple((4,5))])
#
#
# inv.add_item(a2.Coin((5,1)))
# inv.add_item(a2.Honey((5,6)))
# inv.add_item(a2.Water((4,1)))
# print(inv.get_items())
#
# inv.remove_item('Apple')
#
# print(inv.get_items())
#
# print(repr(inv))



# MAZE


# lvl = a2.Level((5,5))
#
# print(lvl.get_maze())
# print(lvl.get_maze().get_tiles())
# print(lvl.get_items())
# print(lvl.get_player_start())
# print(lvl.get_dimensions())
#
# lvl.add_row("#####")
# lvl.add_row("# C D")
# lvl.add_row("# C #")
# lvl.add_row("P C #")
# lvl.add_row("#####")
#
# print(lvl.get_maze())
# print(lvl.get_items())
# print(lvl.get_player_start())
# print(lvl.add_entity((2,3),'M'))
# print(lvl.get_items())
# print(lvl.attempt_unlock_door())
# print(lvl.get_maze())
# print(lvl.remove_item((1,2)))
# print(lvl.remove_item((2,2)))
# print(lvl.remove_item((3,2)))
# print(lvl.get_items())
# print(lvl.attempt_unlock_door())
# print(lvl.get_maze())
# print(lvl.get_maze().get_tiles())
# print(lvl)



# Model

# model = a2.Model('games/game1.txt')
#
# print(model.get_level())
# print(model.has_won())
# print(model.has_lost())
# print(model.did_level_up())
#
# model.move_player((0,1))
# model.move_player((0,1))
# model.move_player((-1,0))
#
# print(model.get_level())
# print(model.get_player().get_position())
# print(model.get_player_inventory().get_items())
# print(model.get_current_items())
# print(model.get_player_stats())
# print(model.get_current_maze())
# print(model.attempt_collect_item((1,2)))
# print(model.get_current_items())
# print(model.get_current_maze())
# model.level_up()
# print(model.did_level_up())
# print(model.get_current_maze())
# print(model.get_level())
# model.move_player((0,1))
# print(model.get_level())