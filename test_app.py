import timeit
import unittest
import random
import main
from systems import System

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
                "from main import systems, nth_element;"
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


class TestNthElement(unittest.TestCase):
    def check_nth_element(self, list, n, key=lambda a : a):
        self.assertEqual(list[n], sorted(list, key=key)[n])
        for e in list[:n]:
            self.assertLessEqual(key(e), key(list[n]))
        for e in list[n + 1:]:
            self.assertGreaterEqual(key(e), key(list[n]))

    def test_nth_element(self):
        list = [1]
        main.nth_element(list, 0)
        self.assertListEqual(list, [1])

        list = [2, 1]
        main.nth_element(list, 0)
        self.assertListEqual(list, [1, 2])

        list = [2, 1, 4, 3]
        main.nth_element(list, 2)
        self.check_nth_element(list, 2)

        list = [1, 2, 3, 4, 5, 6]
        main.nth_element(list, 2)
        self.check_nth_element(list, 2)

        list = [6, 5, 4, 3, 2, 1]
        main.nth_element(list, 2)
        self.check_nth_element(list, 2)

        list = [0, 0, 0, 0, 0]
        main.nth_element(list, 2)
        self.check_nth_element(list, 2)

    def test_nth_element_random(self):
        for i in range(1, 10):
            random.seed(i)
            list = [random.randint(0, 100) for _ in range(100)]
            n = random.randint(0, 99)
            main.nth_element(list, n)
            self.check_nth_element(list, n)
    
    def test_nth_element_key(self):
        list = [1, 2, 3, 4, 5, 6]
        main.nth_element(list, 3, key=lambda a : -a)
        self.check_nth_element(list, 3, key=lambda a : -a)

        list = [3, 2, 1, 0, -1]
        main.nth_element(list, 3, key=lambda a : -a)
        self.check_nth_element(list, 3, key=lambda a : -a)

if __name__ == '__main__':
    unittest.main()
