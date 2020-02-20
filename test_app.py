import timeit
import unittest
import random
import main
from systems import System

@unittest.skip
class TestClosest(unittest.TestCase):
    @unittest.skip
    def test_heapq_time(self):
        # heapq - 1.59s
        res = timeit.repeat(
            "heapq.nsmallest(100, systems, key=lambda a : position.distance2(a))",
            setup=(
                "import heapq;"
                "from systems import System;"
                "from main import systems;"
                "position = System('Sol', (0, 0, 0));"
            ),
            number=1, repeat=10)
        print(res)

    def test_quickselect_time(self):
        # quickselect hoare - 2.06s
        # quickselect lomuto - 2.23s
        res = timeit.repeat((
                "nth_element(systems, 99, key=lambda system : system.distance2(position));"
                "head = systems[:100].sort(key=lambda system : system.distance2(position));"
            ),
            setup=(
                "from systems import System;"
                "from main import systems;"
                "from kd_tree import nth_element;"
                "position = System('Sol', (0, 0, 0));"
            ),
            number=1, repeat=1)
        print(res)

    @unittest.skip
    def test_sort_time(self):
        # sort - 2.29s
        res = timeit.repeat((
                "systems.sort(key=lambda a : a.distance2(position));"
                "head = systems[:100]"
            ),
            setup=(
                "from systems import System;"
                "from main import systems;"
                "position = System('Sol', (0, 0, 0));"
            ),
            number=1, repeat=5)
        print(res)


if __name__ == '__main__':
    unittest.main()
