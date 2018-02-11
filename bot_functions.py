def createListOfShot(map_size):
    """
        Membuat list dari titik yang akan ditembak
        param:
            map_size = [string] ukuran map ("small", "medium", "large")
        output: list of tuple (x,y)
    """
    # TO BE CONTINUED


def updateListOfShot(to_be_shot, last_shot):
    """ Mengupdate shot_list dengan menghapus titik yang telah ditembak (last_hit).
        param:
            last_shot = [tuple] titik yang terakhir ditembak
            to_be_shot = [list] kumpulan titik yang belum ditembak
    """
    if last_shot in to_be_shot:
        to_be_shot.remove(last_shot)


def countEffectiveShots(center, weapon, enemy_map):
    """
        Menghitung tembakan yang efektif jika diketahui center point dan jenis tembakannya
        param:
            center = [tuple] center point dari tembakan
            weapon = [string] jenis tembakannya
            enemy_map = [list of list] peta musuh berserta detilnya
        output:  integer jumlah titik shot yang belum ditembak sebelumnya
    """
    if weapon == 'DiagonalCrossShot':
    elif weapon == 'SeekerMissile':
    elif weapon == 'DoubleShotVer':
    elif weapon == 'DoubleShotVer:
    # TO BE CONTINUED


def playerShipsAttacked(player_ships):
    """
        Mengecek list kapal yang terkena tembak dari musuh tetapi belum mati
        param:
            player_ships: [array of dictionary] info-info lengkap mengenai kapal player
        output: mengembalikan list nama-nama kapal yang terkena hit tetapi belum mati
    """
    list_of_ships = []
    for ship in player_ships:
        if not ship['Destroyed']:
            i = 0
            hit = False
            while i < len(ship['Cells']) and not(hit):
                if ship['Cells']['Hit']:
                    list_of_ships.extend(ship['ShipType'])
                    hit = True
    return list_of_ships


def countEnemyShipsDestroyed(state):
    """
        Menghitung jumlah kapal musuh yang sudah mati
        param:
            state = [json] data lengkap dari file json
        output: integer jumlah kapal musuh yang masih hidup
    """
    count = 0
    for ship in state['OpponentMap']['Ships']:
        if ship['Destroyed']:
            count += 1
    return count


def generateEnemyMap(state, map_size):
    """
        Memetakan peta musuh dalam matriks
        param:
            state = [json] data lengkap dari file json
            map_size = [integer] ukuran peta game yang sedang dijalankan
        output: list of list dari peta musuh
    """
    map = []
    i = 0
    for _ in range(map_size):
        temp = []
        for _ in range(map_size):
            temp.append(state['PlayerMap']['Cells'][i])
            i += 1
        map.append(temp)
    return map

def nextOrientationHitPoint(last_shot, first_hit):
    """
        Menentukan titik yang akan diserang berikutnya jika pada satu arah tidak berhasil mengenai kapal
        param:
            last_shot = [tuple] titik terakhir yang ditembak
            first_hit = [tuple] titik pertama yang pertama kali menemukan kapal
        output: (x,y) yang merupakan titik selanjutnya yang akan ditembak
    """
    if (last_shot == first_hit):
        # pertama kali akan menentukan arah
        return (first_hit[0], first_hit[1] + 1)
    elif (last_shot[0] == first_hit[0]) and (last_shot[1] > first_hit[1]):
        # setelah menelusuri utara
        return (first_hit[0], first_hit[1] - 1)
    elif (last_shot[0] == first_hit[0]) and (last_shot[1] < first_hit[1]):
        # setelah menelusuri selatan
        return (first_hit[0] + 1, first_hit[1])
    elif (last_shot[0] > first_hit[0]) and (last_shot[1] == first_hit[1]):
        # setelah menelusuri timur
        return (first_hit[0] - 1, first_hit[1])
    # else:
    #     # setelah menelusuri barat
    #     return (-1, -1)


def nextShipHit(last_shot, first_hit):
    """
        Menentukan titik selanjutnya (pada orientasi yang sama) jika sebelumnya kena hit
        param:
            last_shot = [tuple] titik terakhir yang ditembak
            first_hit = [tuple] titik pertama yang pertama kali menemukan kapal
        output: (x,y) yang merupakan titik selanjutnya yang akan ditembak
    """
    if (last_shot[0] == first_hit[0]) and (last_shot[1] > first_hit[1]):
        # sedang menelusuri utara
        return (last_shot[0], last_shot[1] + 1)
    elif (last_shot[0] == first_hit[0]) and (last_shot[1] < first_hit[1]):
        # sedang menelusuri selatan
        return (last_shot[0], last_shot[1] - 1)
    elif (last_shot[0] > first_hit[0]) and (last_shot[1] == first_hit[1]):
        # setelah menelusuri timur
        return (last_shot[0] + 1, last_shot[1])
    elif (last_shot[0] < first_hit[0]) and (last_shot[1] == first_hit[1]):
        # setelah menelusuri barat
        return (last_shot[0] - 1, last_shot[1])


def nextSearchShot(enemy_map, to_be_shot):
    """
        Menentukan titik mana yang akan ditembak dan dengan senjata apa
        enemy_map = []
        to_be_shot = [list of tuple]
        output: (x,y) titik yang akan ditembak & jenis senjata (dalam bentuk key dari commands)
    """
    # TO BE CONTINUED 


def isLastShotHit(last_hit_count, state):
    """ Mengembalikan nilai boolean jika last hit mengenai kapal.
        param:
            last_hit_count = [integer] jumlah hit sebelumnya
            state = [json] data lengkap game dari file json
        output: boolean
    """
    return last_hit_count < getShotsHit(state)


def isCrossShotDiagonalAvail(state, charge, list_of_ships):
    """
        Mengembalikan nilai boolean apakah kita dapat menggunakan tembakan
        Cross Shot Diagonal.
        Tembakan ini dapat digunakan jika kapal Battleship masih ada di dalam
        list kapal dan memiliki 12 charge.
        param:
            state = [json] data lengkap dari file json
            charge = [integer] jumlah energi yang masih kita miliki
            list_of_ships = [list] list kapal yang kita miliki
        output: boolean bisa tidaknya senjata digunakan
    """
    return ('Battleship' in list_of_ships) and (charge <= getShotEnergy(state))


def isFireSeekerAvail(state, charge, list_of_ships):
    """ Mengembalikan nilai boolean apakah kita dapat menggunakan tembakan
        Fire seeker.
        Senjata ini dapat digunakan jika kapal Submarine masih ada di dalam
        list kapal dan memiliki 10 charge.
        param:
            state = [json] data lengkap dari file json
            charge = [integer] jumlah energi yang masih kita miliki
            list_of_ships = [list] list kapal yang kita miliki
        output: boolean bisa tidaknya senjata digunakan
    """
    return ('Submarine' in list_of_ships) and (charge <= getShotEnergy(state))


def isDoubleShotAvail(state, charge, list_of_ships):
    """ Mengembalikan nilai boolean apakah kita dapat menggunakan senjata
        Double Shot.
        Senjata ini dapat digunakan jika kapal Destroyer masih ada di dalam
        list kapal dan memiliki 8 charge.
        param:
            state = [json] data lengkap dari file json
            charge = [integer] jumlah energi yang masih kita miliki
            list_of_ships = [list] list kapal yang kita miliki
        output: boolean bisa tidaknya senjata digunakan
    """
    return ('Destroyer' in list_of_ships) and (charge <= getShotEnergy(state))


# def isOpponentKilled(count_ships_opp, list_opp_ships):
#     """ Mengembalikan nilai boolean apakah jumlah kapal lawan berkurang dari sebelumnya.
#         Membandingkan, jika length dari list_opp_ships lebih sedikit dari count_ships_opp
#         maka akan mengembalikan true.
#         param:
#             count_ships_opp = [integer] jumlah kapal sebelum tembakan terakhir
#             list_opp_ships = [list] list kapal yang dimiliki lawan
#         output: boolean apakah jumlah kapal lawan lebih sedikit dibandingkan jumlah sebelum tembakan terakhir
#     """


def isEnemyShielded(point, state):
    """
        Mengetahui apakah sebuah titik sedang di-shield oleh tidak (setelah ditembak ke titik itu)
        param:
            point = [tuple] titik yang ingin diketahui status shieldnya
            state = [json] data lengkap game dari file json
        output: boolean apakah titik tersebut dishield atau tidak
    """
    for cell in state['OpponentMap']['Cells']:
        if(cell['X'] == point[0] and cell['Y'] == point[1]):
            return cell['ShieldHit']


def isPlayerShipAlive(ship_name, player_ships):
    """
        Mencari tahu apakah sebuah kapal masih hidup atau tidak
        param:
            ship_name = [string] nama kapal
            player_ships = []
        output: boolean apakah kapal masih hidup
    """
    for ship in player_ships:
        if (ship['ShipType'] == ship_name):
            return not(ship['Destroyed'])


def isPlayerShieldActive(state):
    """
        Mengetahui apakah shield pemain sudah/masih aktif
        param:
            state = [json] data lengkap game dari file json
        output: boolean yang menyatakan shield pemain masih aktif
    """
    return state['PlayerMap']['Owner']['Shield']['Active']


def getShipWeaponEnergy(ship_name, player_ships):
    """
        Mengembalikan nilai energi yang butuhkan senjata khusus sebuah kapal
        param:
            ship_name = [string] nama kapal
            player_ships: [array of dictionary] info-info lengkap mengenai kapal player
        output: integer nilai energi senjata khusus kapal tersebut
    """
    for ship in player_ships:
        if (ship['ShipType'] == ship_name):
            return ship['Weapons'][1]['EnergyRequired']


def getShipCenterPoint(ship_name, player_ships):
    """
        Mencari titik tengah sebuah kapal
        param:
            ship_name = [string] nama kapal
            player_ships: [array of dictionary] info-info lengkap mengenai kapal player
        output: tuple (x,y) titik tengah kapal
    """
    for ship in player_ships:
        if (ship['ShipType'] == ship_name):
            ship_center = (len(ship['Cells']) - 1) // 2
            return (ship['Cells'][ship_center]['X'], ship['Cells'][ship_center]['Y'])


def getShotEnergy(state):
    """
        Mengetahui jumlah energi yang tersisa untuk menembak
        param:
            state = [json] data lengkap dari file json
        output: integer jumlah energi
    """
    return state['PlayerMap']['Owner']['Energy']


def getShotsHit(state):
    """
        Mengetahui jumlah shot hit terhadap musuh
        param:
            state = [json] data lengkap dari file json
        output: integer jumlah shot hit
    """
    return state['PlayerMap']['Owner']['ShotsFired']
