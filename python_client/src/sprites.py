'''
Gets the coordinates of sprite (care of get_sprite function in GameView)
Should be updated when assets.png is modified
'''
datasprites = {
    # Normal Tiles
    "grass": (1,4),
    "sand": (3,2),
    "water": (2,2),
    "stone": (0,4),
    "none": (6, 6),

    # Rocks
    "rock_on_grass": (4, 6),
    "rock_on_stone": (5, 6),

    # Water Borders
    "water_stone_up": (0,2),
    "stone_water": (0,3),
    "water_stone_down": (0,5),
    "water_grass_up": (1,2),
    "grass_water": (1,3),
    "water_grass_down": (1,5),
    "water_sand_down": (0,7),

    # Stone to Sand
    "stone_sand_NW": (4, 2),
    "stone_sand_N": (5, 2),
    "stone_sand_NE": (6, 2),
    "stone_sand_SW": (2, 4),
    "stone_sand_S": (5, 3),
    "stone_sand_SE": (3, 4),

    # Grass to Sand
    "grass_sand_NW": (2, 3),
    "grass_sand_N": (5, 4),
    "grass_sand_NE": (3, 3),
    "grass_sand_SW": (4, 5),
    "grass_sand_S": (5, 5),
    "grass_sand_SE": (6, 5),

    # Sand Bridge
    "sand_bridge_NW": (4, 3),
    "sand_bridge_SW": (4, 4),
    "sand_bridge_NE": (6, 3),
    "sand_bridge_SE": (6, 4),

    # Highlight Color 
    "blue": (2, 5),
    "yellow": (2, 6),
    "red": (3, 5),
    "white": (3, 6),

    # Pieces
    "red_crystal": (0, 0),
    "red_broken_crystal": (1, 0),
    "red_guard": (2, 0),
    "red_mage": (3, 0),
    "red_archer": (4, 0),
    "red_longsword": (5, 0),
    "red_swordsman": (6, 0),
    "blue_crystal": (0, 1),
    "blue_broken_crystal": (1, 1),
    "blue_guard": (2, 1),
    "blue_mage": (3, 1),
    "blue_archer": (4, 1),
    "blue_longsword": (5, 1),
    "blue_swordsman": (6, 1),
    
    # Rock Obstacles <3
    "rock_on_grass": (4,6),
    "rock_on_stone": (5,6),

    # grass bridge
    "grass_bridge_UP": (5,7),
    "grass_bridge_DOWN" : (5,8),
    "grass_corner_NW":(1,7),
    "grass_corner_NE":(2,7),

    # none
    "none": (6,6)
}

# elle purposes
# default_map = [
#         list("SSSSSSSSSS"),
#         list("SSSSSSSSSS"),
#         list("SSSSSSSSSS"),
#         list("SSS{--}SSS"),
#         list("000PBBQ000"),
#         list("111$BB%111"),
#         list("///<**>///"),
#         list("GGGGGGGGGG"),
#         list("GGGGGGGGGG"),
#         list("GGG(++)GGG"),
#         list("222PBBQ222"),
#         list("333$BB%333"),
#         list(",,,[==],,,"),
#         list("SSSSSSSSSS"),
#         list("SSSSSSSSSS"),
#         list("SSSSSSSSSS"),
# ]
# tiles = {
#     '$': "sand_bridge_SW",
#     '%': "sand_bridge_SE",
#     '(': "grass_sand_NW",
#     ')': "grass_sand_NE",
#     '*': "grass_sand_S",
#     '+': "grass_sand_N",
#     ',': "stone_water",
#     '-': "stone_sand_N",
#     '/': "grass_water",
#     '0': "water_stone_down",
#     '1': "water_grass_up",
#     '2': "water_grass_down",
#     '3': "water_stone_up",
#     '<': "grass_sand_SW",
#     '=': "stone_sand_S",
#     '>': "grass_sand_SE",
#     'B': "sand",
#     'G': "grass",
#     'P': "sand_bridge_NW",
#     'Q': "sand_bridge_NE",
#     'S': "stone",
#     '[': "stone_sand_SW",
#     ']': "stone_sand_SE",
#     '{': "stone_sand_NW",
#     '}': "stone_sand_NE",
# }


# classic 16 x 10
variant1 = [
    ['stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone'],
    ['stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone'],
    ['stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone'],
    ['stone', 'stone', 'stone', 'stone_sand_NW', 'stone_sand_N', 'stone_sand_N', 'stone_sand_NE', 'stone', 'stone', 'stone'],
    ['water_stone_down', 'water_stone_down', 'water_stone_down', 'sand_bridge_NW', 'sand', 'sand', 'sand_bridge_NE', 'water_stone_down', 'water_stone_down', 'water_stone_down'],
    ['water_grass_up', 'water_grass_up', 'water_grass_up', 'sand_bridge_SW', 'sand', 'sand', 'sand_bridge_SE', 'water_grass_up', 'water_grass_up', 'water_grass_up'],
    ['grass_water', 'grass_water', 'grass_water', 'grass_sand_SW', 'grass_sand_S', 'grass_sand_S', 'grass_sand_SE', 'grass_water', 'grass_water', 'grass_water'],
    ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'],
    ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'],
    ['grass', 'grass', 'grass', 'grass_sand_NW', 'grass_sand_N', 'grass_sand_N', 'grass_sand_NE', 'grass', 'grass', 'grass'],
    ['water_grass_down', 'water_grass_down', 'water_grass_down', 'sand_bridge_NW', 'sand', 'sand', 'sand_bridge_NE', 'water_grass_down', 'water_grass_down', 'water_grass_down'],
    ['water_stone_up', 'water_stone_up', 'water_stone_up', 'sand_bridge_SW', 'sand', 'sand', 'sand_bridge_SE', 'water_stone_up', 'water_stone_up', 'water_stone_up'],
    ['stone_water', 'stone_water', 'stone_water', 'stone_sand_SW', 'stone_sand_S', 'stone_sand_S', 'stone_sand_SE', 'stone_water', 'stone_water', 'stone_water'],
    ['stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone'],
    ['stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone'],
    ['stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone']
]

# emps 19 x 13
variant2 = [
    ['grass', 'grass', 'grass', 'grass', 'grass', 'water', 'water', 'water', 'grass', 'grass', 'grass', 'grass', 'grass'], 
    ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], 
    ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], 
    ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], 
    ['water', 'grass', 'grass', 'grass', 'grass', 'water', 'water', 'water', 'grass', 'grass', 'grass', 'grass', 'water'], 
    ['water', 'water', 'grass', 'grass', 'grass', 'grass', 'water', 'grass', 'grass', 'grass', 'grass', 'water', 'water'], 
    ['water', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'water'],
    ['grass', 'grass', 'grass', 'water', 'water', 'grass', 'water', 'grass', 'water', 'water', 'grass', 'grass', 'grass'], ['grass', 'grass', 'water', 'grass', 'water', 'grass', 'water', 'grass', 'water', 'grass', 'water', 'grass', 'grass'], ['water', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'water'], ['grass', 'grass', 'water', 'grass', 'water', 'grass', 'water', 'grass', 'water', 'grass', 'water', 'grass', 'grass'], ['grass', 'grass', 'grass', 'water', 'water', 'grass', 'water', 'grass', 'water', 'water', 'grass', 'grass', 'grass'], ['water', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'water'], ['water', 'water', 'grass', 'grass', 'grass', 'grass', 'water', 'grass', 'grass', 'grass', 'grass', 'water', 'water'], ['water', 'grass', 'grass', 'grass', 'grass', 'water', 'water', 'water', 'grass', 'grass', 'grass', 'grass', 'water'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'], ['grass', 'grass', 'grass', 'grass', 'grass', 'water', 'water', 'water', 'grass', 'grass', 'grass', 'grass', 'grass']
]

variant2 = [
 ['stone', 'stone', 'stone', 'stone', 'stone', 'none', 'none', 'none', 'stone', 'stone', 'stone', 'stone', 'stone']
,['stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone']
,['stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone']
,['stone', 'stone_sand_NW', 'stone_sand_N', 'stone_sand_N', 'stone_sand_NE', 'stone', 'stone', 'stone', 'stone_sand_NW', 'stone_sand_N', 'stone_sand_N', 'stone_sand_NE', 'stone']
,['none', 'sand_bridge_NW', 'sand', 'sand', 'sand_bridge_SE', 'water_stone_down', 'water_stone_down', 'water_stone_down', 'sand_bridge_SW', 'sand', 'sand', 'sand_bridge_NE', 'none']
,['none', 'none', 'sand_bridge_NW', 'sand', 'sand', 'sand_bridge_NE', 'water_grass_up', 'sand_bridge_NW', 'sand', 'sand', 'sand_bridge_NE', 'none', 'none']
,['none', 'sand_bridge_SW', 'sand', 'sand', 'sand', 'sand', 'sand', 'sand', 'sand', 'sand', 'sand', 'sand_bridge_NE', 'none']
,['grass', 'grass_sand_S', 'grass_sand_S', 'water_sand_down', 'water_sand_down', 'grass_bridge_UP', 'water_sand_down', 'grass_bridge_UP', 'water_sand_down', 'water_sand_down', 'grass_sand_S', 'grass_sand_S', 'grass']
,['grass', 'grass', 'rock_on_grass', 'grass_corner_NE', 'water_grass_up', 'grass_bridge_DOWN', 'water_grass_up', 'grass_bridge_DOWN', 'water_grass_up', 'grass_corner_NW', 'rock_on_grass', 'grass', 'grass']
,['none', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'none']
,['grass', 'grass', 'rock_on_grass', 'grass', 'water_grass_down', 'grass_bridge_UP', 'water_grass_down', 'grass_bridge_UP', 'water_grass_down', 'grass', 'rock_on_grass', 'grass', 'grass']
,['grass', 'grass_sand_N', 'grass_sand_N', 'water_grass_down', 'water', 'grass_bridge_DOWN', 'water', 'grass_bridge_DOWN', 'water', 'water_grass_down', 'grass_sand_N', 'grass_sand_N', 'grass']
,['none', 'sand_bridge_NW', 'sand', 'sand', 'sand', 'sand', 'sand', 'sand', 'sand', 'sand', 'sand', 'sand_bridge_NE', 'none']
,['none', 'none', 'sand_bridge_SW', 'sand', 'sand', 'sand_bridge_NE', 'water_sand_down', 'sand_bridge_NW', 'sand', 'sand', 'sand_bridge_SE', 'none', 'none']      
,['none', 'sand_bridge_SW', 'sand', 'sand', 'sand_bridge_SE', 'water_sand_down', 'water', 'water_sand_down', 'sand_bridge_SW', 'sand', 'sand', 'sand_bridge_SE', 'none']
,['stone', 'stone_sand_SW', 'stone_sand_S', 'stone_sand_S', 'stone_sand_SE', 'stone_water', 'stone_water', 'stone_water', 'stone_sand_SW', 'stone_sand_S', 'stone_sand_S', 'stone_sand_SE', 'stone']
,['stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone']
,['stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone']
,['stone', 'stone', 'stone', 'stone', 'stone', 'none', 'none', 'none', 'stone', 'stone', 'stone', 'stone', 'stone']
]

# elle 16 x 21
variant3 = [
    ['stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone'] ,
    ['stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone'] ,
    ['stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone'] ,
    ['stone', 'stone', 'stone', 'stone_sand_NW', 'stone_sand_N', 'stone_sand_N', 'stone_sand_NE', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone_sand_NW', 'stone_sand_N', 'stone_sand_N', 'stone_sand_NE', 'stone', 'stone', 'stone'] ,
    ['water_stone_down', 'water_stone_down', 'water_stone_down', 'sand_bridge_NW', 'sand', 'sand', 'sand_bridge_NE', 'water_stone_down', 'water_stone_down', 'water_stone_down', 'water_stone_down', 'water_stone_down', 'water_stone_down', 'water_stone_down', 'sand_bridge_NW', 'sand', 'sand', 'sand_bridge_NE', 'water_stone_down', 'water_stone_down', 'water_stone_down'] ,
    ['water_grass_up', 'water_grass_up', 'water_grass_up', 'sand_bridge_SW', 'sand', 'sand', 'sand_bridge_SE', 'water_grass_up', 'water_grass_up', 'water_grass_up', 'water_grass_up', 'water_grass_up', 'water_grass_up', 'water_grass_up', 'sand_bridge_SW', 'sand', 'sand', 'sand_bridge_SE', 'water_grass_up', 'water_grass_up', 'water_grass_up'] ,
    ['grass_water', 'grass_water', 'grass_water', 'grass_sand_SW', 'grass_sand_S', 'grass_sand_S', 'grass_sand_SE', 'grass_water', 'grass_water', 'grass_water', 'grass_water', 'grass_water', 'grass_water', 'grass_water', 'grass_sand_SW', 'grass_sand_S', 'grass_sand_S', 'grass_sand_SE', 'grass_water', 'grass_water', 'grass_water'] ,
    ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'] ,
    ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'] ,
    ['grass', 'grass', 'grass', 'grass_sand_NW', 'grass_sand_N', 'grass_sand_N', 'grass_sand_NE', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass_sand_NW', 'grass_sand_N', 'grass_sand_N', 'grass_sand_NE', 'grass', 'grass', 'grass'] ,
    ['water_grass_down', 'water_grass_down', 'water_grass_down', 'sand_bridge_NW', 'sand', 'sand', 'sand_bridge_NE', 'water_grass_down', 'water_grass_down', 'water_grass_down', 'water_grass_down', 'water_grass_down', 'water_grass_down', 'water_grass_down', 'sand_bridge_NW', 'sand', 'sand', 'sand_bridge_NE', 'water_grass_down', 'water_grass_down', 'water_grass_down'] ,
    ['water_stone_up', 'water_stone_up', 'water_stone_up', 'sand_bridge_SW', 'sand', 'sand', 'sand_bridge_SE', 'water_stone_up', 'water_stone_up', 'water_stone_up', 'water_stone_up', 'water_stone_up', 'water_stone_up', 'water_stone_up', 'sand_bridge_SW', 'sand', 'sand', 'sand_bridge_SE', 'water_stone_up', 'water_stone_up', 'water_stone_up'] ,
    ['stone_water', 'stone_water', 'stone_water', 'stone_sand_SW', 'stone_sand_S', 'stone_sand_S', 'stone_sand_SE', 'stone_water', 'stone_water', 'stone_water', 'stone_water', 'stone_water', 'stone_water', 'stone_water', 'stone_sand_SW', 'stone_sand_S', 'stone_sand_S', 'stone_sand_SE', 'stone_water', 'stone_water', 'stone_water'] ,
    ['stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone'] ,
    ['stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone'] ,
    ['stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone'] 
]

# emps 17 x 13
variant4 = [
    ['none', 'none', 'none', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'none', 'none', 'none'] ,
    ['none', 'none', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'none', 'none'],
    ['none', 'stone_sand_N', 'stone_sand_N', 'stone_sand_N', 'stone_sand_NE', 'stone', 'stone', 'stone', 'stone_sand_NW', 'stone_sand_N', 'stone_sand_N', 'stone_sand_N', 'none'],
    ['sand_bridge_NW', 'sand', 'sand', 'sand', 'sand_bridge_NE', 'water_stone_down', 'water_stone_down', 'water_stone_down', 'sand_bridge_NW', 'sand', 'sand', 'sand', 'sand_bridge_NE'],
    ['sand_bridge_SW', 'sand', 'sand', 'sand', 'sand_bridge_SE', 'water', 'water', 'water', 'sand_bridge_SW', 'sand', 'sand', 'sand', 'sand_bridge_SE'],
    ['grass_sand_SW', 'rock_on_grass', 'grass_sand_S', 'rock_on_grass', 'grass_sand_SE', 'water_grass_up', 'water', 'water_grass_up', 'grass_sand_SW', 'rock_on_grass', 'grass_sand_S', 'rock_on_grass', 'grass_sand_SE'],
    ['grass', 'rock_on_grass', 'grass', 'rock_on_grass', 'grass', 'grass_water', 'water_grass_up', 'grass_water', 'grass', 'grass', 'rock_on_grass', 'grass', 'grass'] ,
    ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass_water', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'],
    ['grass', 'rock_on_grass', 'grass', 'rock_on_grass', 'grass', 'rock_on_grass', 'grass', 'rock_on_grass', 'grass', 'rock_on_grass', 'grass', 'rock_on_grass', 'grass']      ,
    ['grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'],
    ['grass', 'rock_on_grass', 'grass', 'rock_on_grass', 'grass', 'grass', 'water_grass_down', 'grass', 'grass', 'grass', 'rock_on_grass', 'grass', 'grass'],
    ['grass_sand_NW', 'rock_on_grass', 'grass_sand_N', 'rock_on_grass', 'grass_sand_NE', 'water_grass_down', 'water', 'water_grass_down', 'grass_sand_NW', 'rock_on_grass', 'grass_sand_N', 'rock_on_grass', 'grass_sand_NE'],
    ['sand_bridge_NW', 'sand', 'sand', 'sand', 'sand_bridge_NE', 'water', 'water', 'water', 'sand_bridge_NW', 'sand', 'sand', 'sand', 'sand_bridge_NE'],
    ['sand_bridge_SW', 'sand', 'sand', 'sand', 'sand_bridge_SE', 'water_stone_up', 'water_stone_up', 'water_stone_up', 'sand_bridge_SW', 'sand', 'sand', 'sand', 'sand_bridge_SE'],
    ['none', 'stone_sand_S', 'stone_sand_S', 'stone_sand_S', 'stone_sand_SE', 'stone_water', 'stone_water', 'stone_water', 'stone_sand_SW', 'stone_sand_S', 'stone_sand_S', 'stone_sand_S', 'none'],
    ['none', 'none', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'none', 'none'],
    ['none', 'none', 'none', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'stone', 'none', 'none', 'none']
]

'''
Configuration of textures per board variant
Texture strings should be consistent with the key in "datasprites" dict 
'''
boardtextures: dict[int,list[list[str]]] = {
    1 : variant1, 
    2 : variant2,
    3 : variant3,
    4 : variant4,
}
