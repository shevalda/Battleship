def decideCoordinatesBeforeStrategy(cmd, point, enemy_map, possibleShipLoc, to_be_shot, map_size):
    """
        - Menentukan apakah point mana yang akan diberikan sebagai last_shot ke fungsi arrangingAStrategy
        - Mengupdate list possibleShipLoc
        param:
            cmd = [integer] kunci dari shot sebelumnya
            point = [tuple of integer] center point yang ditembak pada ronde sebelumnya
            enemy_map = [tuple of dictionary] detil peta musuh
            possibleShipLoc = [tuple of integer] titik-titik pertama menemukan sebuah kapal
        output: (x,y) yang akan dijadikan last_shot yang diberikan ke fungsi arrangingAStrategy & list titik-titik yang mungkin menjadi lokasi kapal lain
    """
    last_shot = (-1,-1)
    if cmd == 1:        # single shot
        to_be_shot = updateListOfShot(to_be_shot, point)
        last_shot = point
    elif cmd == 5:      # diagonal cross shot
        if (not enemy_map[point[0]][point[1]]['Missed']):           # center point
            possibleShipLoc.append((point[0], point[1]))
        to_be_shot = updateListOfShot(to_be_shot, (point[0], point[1]))

        if (point[0]-1 >= 0) and (point[1]+1 < map_size):           # north west
            if (not enemy_map[point[0]-1][point[1]+1]['Missed']):
                possibleShipLoc.append((point[0]-1, point[1]+1))
        to_be_shot = updateListOfShot(to_be_shot, (point[0]-1, point[1]+1))

        if (point[0]+1 < map_size) and (point[1]+1 < map_size):     # north east
            if (not enemy_map[point[0]+1][point[1]+1]['Missed']):
                possibleShipLoc.append((point[0]+1, point[1]+1))
        to_be_shot = updateListOfShot(to_be_shot, (point[0]+1, point[1]+1))

        if (point[0]+1 < map_size) and (point[1]-1 >= 0):           # south east
            if (not enemy_map[point[0]+1][point[1]-1]['Missed']):
                possibleShipLoc.append((point[0]+1, point[1]-1))
        to_be_shot = updateListOfShot(to_be_shot, (point[0]+1, point[1]-1))

        if (point[0]-1 >= 0) and (point[1]-1 >= 0):                 # south west
            if (not enemy_map[point[0]-1][point[1]-1]['Missed']):
                possibleShipLoc.append((point[0]-1, point[1]-1))
        to_be_shot = updateListOfShot(to_be_shot, (point[0]-1, point[1]-1))
        
        if len(possibleShipLoc) != 0:
            last_shot = possibleShipLoc[0]
            possibleShipLoc.remove(last_shot)
        else:
            last_shot = point
    elif cmd == 7:  # seeker missile
        last_shot = (-1,-1)
        # mengecek apakah ada shot yang hit dari fire seeker
        i = point[0] - 2
        while (i <= point[0]+2) and (last_shot == (-1,-1)):
            j = point[1] - 2
            while (j <= point[1]+2) and (last_shot == (-1,-1)):
                if (i >= 0) and (j >= 0) and (i < map_size) and (i < map_size):
                    if enemy_map[i][j]['Damaged']:
                        last_shot = (i,j)
                j += 1
            i += 1
        if (last_shot != (-1,-1)):      # jika ada satu titik yang hit
            to_be_shot = updateListOfShot(to_be_shot, last_shot)
        else:                           # jika tidak ada titik yang hit
            for i in range(point[0]-2, point[1]+2+1):
                for j in range(point[1]-2, point[1]+2+1):
                    to_be_shot = updateListOfShot(to_be_shot, (i,j))
            last_shot = point

    return last_shot, possibleShipLoc

def createListOfShot(map_size):
    """
        Membuat list dari titik yang akan ditembak
        param:
            map_size = [int] ukuran map (7 (small), 10 (medium), 14 (large))
        output: list of tuple (x,y)
    """
    to_be_shot = []

    if (map_size == 7)  : #panjang dan lebar peta adalah genap
        min = 0
        max = map_size - 1 #panjang petanya - 1

        while (max >= min):
            (x,y) = (min,min)
            to_be_shot.append((x,y))
            while (x+2 <= max)  :
                x= x+2
                to_be_shot.append((x,y))
                if (y != x) :
                    to_be_shot.append((y,x))
            y = y+2
            while (y<=max) :
                to_be_shot.append((x,y))
                if (y != x) :
                    to_be_shot.append ((y,x))
                y = y+2
            max = max - 1
            min = min + 1
        min = 0
        max = map_size - 1
        add = 0
        while (y < max) :
            x = min +1 + add
            y = min + add
            while (x <= max) :
                to_be_shot.append((x,y))
                if (y != x) :
                    to_be_shot.append ((y,x))
                x = x + 2
            add = add + 1
    else :
        min = 0
        max = map_size - 1 #panjang petanya - 1
        while (max > min):
            (x,y) = (min,min)
            to_be_shot.append((x,y))

            while (x+2 < max)  :
                x= x+2
                to_be_shot.append((x,y))
                if (y != x) :
                    to_be_shot.append((y,x))
            x = x+1
            y = y+1
            while (y<=max) :
                to_be_shot.append((x,y))
                if (y != x) :
                    to_be_shot.append ((y,x))
                y = y+2
            max = max - 1
            min = min + 1
        min = 0
        max = map_size - 1 #panjang petanya - 1
        add = 0
        x = min +1 + add
        y = min + add
        while (y < max) :
            x = min +1 + add
            y = min + add
            while (x <= max) :
                to_be_shot.append((x,y))
                if (y != x) :
                    to_be_shot.append ((y,x))
                x = x + 2
            add = add + 1
    return to_be_shot

def updateListOfShot(to_be_shot, last_shot):
    """ Mengupdate shot_list dengan menghapus titik yang telah ditembak (last_hit).
        param:
            last_shot = [tuple] titik yang terakhir ditembak
            to_be_shot = [list] kumpulan titik yang belum ditembak
    """
    if last_shot in to_be_shot:
        to_be_shot.remove(last_shot)
    return to_be_shot


def countEffectiveShots(center, weapon, enemy_map, map_size):
    """
        Menghitung tembakan yang efektif jika diketahui center point dan jenis tembakannya
        param:
            center = [tuple] center point dari tembakan
            weapon = [string] jenis tembakannya
            enemy_map = [list of list] peta musuh berserta detilnya
        output:  integer jumlah titik shot yang belum ditembak sebelumnya
    """
    count = 0
    if weapon == 'DiagonalCrossShot':
        if not isPointHasBeenShot((center[0]-1, center[1]+1), enemy_map) and (center[0]-1 >= 0 and center[1]+1 < map_size):
            count += 1
        if not isPointHasBeenShot((center[0]-1, center[1]-1), enemy_map) and (center[0]-1 >= 0 and center[1]-1 >=0):
            count += 1
        if not isPointHasBeenShot((center[0]+1, center[1]+1), enemy_map) and (center[0]+1 < map_size and center[1]+1 < map_size):
            count += 1
        if not isPointHasBeenShot((center[0]+1, center[1]-1), enemy_map) and (center[0]+1 < map_size and center[1]-1 >= 0):
            count += 1
        if not isPointHasBeenShot(center, enemy_map):
            count += 1
    elif weapon == 'SeekerMissile':
        for i in range (-2,2+1):
            for j in range (-2,2+1):
                if (i >= 0 and j >= 0) and (i < map_size and j < map_size):
                    if not isPointHasBeenShot((center[0]+i,center[1]+j), enemy_map):
                        count += 1
    return count


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
                if ship['Cells'][i]['Hit']:
                    list_of_ships.append(ship['ShipType'])
                    hit = True
                i += 1
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
            temp.append(state['OpponentMap']['Cells'][i])
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


def nextSearchShot(enemy_map, to_be_shot, map_size, state, player_ships):
    """
        Menentukan titik mana yang akan ditembak dan dengan senjata apa
        enemy_map = []
        to_be_shot = [list of tuple]
        output: (x,y) titik yang akan ditembak & jenis senjata (dalam bentuk key dari commands)
    """
    dummy = (-1,-1)
    center = dummy
    i = 0
    if isCrossShotDiagonalAvail(state, getShipWeaponEnergy('Battleship', player_ships), player_ships):
        max = countEffectiveShots(to_be_shot[i],'DiagonalCrossShot', enemy_map, map_size)
        while (max<5 and i<len(to_be_shot)):
            i += 1
            max = countEffectiveShots(to_be_shot[i],'DiagonalCrossShot', enemy_map, map_size)
        if (max == 5):
            center = to_be_shot[i]

    if (center == dummy):
        i = 0
        if isFireSeekerAvail(state, getShipWeaponEnergy('Submarine', player_ships), player_ships):
            max = countEffectiveShots(to_be_shot[i],'SeekerMissile', enemy_map, map_size)
            while (max<25 and i<len(to_be_shot)):
                i += 1
                max = countEffectiveShots(to_be_shot[i],'SeekerMissile', enemy_map, map_size)
            if (max == 25):
                center = to_be_shot[i]

    if (center == dummy):
        x,y = to_be_shot[0]
        cmd = 1
    else :
        x,y = to_be_shot[i]
        if (max ==25):
            cmd = 7
        elif (max == 5):
            cmd = 5
    
    return x, y, cmd


def isEnemyShipKilled(state, last_enemy_ships_count):
    """
        Mengetahui apakah kapal musuh sudah mati satu
        param:
            state = [json]
            last_enemy_ships_count = [integer] jumlah kapal musuh yang masih hidup
        output: boolean
    """
    return countEnemyShipsDestroyed(state) < last_enemy_ships_count


def isPointHasBeenShot (point, enemy_map):
    """
        Mengetahui apakah sebuah titik pernah ditembak sebelumnya
        param:
            point = [tuple] titik yang dicek
            enemy_map = [list of list] detil peta musuh
        output: boolean
    """
    return (enemy_map[point[0]][point[1]]['Damaged'] and not(enemy_map[point[0]][point[1]]['Missed'])) or (not(enemy_map[point[0]][point[1]]['Damaged']) and enemy_map[point[0]][point[1]]['Missed'])


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
    return state['PlayerMap']['Owner']['ShotsHit']
