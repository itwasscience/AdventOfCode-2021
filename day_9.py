from __future__ import annotations
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass()
class Point:
    key: Tuple[int, int]
    height: int
    visited: bool = False


def neighbors(grid: Dict[Tuple[int, int], Point], location: Tuple[int, int]) -> List[Point]:
    """Returns all four possible neighbors of a point. Out-of-bounds are points that have already been visited."""
    (y, x) = location
    return [
        grid.get((y - 1, x), Point(key=(y - 1, x), height=9, visited=True)),
        grid.get((y + 1, x), Point(key=(y + 1, x), height=9, visited=True)),
        grid.get((y, x - 1), Point(key=(y, x - 1), height=9, visited=True)),
        grid.get((y, x + 1), Point(key=(y, x + 1), height=9, visited=True))
    ]


def find_low_points(grid: Dict[Tuple[int, int], Point]) -> List[Tuple[int, int]]:
    """Finds the lowest points - points that have four neighbor heights greater than their own."""
    low_points = []
    width = 0
    height = 0
    for k, _v in grid.items():
        (height, width) = k
    for y in range(height + 1):
        for x in range(width + 1):
            if all([n.height > grid[(y, x)].height for n in neighbors(grid, (y, x))]):
                low_points.append((y, x))
    return low_points


def valley_bfs(grid: Dict[Tuple[int, int], Point], starting_tuple: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Runs a limited valley-finding BFS algorithm. Mapping _must_ start inside a valley."""
    # Place BFS limits on borders and reset all other points
    for _k, point in grid.items():
        if 9 == point.height:
            point.visited = True
        else:
            point.visited = False
    # BFS itself
    reached_points = [starting_tuple]
    start_point = grid[starting_tuple]
    start_point.visited = True
    queue = [start_point]
    while len(queue):
        current = queue.pop()
        for neighbor in neighbors(grid, current.key):
            if not neighbor.visited:
                neighbor.visited = True
                reached_points.append(neighbor.key)
                queue.append(neighbor)
    return reached_points


def part_1():
    grid = load_data()
    low_points = find_low_points(grid)
    total = 0
    for coord in low_points:
        total += grid[coord].height + 1
    print(f"Part 1: {total}")


def part_2():
    grid = load_data()
    low_points = find_low_points(grid)
    counts = []
    for coord in low_points:
        valley_coords = valley_bfs(grid, coord)
        counts.append(len(valley_coords))
    counts.sort()
    total = counts[-1] * counts[-2] * counts[-3]
    print(f"Part 2: {total}")


def load_data() -> Dict[(int, int), Point]:
    with open("inputs/day_09.txt") as f:
        cave = f.read()
        lines = cave.replace("\r", "").split("\n")
    # Build node objects in a 2d grid - This will not be used by the transversal algo, it's a temporary thing
    grid = {}
    for y in range(len(lines)):
        line = list(lines[y])
        for x in range(len(line)):
            grid[(y, x)] = Point(key=(y, x), height=int(line[x]))
    return grid


part_1()
part_2()
