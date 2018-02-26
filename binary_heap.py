import random
from functools import total_ordering

class MinBinaryHeap:
  def __init__(self):
    self.array = [0] * 100
    self.count = 0

  def add(self, element):
    if self.count == len(self.array):
      self.array += [0] * len(self.array)
    self.array[self.count] = element
    self.shift_up(self.count)
    self.count += 1

  @staticmethod
  def get_parent(n):
    if n != 0:
      return (n - 1) / 2
    else:
      return -1

  @staticmethod
  def get_left_child(n):
    return 2 * n + 1

  def swap_elements(self, i, j):
    self.array[i], self.array[j] = self.array[j], self.array[i]

  def shift_up(self, index):
    if len(self.array) != 0:
      while index > 0 and \
            self.array[index] < self.array[MinBinaryHeap.get_parent(index)]:
        self.swap_elements(index, MinBinaryHeap.get_parent(index))
        index = MinBinaryHeap.get_parent(index)
      return index

  def shift_down(self, index):
    if index >= 0:
      left_child = MinBinaryHeap.get_left_child(index)
      if left_child < self.count:
        if left_child + 1 < self.count and \
           self.array[left_child + 1] < self.array[left_child]:
          left_child += 1

        if self.array[index] > self.array[left_child]:
          self.swap_elements(index, left_child)
          self.shift_down(left_child)

  def remove_min(self):
    if self.count < 0:
      self.count = 0
      return 0
    self.count -= 1
    self.swap_elements(0, self.count)
    self.shift_down(0)
    return self.array[self.count]

  def build_heap(self):
    i = self.count - 1
    while i >= 0:
      self.shift_down(i)
      i -= 1

  def is_empty(self):
    return self.count <= 0

@total_ordering
class GraphEdge:
  def __init__(self, edge, weight):
    self.edge = edge
    self.weight = weight

  def __eq__(self, other_edge):
    return self.weight == other_edge.weight

  def __lt__(self, other_edge):
    return self.weight < other_edge.weight

  def __str__(self):
    return str(self.edge) + " " + str(self.weight)

successes = []
for c in range(10):
  h = MinBinaryHeap()
  for i in range(0, 20):
    h.add(GraphEdge(random.randint(1,10), random.randint(1, 100)))

  a = []
  while not h.is_empty():
    m = h.remove_min()
    print m
    a.append(m)
  print "-" * 20

  if sorted(a) != a:
    print 'Failure :('
    exit

print 'Success!'

# if all([successes[s] for s in xrange(len(successes) - 1)]):
#   print 'Success!'
# else:
#   print 'Failure :('