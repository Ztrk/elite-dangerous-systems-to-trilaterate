import unittest
from unittest.mock import Mock, patch
from systems import System, Sector, get_systems

class TestSystem(unittest.TestCase):
    def test_init_from_coords(self):
        coords = (12.25, 230.375, -2450.875)
        system = System('System name AB-C e12', coords)
        self.assertEqual(system.coordinates, coords)
        self.assertEqual(system.error, 0)
        self.assertEqual(system.sector_name, 'System name')
        self.assertEqual(system.cube_size, 160)
        self.assertEqual(system.cube_index, 1378)

    @patch('systems.get_systems')
    def test_init_from_edsm(self, get_systems_mock):
        coords = (-2785.675, -1180.125, 270.75)
        coords_dict = {'coords': {'x': coords[0], 'y': coords[1], 'z': coords[2]}}
        get_systems_mock.return_value=coords_dict
        system = System('Name in edsm')
        get_systems_mock.assert_called_with('Name in edsm', multiple=False)
        self.assertEqual(system.coordinates, coords)
        self.assertEqual(system.error, 0)
    
    def test_init_from_sectors(self):
        sectors = Mock()
        origin = (-105, 1005, -5)
        sectors.get_origin.return_value = origin
        system = System('Some name AX-Z c14-1', sectors=sectors)
        sectors.get_origin.assert_called_with('Some name', 40)

        relative = (40 * 10, 40 * 11, 40 * 16)
        coords = (origin[0] + relative[0] + 20, origin[1] + relative[1] + 20, origin[2] + relative[2] + 20)
        self.assertEqual(system.relative, relative)
        self.assertEqual(system.coordinates, coords)
        self.assertEqual(system.cube_index, 263562)
        self.assertEqual(system.error, 20)
    
    def test_init_not_procedural_name(self):
        sectors = Mock()
        system = System('Sol', sectors=sectors)
        
        self.assertEqual(system.coordinates, (0, 0, 0))
        self.assertEqual(system.error, 5000)
        self.assertEqual(system.sector_name, None)
        self.assertEqual(system.cube_index, None)
        self.assertEqual(system.cube_size, None)


class TestSector(unittest.TestCase):
    def test_init_from_origin(self):
        origin = (-1015, 850, 75)
        sector = Sector('Some sector', origin)
        self.assertEqual(sector.origin, origin)

    def test_init_from_coords(self):
        coords = (13405.28125, -514.25, -5960.28125 )
        origin = (12735, -1305, -6185)
        sector = Sector('Some sector', coords, is_origin=False)
        self.assertEqual(sector.origin, origin)

    @patch('systems.get_systems')
    def test_init_from_edsm(self, get_systems):
        coords = (12442.09375, -1120.5, 45902.75)
        origin = (11455, -1305, 45015)
        get_systems.return_value = [{'coords': {'x': coords[0], 'y': coords[1], 'z': coords[2]}}]
        sector = Sector('Some sector')

        get_systems.assert_called()
        self.assertEqual(sector.origin, origin)


if __name__ == '__main__':
    unittest.main()
