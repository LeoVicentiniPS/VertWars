import heapq
import math

class Graph:
  def __init__(self, cities):
    self.vertices = {}
    self.calculate_distances(cities)

  def calculate_distances(self, cities):
     
    for i in range(len(cities)):
       self.add_vertex(i)

    for i in range(len(cities)):
       for j in range(len(cities)):
          if (i>=j): continue
          distance = math.sqrt((cities[i].x - cities[j].x)**2 + (cities[i].y - cities[j].y)**2)
          self.add_edge(i, j, round(distance))

  def add_vertex(self, vertex,):
    self.vertices[vertex] = []

  def add_edge(self, source, target, weight):
    self.vertices[source].append((target, weight))
    self.vertices[target].append((source, weight))


  def prim_mst(self):
    mst_edges = []
    visited = [False] * len(self.vertices)
    min_heap = [(0, len(self.vertices)-1, -1)]  

    while min_heap:
        weight, u, parent = heapq.heappop(min_heap)

        if visited[u]:
            continue
        visited[u] = True

        if parent != -1:
            mst_edges.append((parent, u, weight))

        for v, edge_weight in self.vertices[u]:
            if not visited[v]:
                heapq.heappush(min_heap, (edge_weight, v, u))
    return mst_edges