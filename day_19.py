from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple
from itertools import combinations
import uuid


@dataclass
class Position:
    x: int
    y: int
    z: int


@dataclass
class Vector:
    x: int
    y: int
    z: int


@dataclass
class Beacon:
    uuid: uuid.UUID
    position: Position
    associations: [List[Beacon]] = field(default_factory=list)
    visited: bool = False

    def distance(self, b: Beacon) -> Vector:
        return Vector(
            abs(self.position.x - b.position.x),
            abs(self.position.y - b.position.y),
            abs(self.position.z - b.position.z),
        )


def equals_swizzle(vec_a: Vector, vec_b: Vector):
    """Returns true if a position is equal to another position after any set of 3d rotations."""
    return (
        (vec_a.x, vec_a.y, vec_a.z) == (vec_b.x, vec_b.y, vec_b.z)
        or (vec_a.x, vec_a.y, vec_a.z) == (vec_b.x, vec_b.z, vec_b.y)
        or (vec_a.x, vec_a.y, vec_a.z) == (vec_b.y, vec_b.x, vec_b.z)
        or (vec_a.x, vec_a.y, vec_a.z) == (vec_b.y, vec_b.z, vec_b.x)
        or (vec_a.x, vec_a.y, vec_a.z) == (vec_b.z, vec_b.x, vec_b.y)
        or (vec_a.x, vec_a.y, vec_a.z) == (vec_b.z, vec_b.y, vec_b.x)
    )


def flip_xyz_xzy(vec: Tuple[int, int, int]) -> Tuple[int, int, int]:
    return vec[0], vec[2], vec[1]


def flip_xyz_yxz(vec: Tuple[int, int, int]) -> Tuple[int, int, int]:
    return vec[1], vec[0], vec[2]


def flip_xyz_zyx(vec: Tuple[int, int, int]) -> Tuple[int, int, int]:
    return vec[2], vec[1], vec[0]


def flip_xyz_yzx(vec: Tuple[int, int, int]) -> Tuple[int, int, int]:
    return vec[1], vec[2], vec[0]


def flip_xyz_zxy(vec: Tuple[int, int, int]) -> Tuple[int, int, int]:
    return vec[2], vec[0], vec[1]


def compare_fingerprints(
    fingerprint_a: List[Tuple[Vector, Beacon, Beacon]],
    fingerprint_b: List[Tuple[Vector, Beacon, Beacon]],
    threshold: int = 66,
) -> bool:
    """Returns true if fingerprints have at least threshold matches"""
    matches = 0
    # This is O(n^2)
    for a in fingerprint_a:
        for b in fingerprint_b:
            if equals_swizzle(a[0], b[0]):
                a[1].associations.append(b[1])
                a[2].associations.append(b[2])
                matches += 1
            """
            elif flip_xyz_xzy(a[0]) == b[0]:
                a[1].associations.append(b[1])
                a[2].associations.append(b[2])
                matches += 1
            elif flip_xyz_yxz(a[0]) == b[0]:
                a[1].associations.append(b[1])
                a[2].associations.append(b[2])
                matches += 1
            elif flip_xyz_zyx(a[0]) == b[0]:
                a[1].associations.append(b[1])
                a[2].associations.append(b[2])
                matches += 1
            elif flip_xyz_yzx(a[0]) == b[0]:
                a[1].associations.append(b[1])
                a[2].associations.append(b[2])
                matches += 1
            elif flip_xyz_zxy(a[0]) == b[0]:
                a[1].associations.append(b[1])
                a[2].associations.append(b[2])
                matches += 1
            """
    valid = matches >= threshold
    return valid


def fingerprint_beacons(beacons: List[Beacon]) -> List[Tuple[Vector, Beacon, Beacon]]:
    """Returns all of the relative distances between all beacons."""
    fingerprint = []
    for combo in list(combinations(beacons, 2)):
        [a, b] = combo
        fingerprint.append((a.distance(b), a, b))
    return fingerprint


def find_unique_beacons(completed_report: Dict[int, List[Beacon]]):
    """Returns a list of unique beacons - NOTE: requires that fingerprint comparisons have been run."""
    unique_beacons = []
    for _k, beacons in completed_report.items():
        for beacon in beacons:
            if not beacon.visited:
                unique_beacons.append(beacon)
                # All beacons in the associated table are the current beacon as seen from a different sensor.
                for a in beacon.associations:
                    a.visited = True
    return unique_beacons


def locate_scanner(beacon_a: Beacon, beacon_b: Beacon, offset: Position):
    ##print(beacon_a.position, beacon_b.position, offset)
    """Returns a tuple representing the relative position between the same beacon as seen by two scanners."""
    return Position(
        beacon_a.position.x + beacon_b.position.x - offset.x,
        beacon_a.position.y - beacon_b.position.y - offset.y,
        beacon_a.position.z + beacon_b.position.z - offset.z,
    )


def read_input_file() -> Dict[int, List[Beacon]]:
    """Returns a dictionary indexed by scanner number with a list of all beacons seen by the scanner."""
    with open("inputs/day_19.txt") as f:
        report_raw = f.read()
    report_data = {}
    scanner = None
    for line in report_raw.split("\n"):
        if "" == line:
            continue
        elif "scanner" in line:
            scanner = int(line.split(" ")[2])
            report_data[scanner] = []
        else:
            [x, y, z] = [int(v) for v in line.split(",")]
            report_data[scanner].append(Beacon(uuid.uuid4(), Position(x, y, z)))
    return report_data


# Scanner 0 will always be assumed to be the origin point for absolute references
scanner_locations = {0: Position(0, 0, 0)}
report = read_input_file()
#print(report.keys())
for scanner_pair in list(combinations(report.keys(), 2)):
    (scanner_a, scanner_b) = scanner_pair
    if compare_fingerprints(fingerprint_beacons(report[scanner_a]), fingerprint_beacons(report[scanner_b])):
        # Find any two matching beacons
     #   print(f"Match on {scanner_a},{scanner_b}")
        for beacon in report[scanner_a]:
            if beacon.associations:
                if scanner_a in scanner_locations:
                    # print(locate_scanner(beacon, beacon.associations[0], scanner_locations[scanner_a]))
                    scanner_locations[scanner_b] = locate_scanner(
                        beacon, beacon.associations[0], scanner_locations[scanner_a]
                    )
                elif scanner_b in scanner_locations:
                    # print(locate_scanner(beacon, beacon.associations[0], scanner_locations[scanner_b]))
                    scanner_locations[scanner_a] = locate_scanner(
                        beacon, beacon.associations[0], scanner_locations[scanner_b]
                    )
                #print(scanner_locations)
                break

for x in report[0]:
    if x.position.x == -618:
        print(x)

print(f"Part 1: {len(find_unique_beacons(report))}")
