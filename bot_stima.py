import os
import json
import argparse
import bot_functions as bf

# File and path names
command_file = "command.txt"
place_ship_file = "place.txt"
game_state_file = "state.json"
output_path = '.'

# Other variables used in strategy
map_size = 0
enemy_map = []         # state-state untuk setiap kotak dalam peta musuh
player_ships = []       # state-state untuk semua kapal yang dimiliki player
enemy_ships = []        # nama-nama kapal musuh yang masih hidup
state = {}              # hasil pembacaan dari file json

# Command converter
map_size_name = {
    7: "small",
    10: "medium",
    14: "large"
}

commands = {
    'SingleShot': 1,
    'DoubleShotVer': 2,
    'DoubleShotHor': 3,
    'CornerShot': 4,
    'DiagonalCrossShot' : 5,
    'CrossShot' : 6,
    'SeekerMissile': 7,
    'Shield' : 8
}

ship_info = {
    "Battleship": 4,
    "Cruiser": 3,
    "Submarine": 3,
    "Destroyer": 2,
    "Carrier": 5
}

weapon_ship = {
    'Submarine': 'SeekerMissile',
    'Destroyer': 'DoubleShot',
    'Battleship': 'DiagonalCrossShot',
    'Carrier': 'CornerShot',
    'Cruiser': 'CrossShot'
}


def main(player_key):
    global state, map_size, to_be_shot, enemy_map, player_ships, last_enemy_ships_count, last_hit_count

    # Retrieve current game state
    json_file = open(os.path.join(output_path, game_state_file), 'r')
    state = json.load(json_file)
    json_file.close()

    map_size = state['MapDimension']
    if state['Phase'] == 1:     # Phase 1
        to_be_shot = bf.createListOfShot(map_size)
        placeShips(map_size)
    else:                       # Phase 2
        enemy_map = bf.generateEnemyMap(state, map_size)
        player_ships = state['PlayerMap']['Owner']['Ships']

        x, y, cmd = arrangingAStrategy()

        last_enemy_ships_count = bf.countEnemyShipsDestroyed(state)
        last_hit_count = bf.getShotsHit(state)

        writeCommand(x, y, cmd)


def placeShips(ukuran):
    " This is where the ships location determined "
    # ship format <Shipname> <x> <y> <direction>
    # Ship names: Battleship, Cruiser, Carrier, Destroyer, Submarine
    # Directions: north east south west

    if map_size_name[ukuran] == "small":
        ships = [
            'Battleship 1 2 north',
            'Cruiser 2 6 east',
            'Carrier 5 1 north',
            'Destroyer 3 1 north',
            'Submarine 0 0 east'
        ]
    elif map_size_name[ukuran] == "medium":
        ships = [
            'Battleship 6 2 north',
            'Cruiser 1 7 east',
            'Carrier 8 4 north',
            'Destroyer 4 3 north',
            'Submarine 1 1 east'
        ]
    elif map_size_name[ukuran] == "large":
        ships = [
            'Battleship 7 5 north',
            'Cruiser 2 10 east',
            'Carrier 10 7 east',
            'Destroyer 5 6 north',
            'Submarine 3 2 east'
        ]

    # Writing the ships location for Phase 1
    f = open(os.path.join(output_path, place_ship_file), 'w')
    for ship in ships:
        f.write(ship + "\n")
    f.close


def writeCommand(x, y, cmd):
    " Writing command to command_file text"
    f = open(os.path.join(output_path, command_file), 'w')
    f.write("%d,%d,%d\n" % (cmd, x, y))
    f.close


### PROTOTYPE ###
to_be_shot = []                 # list
found_ship = False              # mengecek apakah kita sudah menemukan sebuah kapal musuh
first_hit = (-1, -1)            # titik pertama kali menemukan kapal musuh
last_shot = (-1, -1)            # menyimpan titik (satu atau lebih) terakhir yang ditembak
last_hit_count = 0              # jumlah hit pada ronde sebelumnya sebelumnya
last_enemy_ships_count = 5      # kapal-kapal musuh yang masih ada


def arrangingAStrategy():
    """
        Fungsi utama yang menyusun strategi untuk command dan titik apa yang akan diberikan ke game engine
        output: x, y, nomor command yang akan diberikan

        ASUMSI: masih menggunakan SingleShot. Jika menggunakan DiagonalCrossShot, SeekerMissile, DoubleShot, belum tahu gimana nentuin seterusnya
    """
    global map_size, player_map, player_ships, state, enemy_ships, to_be_shot, found_ship, first_hit, last_shot, last_hit_count, last_enemy_ships_count

    ships_attacked = bf.playerShipsAttacked(player_ships)
    if ships_attacked != [] and not(bf.isPlayerShieldActive(state)):
        # ketika kapal player sudah diserang dan shield tidak aktif
        x, y = bf.getShipCenterPoint(ships_attacked[0],player_ships)
        cmd = commands['Shield']
    elif state['Round'] == 1:
        # masih ronde pertama game
        x, y = to_be_shot[0]
        last_shot = (x,y)
        bf.updateListOfShot(to_be_shot, last_shot)
        cmd = commands['SingleShot']
    else:
        got_a_hit = bf.isLastShotHit(last_hit_count, state)
        if got_a_hit and not(found_ship):
            # jika ketemu kapal musuh dan sebelumnya tidak menemukan kapal
            found_ship = True
            first_hit = last_shot
            x, y = bf.nextOrientationHitPoint(last_shot, first_hit)
            last_shot = (x,y)
            bf.updateListOfShot(to_be_shot, last_shot)
            cmd = commands['SingleShot']
        elif got_a_hit and first_hit != (-1,-1):
            # jika kapal masih ditemukan dengan orientasi yang sama dengan sebelumnya
            x, y = bf.nextShipHit(last_shot, first_hit)
            last_shot = (x,y)
            bf.updateListOfShot(to_be_shot, last_shot)
            cmd = commands['SingleShot']
        elif not(got_a_hit) and found_ship:
            # jika pada awalnya sudah menemukan kapal tetapi tembakan tidak hit
            if bf.`nemyShipsDestroyed(state) == last_enemy_ships_count:
                # jika kapal musuh yang hidup ternyata belum berkurang
                if bf.isEnemyShielded(last_shot, state):
                    # jika ternyata titik sebelumnya di-shield oleh lawan
                    x,y = last_shot
                    # tidak perlu mengupdate last_shot dan to_be_shot karena akan terus menembak di tempat yang sama sampai shield lawan deactivated
                    cmd = commands['SingleShot']
                else:
                    # mencari orientasi atau satu bagian kapal sudah dihabiskan
                    x, y = bf.nextOrientationHitPoint(last_shot, first_hit)
                    last_shot = (x,y)
                    to_be_shot = bf.updateListOfShot(to_be_shot, last_shot)
                    cmd = commands['SingleShot']
                    
                        # jika ternyata ada dua kapal yang ditembak
                        # BELUM TAHU MAU DIAPAKAN :(
                        # TO BE CONTINUED
            else:
                # jika sebuah kapal sudah dihancurkan
                found_ship = False
                first_hit = (-1,-1)     # mereset first_hit
                x, y, cmd = bf.nextSearchShot(state, to_be_shot, enemy_ships)
                last_shot = (x,y)
                to_be_shot = bf.updateListOfShot(to_be_shot, last_shot)
        else:
            # belum ketemu kapal sejak tembakan sebelumnya
            x, y, cmd = bf.nextSearchShot(state, to_be_shot, enemy_ships)
            last_shot = (x,y)
            to_be_shot = bf.updateListOfShot(to_be_shot, last_shot)

    
    return x, y, cmd

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('PlayerKey', nargs='?',
                        help='Player key registered in the game')
    parser.add_argument('WorkingDirectory', nargs='?', default=os.getcwd(
    ), help='Directory for the current game files')
    args = parser.parse_args()
    assert (os.path.isdir(args.WorkingDirectory))
    output_path = args.WorkingDirectory
    main(args.PlayerKey)
