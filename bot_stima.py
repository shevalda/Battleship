import os

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

ship_size = {
    "Battleship" : 4,
    "Cruiser" : 3,
    "Submarine" : 3,
    "Destroyer" : 2,
    "Carrier" : 5
}

ships_location = {
    "small" : {
        "Battleship" : [],
        "Cruiser" : [],
        "Submarine" : [],
        "Destroyer" : [],
        "Carrier" : []
        },
    "medium" : {
        "Battleship" : [],
        "Cruiser" : [],
        "Submarine" : [],
        "Destroyer" : [],
        "Carrier" : []
        },
    "large" : {
        "Battleship" : [],
        "Cruiser" : [],
        "Submarine" : [],
        "Destroyer" : [],
        "Carrier" : []
        }     
    }

def placeShips(ukuran):
    " This is where the ships location determined "
    # ship format <Shipname> <x> <y> <direction>
    # Ship names: Battleship, Cruiser, Carrier, Destroyer, Submarine
    # Directions: north east south west

    if (ukuran == "small"):
        ships = [
            'Battleship 1 2 south',
            'Cruiser 2 0 east',
            'Carrier 5 1 south',
            'Destroyer 3 4 south',
            'Submarine 0 6 east'
        ]
    elif (ukuran == "medium"):
        # ships = [
        #     'Battleship <x> <y> <direction>',
        #     'Cruiser x y direction',
        #     'Carrier x y direction',
        #     'Destroyer x y direction',
        #     'Submarine x y direction'
        # ]
    elif (ukuran == "large"):
        # ships = [
        #     'Battleship <x> <y> <direction>',
        #     'Cruiser x y direction',
        #     'Carrier x y direction',
        #     'Destroyer x y direction',
        #     'Submarine x y direction'
        # ]

    # Writing the ships location for Phase 1
    f = open(os.path.join(output_path, command_file), 'w')
    for ship in ships:
        f.write(ship + "\n")
    f.close

def writeShot(x,y,cmd):
    " Writing command to command_file text"
    f = open(os.path.join(output_path, command_file), 'w')
    f.write("%d,%d,%d\n" %(cmd, x, y))
    f.close

### PROTOTYPE ###
found_ship = False          # mengecek apakah kita sudah menemukan sebuah kapal musuh
first_hit = (-1,-1)         # titik pertama kali menemukan kapal musuh
last_hit = (-1,-1)          # menyimpan titik terakhir yang ditembak
hit_orientation = "n"       # menyimpan orientasi tembakan dalam urutan atas, bawah, kanan, kiri
list_of_enemy_ship = []     # kapal-kapal musuh yang masih ada

def isLastShotHit (last_hit, map):
    """ Mengembalikan nilai boolean jika last hit mengenai kapal.
        param:
            last_hit = [tuple] titik terakhir menembak
            map = [list of char] peta musuh yang diberikan oleh game engine
        output: boolean
    """
def createListOfShot(ukuran):
    """
        Membuat list dari titik yang akan ditembak
        param:
            ukuran = [string] ukuran map ("small", "medium", "large")
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

    
def isShipDamage(ships):
    """
    """
    
    
def isShieldNeeded()


