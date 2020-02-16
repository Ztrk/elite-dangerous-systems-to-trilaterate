import unittest
from systems import System, Sectors, get_systems

class TestSystems(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sectors = Sectors()

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
        self.check_systems_in_sector('Corona Austr. Dark Region')

if __name__ == '__main__':
    unittest.main()
