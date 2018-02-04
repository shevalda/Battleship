# File and path names
command_file = "command.txt"
place_ship_file = "place.txt"
game_state_file = "state.json"
output_path = '.'   # NOT YET SURE
map_size = 0        # NOT YET SURE

# Command converter
commands = {
    "singleShot" : 1,
    "doubleShotVer" : 2,
    "doubleShotHor" : 3,
    "cornerShot" : 4,
    "crossDiagonalShot" : 5,
    "crossHorizontalShot" : 6,
    "seekerMissile" : 7,
    "shield" : 8
}

def place_ships():
    " This is where the ships location determined "
    # ship format <Shipname> <x> <y> <direction>
    # Ship names: Battleship, Cruiser, Carrier, Destroyer, Submarine
    # Directions: north east south west

    # TO BE CONTINUED (each ships' location)
    ships =[
        'Battleship <x> <y> <direction>',
        'Cruiser x y direction',
        'Carrier x y direction',
        'Destroyer x y direction',
        'Submarine x y direction'
    ]

    # Writing the ships location for Phase 1
    f = open(os.path.join(output_path, command_file), 'w')
    for ship in ships:
        f.write(ship + "\n")
    f.close

def write_shot(x,y,cmd):
    " Writing command to command_file text"
    f = open(os.path.join(output_path, command_file), 'w')
    f.write("%d,%d,%d\n" %(cmd, x, y))
    f.close
