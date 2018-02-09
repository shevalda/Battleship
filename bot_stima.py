import os
import json

# File and path names
command_file = "command.txt"
place_ship_file = "place.txt"
game_state_file = "state.json"
output_path = '.'

# Other variables used in strategy
map_size = 0
player_map = []         # state-state untuk setiap kotak dalam peta player
player_ships = []       # state-state untuk semua kapal yang dimiliki player
enemy_ships = []        # nama-nama kapal musuh yang masih hidup
state = {}              # hasil pembacaan dari file json

# Command converter
map_size_name = {
    7 : "small",
    10 : "medium",
    14 : "large"
}

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

ship_info = {
    "Battleship" : 4,
    "Cruiser" : 3,
    "Submarine" : 3,
    "Destroyer" : 2,
    "Carrier" : 5
}

def main(player_key):
    global map_size, player_map, player_ships, state, enemy_ships
    
    # Retrieve current game state
    json_file = open(os.path.join(output_path, game_state_file), 'r')
    state = json.load(json_file)
    json_file.close()

    map_size = state['MapDimension']
    if state['Phase'] == 1:     # Phase 1
        placeShips(map_size)
    else:                       # Phase 2
        player_map = state['PlayerMap']['Cells']
        player_ships = state['PlayerMap']['Owner']['Ships']

        x, y, cmd = arrangingAStrategy()

        enemy_ships = [ship['ShipType'] for ship in state['OpponentMap']['Ships'] if not(ship['Destroyed'])]

        writeCommand(x,y,cmd)

def placeShips(ukuran):
    " This is where the ships location determined "
    # ship format <Shipname> <x> <y> <direction>
    # Ship names: Battleship, Cruiser, Carrier, Destroyer, Submarine
    # Directions: north east south west

    if (map_size_name[ukuran] == "small"):
        ships = [
            'Battleship 1 2 north',
            'Cruiser 2 6 east',
            'Carrier 5 1 north',
            'Destroyer 3 1 north',
            'Submarine 0 0 east'
        ]
    elif (map_size_name[ukuran] == "medium"):
        ships = [
            'Battleship 6 2 north',
            'Cruiser 1 7 east',
            'Carrier 8 4 north',
            'Destroyer 4 3 north',
            'Submarine 1 1 east'
        ]
    elif (map_size_name[ukuran] == "large"):
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

    return

def writeCommand(x,y,cmd):
    " Writing command to command_file text"
    f = open(os.path.join(output_path, command_file), 'w')
    f.write("%d,%d,%d\n" %(cmd, x, y))
    f.close

### PROTOTYPE ###
to_be_shot = []
found_ship = False      # mengecek apakah kita sudah menemukan sebuah kapal musuh
first_hit = (-1,-1)     # titik pertama kali menemukan kapal musuh
last_shot = (-1,-1)     # menyimpan titik terakhir yang ditembak
last_hit_count = 0      # jumlah hit pada ronde sebelumnya sebelumnya
enemy_ships = []        # kapal-kapal musuh yang masih ada

def getPhase():
    """
        Menentukan phase apa sekarang
        output: integer phase sekarang
    """
    global state
    return state['Phase']

def arrangingAStrategy():
    """
        Fungsi utama yang menyusun strategi untuk command dan titik apa yang akan diberikan ke game engine
        output: x, y, command yang akan diberikan
    """
    global map_size, player_map, player_ships, state, enemy_ships

def createListOfShot(map_size):
    """
        Membuat list dari titik yang akan ditembak
        param:
            map_size = [string] ukuran map ("small", "medium", "large")
        output: list of tuple (x,y)
    """

def updateListOfShot(shot_list, last_hit):
    """ Mengupdate shot_list dengan menghapus titik yang telah ditembak (last_hit).
        param:
            last_hit = [tuple] titik yang terakhir ditembak
            shot_list = [list] kumpulan titik yang belum ditembak
        output: list of tuple (x,y) koordinat yang belum ditembak
    """

def countEffectiveShots(center, weapon):
    """
        Menghitung tembakan yang efektif jika diketahui center point dan jenis tembakannya
        param:
            center = [tuple] center point dari tembakan
            weapon = [string] jenis tembakannya
        output:  integer jumlah titik shot yang belum ditembak sebelumnya
    """

def isLastShotHit (last_hit, map):
    """ Mengembalikan nilai boolean jika last hit mengenai kapal.
        param:
            last_hit = [tuple] titik terakhir menembak
            map = [list of char] peta musuh yang diberikan oleh game engine
        output: boolean
    """

def isCrossShotDiagonalAvail (charge, list_of_ships) :
    """
        Mengembalikan nilai boolean apakah kita dapat menggunakan tembakan
        Cross Shot Diagonal.
        Tembakan ini dapat digunakan jika kapal Battleship masih ada di dalam
        list kapal dan memiliki 12 charge.
        param:
            charge = [integer] jumlah energi yang masih kita miliki
            list_of_ships = [list] list kapal yang kita miliki
        output: boolean bisa tidaknya senjata digunakan
    """

def isFireSeekerAvail (charge, list_of_ships) :
    """ Mengembalikan nilai boolean apakah kita dapat menggunakan tembakan
        Fire seeker.
        Senjata ini dapat digunakan jika kapal Submarine masih ada di dalam
        list kapal dan memiliki 10 charge.
        param:
            charge = [integer] jumlah energi yang masih kita miliki
            list_of_ships = [list] list kapal yang kita miliki
        output: boolean bisa tidaknya senjata digunakan
    """

def isDoubleShotAvail (charge, list_of_ships) :
    """ Mengembalikan nilai boolean apakah kita dapat menggunakan senjata
        Double Shot.
        Senjata ini dapat digunakan jika kapal Destroyer masih ada di dalam
        list kapal dan memiliki 8 charge.
        param:
            charge = [integer] jumlah energi yang masih kita miliki
            list_of_ships = [list] list kapal yang kita miliki
        output: boolean bisa tidaknya senjata digunakan
    """

def isOpponentKilled (count_ships_opp, list_opp_ships) :
    """ Mengembalikan nilai boolean apakah jumlah kapal lawan berkurang dari sebelumnya.
        Membandingkan, jika length dari list_opp_ships lebih sedikit dari count_ships_opp
        maka akan mengembalikan true.
        param:
            count_ships_opp = [integer] jumlah kapal sebelum tembakan terakhir
            list_opp_ships = [list] list kapal yang dimiliki lawan
        output: boolean apakah jumlah kapal lawan lebih sedikit dibandingkan jumlah sebelum tembakan terakhir
    """
    
def isOpponentShielded (point):
    """ Mengembalikan nilai boolean true jika titik yang player tembak sedang dilindungi.
        Param:
            point = [tuple] titik yang player tembak
        output: boolean dilindungi atau tidaknya titik yang ditembak
    """
    
def isShieldNeeded():
    """
    """

def isPlayerShipAlive(ship_name):
    """
        Mencari tahu apakah sebuah kapal masih hidup atau tidak
        param:
            ship_name = [string] nama kapal
        output: boolean apakah kapal masih hidup
    """
    global player_ships

    for ship in player_ships:
        if (ship['ShipType'] == ship_name):
            return not(ship['Destroyed'])

def isPointAHit(point):
    """
        Mengetahui apakah sebuah titik terjadi hit atau tidak setelah sebuah tembakan di titik itu
        param:
            point = [tuple] titik yang ingin diketahui status hitnya
        output: boolean apakah tembakan sebelumnya ada hit atau tidak
    """
    global state

    for cell in state['OpponentMap']['Cells']:
        if(cell['X'] == point[0] and cell['Y'] == point[1]):
            return cell['Damaged'] and not(cell['Missed'])

def isEnemyPointShielded(point):
    """
        Mengetahui apakah sebuah titik sedang di-shield oleh tidak (setelah ditembak ke titik itu)
        param:
            point = [tuple] titik yang ingin diketahui status shieldnya
        output: boolean apakah titik tersebut dishield atau tidak
    """
    global state

    for cell in state['OpponentMap']['Cells']:
        if(cell['X'] == point[0] and cell['Y'] == point[1]):
            return cell['ShieldHit']

def isPlayerShieldActive():
    """
        Mengetahui apakah shield pemain sudah/masih aktif
        output: boolean yang menyatakan shield pemain masih aktif
    """
    global state

    return state['PlayerMap']['Owner']['Shield']['Active']

def getShipWeaponEnergy(ship_name):
    """
        Mengembalikan nilai energi yang butuhkan senjata khusus sebuah kapal
        param:
            ship_name = [string] nama kapal
        output: integer nilai energi senjata khusus kapal tersebut
    """
    global player_ships

    for ship in player_ships:
        if (ship['ShipType'] == ship_name):
            return ship['Weapons'][1]['EnergyRequired']

def getShipCenterPoint(ship_name, list_of_ship):
    """
        Mencari titik tengah sebuah kapal
        param:
            ship_name = [string] nama kapal
            list_of_ship = [list of dictionary] state-state kapal yang dimiliki player
        output: tuple (x,y) titik tengah kapal
    """

    for ship in list_of_ship:
        if (ship['ShipType'] == ship_name):
            ship_center = (len(ship['Cells']) - 1) // 2
            return (ship['Cells'][ship_center]['X'], ship['Cells'][ship_center]['Y'])

def getShotEnergy():
    """
        Mengetahui jumlah energi yang tersisa untuk menembak
        output: integer jumlah energi
    """
    global state

    return state['PlayerMap']['Owner']['Energy']

def getShotsHit():
    """
        Mengetahui jumlah shot hit terhadap musuh
        output: integer jumlah shot hit
    """
    global state

    return state['PlayerMap']['Owner']['ShotsFired']