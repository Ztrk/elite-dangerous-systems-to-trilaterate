from math import sqrt
import re
import requests
from yaml import load, dump, CLoader as Loader, CDumper as Dumper

NEW_SECTORS_ALLOWED = False

def to_number(letter):
    return ord(letter) - ord('A')

def get_systems(name, multiple=True):
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

    def __init__(self, name, coordinates=None, hand_placed=False, is_origin=True):
        self.name = name
        self.hand_placed = hand_placed
        if coordinates is None:
            self.compute_origin()
        else:
            if is_origin:
                self.origin = coordinates
            else:
                self.get_origin_from_coordinates(coordinates)
    
    def __repr__(self):
        return 'Sector({}, {}, {})'.format(self.name, self.origin, self.hand_placed)

    def get_origin_from_coordinates(self, coords):
        """Computes sector origin from given coords"""
        coords = list(coords)
        for i in range(len(coords)):
            coords[i] -= (coords[i] - self.sectors_origin[i]) % self.sector_size
        self.origin = tuple(coords)

    def compute_origin(self):
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
        self.get_origin_from_coordinates(sector_coords)

    def get_origin(self, size):
        """Computes sector origin for cube of given size"""
        if self.hand_placed:
            coords = list(self.origin)
            for i in range(len(coords)):
                coords[i] -= (coords[i] - self.sectors_origin[i]) % size
            return coords
        return self.origin


class System:
    def __init__(self, name, coordinates=None, sectors=None):
        self.name = name
        self.parse_name()
        if coordinates is None:
            if sectors is None:
                self.coordinates_from_edsm()
            else:
                self.coordinates_from_name(sectors)
        else:
            self.coordinates = coordinates
            self.error = 0
            self.relative = (0, 0, 0)
    
    def distance(self, other):
        dist = 0
        for c1, c2 in zip(self.coordinates, other.coordinates):
            dist += (c1 - c2) ** 2
        return sqrt(dist)
    
    def parse_name(self):
        """Calculate sector_name, cube_size and cube_index"""
        match = re.search(r'([A-Z]{2}-[A-Z]) ([a-h])(\d+)(-\d+)?', self.name)
        if match is None:
            self.sector_name = None
            self.cube_size = None
            self.cube_index = None
            return

        self.sector_name = self.name[:match.start() - 1]
        self.cube_size = 10 * 2 ** (ord(match.group(2)) - ord('a'))
        letter_code = match.group(1)
        if match.group(4) is None:
            number = 0
        else:
            number = int(match.group(3))
        self.cube_index = (26 * 26 * 26 * number + 26 * 26 * to_number(letter_code[3])
            + 26 * to_number(letter_code[1]) + to_number(letter_code[0]))

    def coordinates_from_edsm(self):
        response = get_systems(self.name, multiple=False)
        self.relative = None
        if len(response) > 0:
            coords = response['coords']
            self.coordinates = (coords['x'], coords['y'], coords['z'])
            self.error = 0
        else:
            self.coordinates = (0, 0, 0)
            self.error = 5000

    def coordinates_from_name(self, sectors):
        if self.sector_name is None:
            self.relative = None
            self.coordinates = (0, 0, 0)
            self.error = 5000
            return

        origin = sectors.get_origin(self.sector_name, self.cube_size)
        if origin is None:
            origin = (0, 0, 0)

        size = self.cube_size
        index = self.cube_index
        self.relative = (size * (index % 128), size * (index//128 % 128), size * (index//(128 * 128)))
        self.coordinates = (origin[0] + size/2 + self.relative[0],
            origin[1] + size/2 + self.relative[1], origin[2] + size/2 + self.relative[2])
        self.error = size/2


class Sectors:
    sectors_file = 'resources/sectors.yaml'
    def __init__(self, allow_new=False):
        self.allow_new = allow_new
        self.sectors = self.read_sectors(self.sectors_file)

    def read_sectors(self, filename):
        print('Reading sectors')
        with open(filename, 'r') as file:
            data = load(file, Loader=Loader)
        if data is None:
            return {}
        return data

    def write_sectors(self, filename, sectors):
        print('Writing sectors')
        with open(filename, 'w') as file:
            dump(sectors, file, Dumper=Dumper)
        print('Sectors written')

    def get_origin(self, name, size):
        if name not in self.sectors:
            if self.allow_new:
                self.sectors[name] = Sector(name)
                origin = self.sectors[name].get_origin(size)
                self.write_sectors(self.sectors_file, self.sectors)
                return origin
            else:
                return None
        return self.sectors[name].get_origin(size)
