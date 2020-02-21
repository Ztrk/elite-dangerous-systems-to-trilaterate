import heapq
import random


class KdTree:
    def __init__(self, points, data=None):
        self.root = None
        if len(points) > 0:
            if data is not None:
                points = [(p, d) for p, d in zip(points, data)]
            else:
                points = [(p, None) for p in points]
            self.root = KdNode(points, 0) 
   
    def nearest_neighbour(self, point, k):
        heap = []
        self.root.nearest_neighbour(point, k, heap)
        nodes = [node for distance, _, node in sorted(heap, reverse=True)]
        return nodes


class KdNode:
    def __init__(self, points, dim):
        self.left_child = None
        self.right_child = None
        self.split_dim = dim
        self.id = id

        half = len(points)//2
        points.sort(key=lambda x : x[0][dim])
        self.point = points[half][0]
        self.data = points[half][1]
        if len(points) > 1:
            self.left_child = KdNode(points[:half], (dim + 1) % len(self.point))
        if len(points) > 2:
            self.right_child = KdNode(points[half + 1:], (dim + 1) % len(self.point))

    def nearest_neighbour(self, point, k, heap):
        dist = distance(self.point, point)
        if len(heap) < k:
            heapq.heappush(heap, (-dist, len(heap), self))
        elif dist < -heap[0][0]:
            heapq.heappushpop(heap, (-dist, heap[0][1], self))

        if self.left_child is None:
            return
        if self.right_child is None:
            self.left_child.nearest_neighbour(point, k, heap)
            return

        if point[self.split_dim] <= self.point[self.split_dim]:
            closer_child = self.left_child
            further_child = self.right_child
        else:
            closer_child = self.right_child
            further_child = self.left_child

        closer_child.nearest_neighbour(point, k, heap)
        point2 = list(point)
        point2[self.split_dim] = self.point[self.split_dim]
        if distance(point, point2) <= -heap[0][0]:
            further_child.nearest_neighbour(point, k, heap)
    

def distance(point1, point2):
    result = 0
    for p1, p2 in zip(point1, point2):
        result += (p1 - p2) ** 2
    return result

def nth_element_util(list, n, begin, end, keys=None):
    if begin + 1 >= end:
        return
    # partition
    pivot_index = random.randint(begin, end - 1)
    pivot = keys[pivot_index]
    i, j = begin - 1, end
    while i < j:
        i += 1
        j -= 1
        while keys[i] < pivot:
            i += 1
        while keys[j] > pivot:
            j -= 1
        if i < j:
            list[i], list[j] = list[j], list[i]
            keys[i], keys[j] = keys[j], keys[i]
    if n <= j:
        nth_element_util(list, n, begin, j + 1, keys=keys)
    else:
        nth_element_util(list, n, j + 1, end, keys=keys)

def nth_element(list, n, key=None):
    if key is None:
        key = lambda a : a
    keys = [key(e) for e in list]
    nth_element_util(list, n, 0, len(list), keys=keys)
