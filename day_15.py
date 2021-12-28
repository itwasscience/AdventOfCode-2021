from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import List, Optional
import heapq
import time
import cProfile


@dataclass
class Edge:
    """Not to be used directly - does not validate nodes build inverse relationships. Use the node methods."""

    source: Node
    target: Node
    cost: int

    def __init__(self, source: Node, target: Node, cost: int):
        self.source = source
        self.target = target
        self.cost = cost


@dataclass
class Node:
    name: str
    x: int
    y: int
    incoming_cost: int
    edges: Optional[List[Edge]]
    visited: bool
    tentative_distance: int
    previous: Optional[Node]

    def __init__(self, name: str, incoming_cost: int, x: int, y: int):
        self.name = name
        self.x = x
        self.y = y
        self.incoming_cost = incoming_cost
        self.edges = []
        self.visited = False
        self.tentative_distance = 9999
        self.previous = None

    def add_edge(self, edge: Edge):
        self.edges.append(edge)

    def add_neighbor(self, target: Node):
        self.edges.append(Edge(self, target, self.incoming_cost))

    def adjacent_nodes(self):
        return [n.target for n in self.edges]

    def set_previous(self, node: Node):
        self.previous = node


def heuristic(a: Node, b: Node) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def spf(start_node: Node, target_node: Node, all_nodes: List[Node]):
    start_node.tentative_distance = 0
    _tiebreaker = itertools.count()
    unvisited_queue = [(start_node.tentative_distance, next(_tiebreaker), start_node)]
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        # Pops a node with the smallest distance
        current_node = heapq.heappop(unvisited_queue)[2]
        current_node.visited = True

        for next_node in current_node.adjacent_nodes():
            if next_node.visited:
                continue
            new_distance = (
                current_node.tentative_distance + next_node.incoming_cost
            )  # + heuristic(next_node, target_node)
            if new_distance < next_node.tentative_distance:
                next_node.tentative_distance = new_distance
                next_node.set_previous(current_node)
                heapq.heappush(unvisited_queue, (next_node.tentative_distance, next(_tiebreaker), next_node))
            if next_node.name == target_node.name:
                return


def spf_backtrace(node: Node, path: List) -> None:
    current_node = node
    while True:
        if current_node.previous:
            path.append(current_node)
            current_node = current_node.previous
        else:
            return


def build_node_relationships(grid: List[List[Node]]) -> None:
    # Build Neighbor relationships - All rows are of equal length
    height = len(grid) - 1
    width = len(grid[0]) - 1
    print(f"Grid is {width + 1} x {height + 1}")

    for y in range(0, len(grid)):
        for x in range(0, len(grid[0])):
            # Left Top Corner
            node = grid[y][x]
            if x == 0 and y == 0:
                node.add_neighbor(grid[y][x + 1])  # >
                node.add_neighbor(grid[y + 1][x])  # V
            # Left Side
            elif x == 0 and y != 0 and y < height:
                node.add_neighbor(grid[y][x + 1])  # >
                node.add_neighbor(grid[y + 1][x])  # V
                node.add_neighbor(grid[y - 1][x])  # ^
            # Left Bottom Corner
            elif x == 0 and y == height:
                node.add_neighbor(grid[y][x + 1])  # >
                node.add_neighbor(grid[y - 1][x])  # ^
            # Bottom Side
            elif x != 0 and x < width and y == height:
                node.add_neighbor(grid[y][x + 1])  # >
                node.add_neighbor(grid[y - 1][x])  # ^
                node.add_neighbor(grid[y][x - 1])  # <
            # Right Bottom Corner
            elif x == width and y == height:
                node.add_neighbor(grid[y][x - 1])  # <
                node.add_neighbor(grid[y - 1][x])  # ^
            # Right Side
            elif x == width and y != 0 and y < height:
                node.add_neighbor(grid[y][x - 1])  # <
                node.add_neighbor(grid[y + 1][x])  # V
                node.add_neighbor(grid[y - 1][x])  # ^
            # Top Side
            elif x != 0 and x < width and y == 0:
                node.add_neighbor(grid[y][x + 1])  # >
                node.add_neighbor(grid[y][x - 1])  # <
                node.add_neighbor(grid[y + 1][x])  # V
            # Right Top Corner
            elif x == width and y == 0:
                node.add_neighbor(grid[y][x - 1])  # <
                node.add_neighbor(grid[y + 1][x])  # V
            # Sweet Gooey Center
            else:
                node.add_neighbor(grid[y][x - 1])  # <
                node.add_neighbor(grid[y + 1][x])  # V
                node.add_neighbor(grid[y - 1][x])  # ^
                node.add_neighbor(grid[y][x + 1])  # >


def part_1():
    with open("inputs/day_15.txt") as f:
        cave = f.read()
        lines = cave.replace("\r", "").split("\n")
    # Build node objects in a 2d grid - This will not be used by the transversal algo, it's a temporary thing
    grid = []
    y = 0
    for line in lines:
        x = 0
        row = []
        for cell in list(line):
            row.append(Node(name=f"{x}, {y}", incoming_cost=int(cell), x=x, y=y))
            x += 1
        grid.append(row)
        y += 1

    build_node_relationships(grid)

    all_nodes = []
    for row in grid:
        for cell in row:
            all_nodes.append(cell)
    height = len(grid) - 1
    width = len(grid[0]) - 1
    # Do the stuff.
    spf(start_node=grid[0][0], target_node=grid[height][width], all_nodes=all_nodes)
    path = []
    spf_backtrace(grid[height][width], path)

    sum = 0
    for node in path:
        sum += node.incoming_cost
    print(f"Part 1: {sum}")


def add_wrap(a: int, b: int) -> int:
    if a + b > 9:
        return a + b - 9
    else:
        return a + b


def replicate_right(grid: List[List[int]], replicate_count: int) -> List[List[int]]:
    """Replicates the grid to the right while increasing cells by 1 with wrapping"""
    new_grid = []
    for row in grid:
        new_row = []
        for x in range(0, replicate_count):
            for cell in row:
                new_row.append(add_wrap(cell, x))
        new_grid.append(new_row)
    return new_grid


def replicate_down(grid: List[List[int]], replicate_count: int) -> List[List[int]]:
    """Replicates the grid downwards while increasing cells by 1 with wrapping"""
    new_grid = []
    for x in range(0, replicate_count):
        for row in grid:
            new_row = []
            for cell in row:
                new_row.append(add_wrap(cell, x))
            new_grid.append(new_row)
    return new_grid


def part_2():
    with open("inputs/day_15.txt") as f:
        cave = f.read()
        lines = cave.replace("\r", "").split("\n")
    # Build node objects in a 2d grid - This will not be used by the transversal algo, it's a temporary thing
    grid = []
    for line in lines:
        row = []
        for cell in list(line):
            row.append(int(cell))
        grid.append(row)
    grid = replicate_right(grid, 5)
    grid = replicate_down(grid, 5)

    node_grid = []
    y = 0
    for row in grid:
        x = 0
        new_row = []
        for cell in row:
            new_row.append(Node(name=f"{x},{y}", incoming_cost=cell, x=x, y=y))
            x += 1
        y += 1
        node_grid.append(new_row)

    build_node_relationships(node_grid)
    all_nodes = []
    for row in node_grid:
        for cell in row:
            all_nodes.append(cell)

    height = len(node_grid) - 1
    width = len(node_grid[0]) - 1
    # Do the stuff.
    spf(start_node=node_grid[0][0], target_node=node_grid[height][width], all_nodes=all_nodes)
    path = []
    spf_backtrace(node_grid[width][height], path)

    sum = 0
    for node in path:
        sum += node.incoming_cost
    print(f"Part 2: {sum}")


part_1()
part_2()
