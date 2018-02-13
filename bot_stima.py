import os
import json
import argparse
import bot_functions as bf

# File and path names
command_file = "command.txt"
place_ship_file = "place.txt"
game_state_file = "state.json"
output_path = '.'
bot_variable_file = "bot_var.json"

# Other variables used in strategy
map_size = 0                # ukuran map dari game
enemy_map = []              # state-state untuk setiap kotak dalam peta musuh
player_ships = []           # state-state untuk semua kapal yang dimiliki player
to_be_shot = []             # list titik yang akan ditembak
found_ship = False          # mengecek apakah kita sudah menemukan sebuah kapal musuh
first_hit = (-1, -1)        # titik pertama kali menemukan kapal musuh
last_shot = (-1, -1)        # menyimpan titik (satu atau lebih) terakhir yang ditembak
last_enemy_ships_count = 5  # kapal-kapal musuh yang sudah mati
possibleShipLoc = []        # list dari titik yang menandakan adanya kapal
last_command = -1           # command terakhir yang dipanggil
state = {}                  # hasil pembacaan dari file json

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

def main(player_key):
    global state, map_size, enemy_map, player_ships, to_be_shot, found_ship, first_hit, last_shot, last_enemy_ships_count, possibleShipLoc, last_command

    # Retrieve current game state
    json_file = open(os.path.join(output_path, game_state_file), 'r')
    state = json.load(json_file)
    json_file.close()

    if state['Phase'] == 1:     # Phase 1
        map_size = state['MapDimension']
        to_be_shot = bf.createListOfShot(map_size)

        # Menuliskan inisiasi semua variabel yang akan dipakai oleh bot
        putVariableInJSONFile(bot_variable_file, map_size, player_ships, to_be_shot, found_ship, first_hit, last_shot, last_enemy_ships_count, possibleShipLoc, last_command)

        # menuliskan posisi kapal
        placeShips(map_size)
    else:                       # Phase 2
        # Mengisi variabel dari round sebelumnya
        map_size, player_ships, to_be_shot, found_ship, first_hit, last_shot, last_enemy_ships_count, possibleShipLoc, last_command = getVariablefromJSON(bot_variable_file)

        enemy_map = bf.generateEnemyMap(state, map_size)        # detil peta musuh
        player_ships = state['PlayerMap']['Owner']['Ships']     # detil kapal pemain

        # Menentukan last_shot berdasarkan last_command
        # Mengupdate possibleShipLoc jika sebelumnya mendapat hit lebih dari satu
        last_shot, possibleShipLoc = bf.decideCoordinatesBeforeStrategy(last_command, last_shot, enemy_map, possibleShipLoc, to_be_shot, map_size)

        # Menyusun strategi untuk command selanjutnya
        x, y, cmd = arrangingAStrategy()

        last_enemy_ships_count = bf.countEnemyShipsDestroyed(state)     # mencatat jumlah kapal yang telah dihancurkan sebelumnya

        putVariableInJSONFile(bot_variable_file, map_size, player_ships, to_be_shot, found_ship, first_hit, last_shot, last_enemy_ships_count, possibleShipLoc, last_command)

        # BEGIN - TO BE DELETED
        putVariableInJSONFile(os.path.join(output_path, bot_variable_file), map_size, player_ships, to_be_shot, found_ship, first_hit, last_shot, last_enemy_ships_count, possibleShipLoc, last_command)
        # END - TO BE DELETED

        writeCommand(x, y, cmd)


def placeShips(ukuran):
    " This is where the ships location determined "
    # ship format <Shipname> <x> <y> <direction>
    # Ship names: Battleship, Cruiser, Carrier, Destroyer, Submarine
    # Directions: north east south west

    if ukuran == 7:     # small
        ships = [
            'Battleship 1 2 north',
            'Cruiser 2 6 east',
            'Carrier 5 1 north',
            'Destroyer 3 1 north',
            'Submarine 0 0 east'
        ]
    elif ukuran == 10:  # medium
        ships = [
            'Battleship 6 2 north',
            'Cruiser 1 7 east',
            'Carrier 8 4 north',
            'Destroyer 4 3 north',
            'Submarine 1 1 east'
        ]
    elif ukuran == 14:  # large
        ships = [
            'Battleship 7 5 north',
            'Cruiser 2 10 east',
            'Carrier 10 7 north',
            'Destroyer 5 6 north',
            'Submarine 3 2 east'
        ]

    # Writing the ships location for Phase 1
    f = open(os.path.join(output_path, place_ship_file), 'w')
    for ship in ships:
        f.write(ship + "\n")
    f.close()


def writeCommand(x, y, cmd):
    " Writing command to command_file text"
    f = open(os.path.join(output_path, command_file), 'w')
    f.write("%d,%d,%d\n" % (cmd, x, y))
    f.close()


def putVariableInJSONFile(file_name, map_size, player_ships, to_be_shot, found_ship, first_hit, last_shot, last_enemy_ships_count, possibleShipLoc, last_command):
    """
        Menuliskan variabel-variabel dalam program ke file JSON
    """
    data = {}
    data['map_size'] = map_size
    data['player_ships'] = player_ships
    data['to_be_shot'] = to_be_shot
    data['found_ship'] = found_ship
    data['first_hit'] = first_hit
    data['last_shot'] = last_shot
    data['last_enemy_ships_count'] = last_enemy_ships_count
    data['possibleShipLoc'] = possibleShipLoc
    data['last_command'] = last_command

    fn = open(file_name, 'w')
    json.dump(data, fn)
    fn.close()


def getVariablefromJSON(file_name):
    """
        Memasukkan nilai variabel dari file JSON ke program
    """
    fn = open(file_name, 'r')
    data = json.load(fn)
    fn.close()

    map_size = data['map_size']
    player_ships = data['player_ships']
    to_be_shot = data['to_be_shot']
    found_ship = data['found_ship']
    first_hit = data['first_hit']
    last_shot = data['last_shot']
    last_enemy_ships_count = data['last_enemy_ships_count']
    possibleShipLoc = data['possibleShipLoc']
    last_command = data['last_command']

    return map_size, player_ships, to_be_shot, found_ship, first_hit, last_shot, last_enemy_ships_count, possibleShipLoc, last_command


def arrangingAStrategy():
    """
        Fungsi utama yang menyusun strategi untuk command dan titik apa yang akan diberikan ke game engine
        output: x, y, nomor command yang akan diberikan
    """
    global state, map_size, enemy_map, player_ships, to_be_shot, found_ship, first_hit, last_shot, last_enemy_ships_count, possibleShipLoc, last_command, commands

    if state['Round'] == 1:     # masih ronde pertama game
        x, y = to_be_shot[0]
        last_shot = (x,y)
        cmd = commands['SingleShot']
    else:                       # player akan menembak
        got_a_hit = bf.isLastShotHit(last_shot,enemy_map)
        if got_a_hit and not(found_ship):           # jika ketemu kapal musuh dan sebelumnya tidak menemukan kapal
            found_ship = True
            first_hit = last_shot
            x, y = bf.nextOrientationHitPoint(last_shot, first_hit, map_size)
            cmd = commands['SingleShot']
            last_shot = (x,y)
        elif got_a_hit and first_hit != (-1,-1):    # jika kapal masih ditemukan dengan orientasi yang sama dengan sebelumnya
            if bf.isEnemyShipKilled(state, last_enemy_ships_count):     # jika ternyata kapal musuh sudah berkurang
                if len(possibleShipLoc) != 0:       # masih ada kapal lain yang telah diketahui keberadaannya
                    first_hit = possibleShipLoc[0]
                    last_shot = first_hit
                    possibleShipLoc.remove(possibleShipLoc[0])
                    x, y = bf.nextOrientationHitPoint(last_shot, first_hit, map_size)
                    cmd = commands['SingleShot']
                    if (x,y) == (-1,-1):
                        x,y,cmd = bf.nextSearchShot(enemy_map, to_be_shot, map_size, state, player_ships)
                        found_ship = False
                    last_shot = (x,y)
                else:                               # jika belum ada kapal lain yang lokasinya diketahui
                    found_ship = False
                    first_hit = (-1,-1)     # mereset first_hit
                    x, y, cmd = bf.nextSearchShot(enemy_map, to_be_shot, map_size, state, player_ships)
                    last_shot = (x,y)
            else:                                                       # jika ternyata kapal musuh masih belum mati
                x, y = bf.nextShipHit(last_shot, first_hit, map_size)
                last_shot = (x,y)
                cmd = commands['SingleShot']
        elif not(got_a_hit) and found_ship:         # jika pada awalnya sudah menemukan kapal tetapi tembakan tidak hit
            if bf.isEnemyShielded(last_shot, state):
                # jika ternyata titik sebelumnya di-shield oleh lawan
                x,y = last_shot
                
                # tidak perlu mengupdate last_shot dan to_be_shot karena akan terus menembak di tempat yang sama sampai shield lawan deactivated
                
                cmd = commands['SingleShot']
            else:                                                       # mencari orientasi atau satu bagian kapal sudah dihabiskan
                x, y = bf.nextOrientationHitPoint(last_shot, first_hit, map_size)
                cmd = commands['SingleShot']
                if (x,y) == (-1,-1):
                    x,y,cmd = bf.nextSearchShot(enemy_map, to_be_shot, map_size, state, player_ships)
                    found_ship = False
                last_shot = (x,y)
        else:                                       # belum ketemu kapal sejak tembakan sebelumnya
            x, y, cmd = bf.nextSearchShot(enemy_map, to_be_shot, map_size, state, player_ships)
            last_shot = x,y

    if ((x,y) in possibleShipLoc) and cmd != commands['Shield']:        # jika ternyata titik berada di kapal yang sedang diserang
        possibleShipLoc.remove((x,y))
    last_command = cmd
    return x, y, cmd


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('PlayerKey', nargs='?', help='Player key registered in the game')
    parser.add_argument('WorkingDirectory', nargs='?', default=os.getcwd(), help='Directory for the current game files')
    args = parser.parse_args()
    assert (os.path.isdir(args.WorkingDirectory))
    output_path = args.WorkingDirectory
    main(args.PlayerKey)
