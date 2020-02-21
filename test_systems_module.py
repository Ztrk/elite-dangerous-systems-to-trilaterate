import unittest
import logging
from systems import System, Sectors, Sector, get_systems

class TestSystems(unittest.TestCase):
    def check_systems_in_sector(self, name):
        for s in get_systems(name):
            system = System(s['name'], sectors=self.sectors)

            coords = list(s['coords'].values())
            pred, error = system.coordinates, system.error
            for c, p in zip(coords, pred):
                self.assertTrue(p - error <= c <= p + error)
            #origin = (coords[0] - delta[0], coords[1] - delta[1], coords[2] - delta[2])
            #print(origin)
    
    def test_systems_against_edsm(self):
        self.sectors = Sectors()
        self.check_systems_in_sector('ICZ')
        self.check_systems_in_sector('Regor Sector')
        self.check_systems_in_sector('Retina Sector')
        self.check_systems_in_sector('Red Spider Sector')
        self.check_systems_in_sector('Ghost of Jupiter Sector')
        self.check_systems_in_sector('NGC')
        self.check_systems_in_sector('Col 1')
        self.check_systems_in_sector('Col 2')
        self.check_systems_in_sector("Barnard's Loop")
        self.check_systems_in_sector('Horsehead Sector')
        self.check_systems_in_sector('Bleia')

    def test_reading_from_json(self):
        # clear test file
        with open('resources/testSectorsEmpty.yaml', 'w'):
            pass            
        self.sectors = Sectors('resources/testSectorsEmpty.yaml')
        self.assertDictEqual(self.sectors.sectors, {})
        self.sectors.sectors_from_json('resources/testSystemsWithCoordinates.json')
        self.assertNotEqual(self.sectors.sectors, {})

    def test_reading_from_json_small(self):
        # clear test file
        with open('resources/testSectorsEmpty.yaml', 'w'):
            pass            

        self.sectors = Sectors('resources/testSectorsEmpty.yaml')
        self.assertDictEqual(self.sectors.sectors, {})
        self.sectors.sectors_from_json('resources/testSystemsWithCoordinatesSmall.json')
        expected = {
            'Praea Euq': Sector('Praea Euq', (-65.0, -25.0, 215.0), False),
            'Wregoe': Sector('Wregoe', (-65.0, -25.0, -1065.0), False),
            'LBN 623 Sector': Sector('LBN 623 Sector', (-1345.0, -1305.0, -1065.0), False),
            'Synuefai': Sector('Synuefai', (-1345.0, -1305.0, -1065.0), False),
            'Outorst': Sector('Outorst', (-2625.0, -25.0, -2345.0), False),
            'Plaa Eurk': Sector('Plaa Eurk', (-2625.0, -25.0, -1065.0), False),
            'Synuefue': Sector('Synuefue', (-2625.0, -1305.0, -1065.0), False),
            'Wredguia': Sector('Wredguia', (-1345.0, -25.0, -1065.0), False),
            'Col 285 Sector': Sector('Col 285 Sector', (-1345.0, -25.0, -1065.0), False),
            'Col 359 Sector': Sector('Col 359 Sector', (-1345.0, -25.0, 215.0), False),
            'IC 4665 Sector': Sector('IC 4665 Sector', (-1345.0, -25.0, 215.0), False),
            'Pru Euq': Sector('Pru Euq', (-1345.0, -25.0, 215.0), False),
            'Bleae Thua': Sector('Bleae Thua', (-1345.0, -25.0, 1495.0), False),
            'Blu Ain': Sector('Blu Ain', (-65.0, -25.0, 14295.0), False),
            'Pyramoe': Sector('Pyramoe', (-1345.0, -1305.0, 5335.0), False)
        }
        self.assertDictEqual(self.sectors.sectors, expected)
            
    def test_reading_ha_sectors(self):
        # clear test file
        with open('resources/testSectorsEmpty.yaml', 'w'):
            pass            

        self.sectors = Sectors('resources/testSectorsEmpty.yaml')
        self.sectors.read_ha_sectors('resources/ha-sectors.txt')
        self.assertEqual(len(self.sectors.sectors), 465)


if __name__ == '__main__':
    unittest.main()
