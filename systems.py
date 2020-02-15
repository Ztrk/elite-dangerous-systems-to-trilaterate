from math import sqrt
from time import sleep
import re
import requests
from yaml import load, dump, CLoader as Loader, CDumper as Dumper

NEW_SECTORS_ALLOWED = False

def to_number(letter):
    return ord(letter) - ord('A')

def get_systems(name, multiple=True):
    sleep(2)
    if multiple:
        url = 'https://www.edsm.net/api-v1/systems'
    else:
        url = 'https://www.edsm.net/api-v1/system'
    system_name = {'systemName': name, 'showCoordinates': 1, 'onlyKnownCoordinates': 1}
    response = requests.get(url, system_name)
    print(name, 'Systems in response:', len(response.json()))
    return response.json()

def get_system_coords(name):
    systems = get_systems(name)
    if len(systems) > 0:
        return systems[0]['coords']
    return None

class Sector:
    sector_size = 1280
    sectors_origin = (-65, -25, 215)

    def __init__(self, name, coordinates=None, hand_placed=False):
        self.name = name
        self.origin = coordinates
        self.hand_placed = hand_placed
    
    def __repr__(self):
        return 'Sector({}, {}, {})'.format(self.name, self.origin, self.hand_placed)

    def get_origin(self, size):
        if self.origin is None:
            coords = get_system_coords(self.name + ' AA-A')
            if coords is None:
                coords = get_system_coords(self.name + ' AA')
            if coords is None:
                coords = get_system_coords(self.name + ' A')
            if coords is None:
                coords = get_system_coords(self.name + ' ')
            if coords is None:
                self.origin = (1000000, 1000000, 1000000)
                return self.origin

            sector_coords = [coords['x'], coords['y'], coords['z']]
            for i in range(len(sector_coords)):
                sector_coords[i] -= (sector_coords[i] - self.sectors_origin[i]) % self.sector_size

            self.origin = tuple(sector_coords)

        if self.hand_placed:
            coords = list(self.origin)
            for i in range(len(coords)):
                coords[i] -= (coords[i] - self.sectors_origin[i]) % size
            return coords
        return self.origin


class System:
    def __init__(self, name, use_edsm=False):
        self.name = name
        self.relative = (0, 0, 0)
        self.coordinates = (0, 0, 0)
        self.error = 5000
        self.masscode = None
        if use_edsm:
            self.coordinates = self.coordinates_from_edsm()
        else:
            self.coordinates = self.coordinates_from_name()
    
    def distance(self, other):
        dist = 0
        for c1, c2 in zip(self.coordinates, other.coordinates):
            dist += (c1 - c2) ** 2
        return sqrt(dist)

    def coordinates_from_edsm(self):
        response = get_systems(self.name, multiple=False)
        if len(response) > 0:
            coords = response['coords']
            return (coords['x'], coords['y'], coords['z'])
        else:
            return (0, 0, 0)

    def coordinates_from_name(self):
        match = re.search(r'([A-Z]{2}-[A-Z]) ([a-h])(\d+)(-\d+)?', self.name)
        if match is None:
            return self.coordinates

        self.masscode = match.group(2)
        size = 10 * 2 ** (ord(self.masscode) - ord('a'))
        origin = get_origin(self.name[:match.start() - 1], size)

        letter_code = match.group(1)
        if match.group(4) is None:
            number = 0
        else:
            number = int(match.group(3))
        index = (26 * 26 * 26 * number + 26 * 26 * to_number(letter_code[3])
            + 26 * to_number(letter_code[1]) + to_number(letter_code[0]))

        self.relative = (size * (index % 128), size * (index//128 % 128), size * (index//(128 * 128)))
        self.coordinates = (origin[0] + size/2 + self.relative[0],
            origin[1] + size/2 + self.relative[1], origin[2] + size/2 + self.relative[2])
        self.error = size/2
        return self.coordinates

def read_sectors(filename):
    print('Reading sectors')
    with open(filename, 'r') as file:
        data = load(file, Loader=Loader)
    if data is None:
        return {}
    return data

def write_sectors(filename, sectors):
    print('Writing sectors')
    with open(filename, 'w') as file:
        dump(sectors, file, Dumper=Dumper)
    print('Sectors written')

def get_origin(name, size):
    if name not in sectors:
        if NEW_SECTORS_ALLOWED:
            sectors[name] = Sector(name)
            origin = sectors[name].get_origin(size)
            write_sectors(sectors_file, sectors)
            return origin
        else:
            return (1000000, 1000000, 1000000)
    return sectors[name].get_origin(size)

sectors_file = 'resources/sectors.yaml'
sectors = read_sectors(sectors_file)

if __name__ == '__main__':
    for s in get_systems('Corona Austr. Dark Region'):
        print(s['name'])
        system = System(s['name'])

        coords = list(s['coords'].values())
        pred, error, delta = system.coordinates, system.error, system.relative
        ok = True
        for c, p in zip(coords, pred):
            if not p - error <= c <= p + error:
                ok = False
                break

        origin = (coords[0] - delta[0], coords[1] - delta[1], coords[2] - delta[2])
        #print(origin)
        if ok:
            pass
            print('OK')
        else:
            #print(coords)
            #print(pred, error)
            print('WRONG')
