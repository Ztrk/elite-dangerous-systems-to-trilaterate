import random
import timeit
import unittest
from kd_tree import nth_element, KdTree, distance

class TestNthElement(unittest.TestCase):
    def check_nth_element(self, list, n, key=lambda a : a):
        self.assertEqual(list[n], sorted(list, key=key)[n])
        for e in list[:n]:
            self.assertLessEqual(key(e), key(list[n]))
        for e in list[n + 1:]:
            self.assertGreaterEqual(key(e), key(list[n]))

    def test_nth_element(self):
        list = [1]
        nth_element(list, 0)
        self.assertListEqual(list, [1])

        list = [2, 1]
        nth_element(list, 0)
        self.assertListEqual(list, [1, 2])

        list = [2, 1, 4, 3]
        nth_element(list, 2)
        self.check_nth_element(list, 2)

        list = [1, 2, 3, 4, 5, 6]
        nth_element(list, 2)
        self.check_nth_element(list, 2)

        list = [6, 5, 4, 3, 2, 1]
        nth_element(list, 2)
        self.check_nth_element(list, 2)

        list = [0, 0, 0, 0, 0]
        nth_element(list, 2)
        self.check_nth_element(list, 2)

    def test_nth_element_random(self):
        for i in range(1, 10):
            random.seed(i)
            list = [random.randint(0, 100) for _ in range(100)]
            n = random.randint(0, 99)
            nth_element(list, n)
            self.check_nth_element(list, n)
    
    def test_nth_element_key(self):
        list = [1, 2, 3, 4, 5, 6]
        nth_element(list, 3, key=lambda a : -a)
        self.check_nth_element(list, 3, key=lambda a : -a)

        list = [3, 2, 1, 0, -1]
        nth_element(list, 3, key=lambda a : -a)
        self.check_nth_element(list, 3, key=lambda a : -a)


class TestKdTree(unittest.TestCase):
    def test_init(self):
        tree = KdTree([(1, 2)])
        self.assertTupleEqual(tree.root.point, (1, 2))
        self.assertIsNone(tree.root.left_child)
        self.assertIsNone(tree.root.right_child)

        tree = KdTree([(1, 2), (2, 1)])
        self.assertTupleEqual(tree.root.point, (2, 1))
        self.assertTupleEqual(tree.root.left_child.point, (1, 2))
        self.assertIsNone(tree.root.right_child)

        tree = KdTree([(1, ), (2, ), (3, )])
        self.assertTupleEqual(tree.root.point, (2, ))
        self.assertTupleEqual(tree.root.left_child.point, (1, ))
        self.assertTupleEqual(tree.root.right_child.point, (3, ))

    def test_nearest_neighbour(self):
        tree = KdTree([(1, )])
        nearest = tree.nearest_neighbour((-3, ), 1)
        self.assertTupleEqual(nearest[0].point, (1, ))

        tree = KdTree([(1, 3), (2, 4)])
        nearest = tree.nearest_neighbour((0, 2), 1)
        self.assertTupleEqual(nearest[0].point, (1, 3))
        nearest = tree.nearest_neighbour((3, 5), 1)
        self.assertTupleEqual(nearest[0].point, (2, 4))

        tree = KdTree([(1, 3, 3), (4, 8, 7), (2, -1, 2), (3, 4, 1)])
        nearest = tree.nearest_neighbour((1, 2, 0), 1)
        self.assertTupleEqual(nearest[0].point, (3, 4, 1))

        tree = KdTree([(-1, 1), (0, -2), (1, -2)])
        nearest = tree.nearest_neighbour((1, 2), 1)
        self.assertTupleEqual(nearest[0].point, (-1, 1))
    
    def random_point(self, range):
        return random.randint(-range, range), random.randint(-range, range), random.randint(-range, range)
    
    def test_nearest_neighbour_random(self):
        for seed in range(1, 10):
            random.seed(seed)
            points = [self.random_point(100) for _ in range(100)]
            point = self.random_point(100)
            closest = sorted(points, key=lambda x : distance(point, x))

            tree = KdTree(points)
            self.assertTupleEqual(tree.nearest_neighbour(point, 1)[0].point, closest[0])
            
            nearest = tree.nearest_neighbour(point, 10)
            for n, c in zip(nearest, closest):
                self.assertTupleEqual(n.point, c)

    def test_nearest_neighbour_big(self):
        # creating tree - 36 s
        # finding nn - 0.3 ms
        # nth element - 1.37 ms
        # sort - 1.2 ms
        random.seed(42)
        points = [(random.randint(-100000, 100000), random.randint(-100000, 100000),
            random.randint(-100000, 100000)) for _ in range(25000)]
        point = (random.randint(-100000, 100000), random.randint(-100000, 100000), random.randint(-100000, 100000))
        closest = (-10000000, -10000000, -10000000)
        for p in points:
            if distance(point, p) < distance(point, closest):
                closest = p

        start = timeit.default_timer()
        tree = KdTree(points)
        print('Creating tree', timeit.default_timer() - start)

        start = timeit.default_timer()
        nearest = tree.nearest_neighbour(point, 100)
        print('Searching NN', timeit.default_timer() - start)
        self.assertTupleEqual(nearest[0].point, closest)


if __name__ == '__main__':
    unittest.main()
