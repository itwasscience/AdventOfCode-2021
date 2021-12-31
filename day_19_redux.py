from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
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
    scanner: int
    position: Position
    associations: [List[Tuple[str, Beacon]]] = field(default_factory=list)
    visited: bool = False

    def distance(self, b: Beacon) -> Vector:
        return Vector(
            self.position.x - b.position.x,
            self.position.y - b.position.y,
            self.position.z - b.position.z,
        )


"""def equals_swizzle(vec_a: Vector, vec_b: Vector):
    return (
        (vec_a.x, vec_a.y, vec_a.z) == (vec_b.x, vec_b.y, vec_b.z)
        or (vec_a.x, vec_a.y, vec_a.z) == (vec_b.x, vec_b.z, vec_b.y)
        or (vec_a.x, vec_a.y, vec_a.z) == (vec_b.y, vec_b.x, vec_b.z)
        or (vec_a.x, vec_a.y, vec_a.z) == (vec_b.y, vec_b.z, vec_b.x)
        or (vec_a.x, vec_a.y, vec_a.z) == (vec_b.z, vec_b.x, vec_b.y)
        or (vec_a.x, vec_a.y, vec_a.z) == (vec_b.z, vec_b.y, vec_b.x)
    )
"""

def mirror_none(vec: Vector) -> Vector:
    return Vector(vec.x, vec.y, vec.z)


def mirror_x(vec: Vector) -> Vector:
    return Vector(vec.x, vec.y, -vec.z)


def mirror_y(vec: Vector) -> Vector:
    return Vector(vec.x, -vec.y, vec.z)


def mirror_z(vec: Vector) -> Vector:
    return Vector(vec.x, vec.y, -vec.z)


def flip_xyz_xyz(vec: Vector) -> Vector:
    return vec


def flip_xyz_xzy(vec: Vector) -> Vector:
    return Vector(vec.x, vec.z, vec.y)


def flip_xyz_yxz(vec: Vector) -> Vector:
    return Vector(vec.y, vec.x, vec.z)


def flip_xyz_zyx(vec: Vector) -> Vector:
    return Vector(vec.z, vec.y, vec.x)


def flip_xyz_yzx(vec: Vector) -> Vector:
    return Vector(vec.y, vec.z, vec.x)


def flip_xyz_zxy(vec: Vector) -> Vector:
    return Vector(vec.z, vec.x, vec.y)


def compare_fingerprints(
    fingerprint_a: List[Tuple[Vector, Beacon, Beacon]],
    fingerprint_b: List[Tuple[Vector, Beacon, Beacon]],
    threshold: int = 66,
) -> bool:
    """Returns true if fingerprints have at least threshold matches. Positions are normalized to the a-coord system."""
    matches = 0
    # This is O(n^2)
    for a in fingerprint_a:
        for b in fingerprint_b:
            if a[0] == b[0]:
                a[1].associations.append(("xyz", b[1]))
                a[2].associations.append(("xyz", b[2]))
                matches += 1
            elif a[0] == flip_xyz_xzy(b[0]):
                #   b.position = Position(b.position.x, b.position.z, b.position.y)
                a[1].associations.append(("xzy", b[1]))
                a[2].associations.append(("xzy", b[2]))
                matches += 1
            elif a[0] == flip_xyz_yxz(b[0]):
                #     b.position = Position(b.position.y, b.position.x, b.position.z)
                a[1].associations.append(("yxz", b[1]))
                a[2].associations.append(("yxz", b[2]))
                matches += 1
            elif a[0] == flip_xyz_zyx(b[0]):
                #           b.position = Position(b.position.z, b.position.y, b.position.x)
                a[1].associations.append(("zyx", b[1]))
                a[2].associations.append(("zyx", b[2]))
                matches += 1
            elif a[0] == flip_xyz_yzx(b[0]):
                #   b[1].position = Position(b[1].position.y, b[1].position.z, b[1].position.x)
                a[1].associations.append(("yzx", b[1]))
                a[2].associations.append(("yzx", b[2]))
                matches += 1
            elif a[0] == flip_xyz_zxy(b[0]):
                #                b.position = Position(b.position.z, b.position.x, b.position.y)
                a[1].associations.append(("zxy", b[1]))
                a[2].associations.append(("zxy", b[2]))
                matches += 1
            tmp_b = mirror_x(b[0])
            if a[0] == tmp_b:
                a[1].associations.append(("-xyz", b[1]))
                a[2].associations.append(("-xyz", b[2]))
                matches += 1
            elif a[0] == flip_xyz_xzy(tmp_b):
                a[1].associations.append(("-xzy", b[1]))
                a[2].associations.append(("-xzy", b[2]))
                matches += 1
            elif a[0] == flip_xyz_yxz(tmp_b):
                a[1].associations.append(("y-xz", b[1]))
                a[2].associations.append(("y-xz", b[2]))
                matches += 1
            elif a[0] == flip_xyz_zyx(tmp_b):
                a[1].associations.append(("zy-x", b[1]))
                a[2].associations.append(("zy-x", b[2]))
                matches += 1
            elif a[0] == flip_xyz_yzx(tmp_b):
                a[1].associations.append(("yz-x", b[1]))
                a[2].associations.append(("yz-x", b[2]))
                matches += 1
            elif a[0] == flip_xyz_zxy(tmp_b):
                a[1].associations.append(("z-xy", b[1]))
                a[2].associations.append(("z-xy", b[2]))
                matches += 1
            tmp_b = mirror_y(b[0])
            if a[0] == tmp_b:
                a[1].associations.append(("x-yz", b[1]))
                a[2].associations.append(("x-yz", b[2]))
                matches += 1
            elif a[0] == flip_xyz_xzy(tmp_b):
                a[1].associations.append(("xz-y", b[1]))
                a[2].associations.append(("xz-y", b[2]))
                matches += 1
            elif a[0] == flip_xyz_yxz(tmp_b):
                a[1].associations.append(("-yxz", b[1]))
                a[2].associations.append(("-yxz", b[2]))
                matches += 1
            elif a[0] == flip_xyz_zyx(tmp_b):
                a[1].associations.append(("z-yx", b[1]))
                a[2].associations.append(("z-yx", b[2]))
                matches += 1
            elif a[0] == flip_xyz_yzx(tmp_b):
                a[1].associations.append(("-yzx", b[1]))
                a[2].associations.append(("-yzx", b[2]))
                matches += 1
            elif a[0] == flip_xyz_zxy(tmp_b):
                a[1].associations.append(("zx-y", b[1]))
                a[2].associations.append(("zx-y", b[2]))
                matches += 1
            tmp_b = mirror_z(b[0])
            if a[0] == tmp_b:
                a[1].associations.append(("xy-z", b[1]))
                a[2].associations.append(("xy-z", b[2]))
                matches += 1
            elif a[0] == flip_xyz_xzy(tmp_b):
                a[1].associations.append(("x-zy", b[1]))
                a[2].associations.append(("x-zy", b[2]))
                matches += 1
            elif a[0] == flip_xyz_yxz(tmp_b):
                a[1].associations.append(("yx-z", b[1]))
                a[2].associations.append(("yx-z", b[2]))
                matches += 1
            elif a[0] == flip_xyz_zyx(tmp_b):
                a[1].associations.append(("-zyx", b[1]))
                a[2].associations.append(("-zyx", b[2]))
                matches += 1
            elif a[0] == flip_xyz_yzx(tmp_b):
                a[1].associations.append(("y-zx", b[1]))
                a[2].associations.append(("y-zx", b[2]))
                matches += 1
            elif a[0] == flip_xyz_zxy(tmp_b):
                a[1].associations.append(("-zxy", b[1]))
                a[2].associations.append(("-zxy", b[2]))
                matches += 1
            tmp_b = mirror_x(mirror_y(b[0]))
            if a[0] == tmp_b:
                a[1].associations.append(("-x-yz", b[1]))
                a[2].associations.append(("-x-yz", b[2]))
                matches += 1
            elif a[0] == flip_xyz_xzy(tmp_b):
                a[1].associations.append(("-xz-y", b[1]))
                a[2].associations.append(("-xz-y", b[2]))
                matches += 1
            elif a[0] == flip_xyz_yxz(tmp_b):
                a[1].associations.append(("-y-xz", b[1]))
                a[2].associations.append(("-y-xz", b[2]))
                matches += 1
            elif a[0] == flip_xyz_zyx(tmp_b):
                a[1].associations.append(("z-y-x", b[1]))
                a[2].associations.append(("z-y-x", b[2]))
                matches += 1
            elif a[0] == flip_xyz_yzx(tmp_b):
                a[1].associations.append(("-yz-x", b[1]))
                a[2].associations.append(("-yz-x", b[2]))
                matches += 1
            elif a[0] == flip_xyz_zxy(tmp_b):
                a[1].associations.append(("z-x-y", b[1]))
                a[2].associations.append(("z-x-y", b[2]))
                matches += 1
            tmp_b = mirror_x(mirror_z(b[0]))
            if a[0] == tmp_b:
                a[1].associations.append(("-xy-z", b[1]))
                a[2].associations.append(("-xy-z", b[2]))
                matches += 1
            elif a[0] == flip_xyz_xzy(tmp_b):
                a[1].associations.append(("-x-zy", b[1]))
                a[2].associations.append(("-x-zy", b[2]))
                matches += 1
            elif a[0] == flip_xyz_yxz(tmp_b):
                a[1].associations.append(("y-x-z", b[1]))
                a[2].associations.append(("y-x-z", b[2]))
                matches += 1
            elif a[0] == flip_xyz_zyx(tmp_b):
                a[1].associations.append(("-zy-x", b[1]))
                a[2].associations.append(("-zy-x", b[2]))
                matches += 1
            elif a[0] == flip_xyz_yzx(tmp_b):
                a[1].associations.append(("y-z-x", b[1]))
                a[2].associations.append(("y-z-x", b[2]))
                matches += 1
            elif a[0] == flip_xyz_zxy(tmp_b):
                a[1].associations.append(("-z-xy", b[1]))
                a[2].associations.append(("-z-xy", b[2]))
                matches += 1
            tmp_b = mirror_z(mirror_y(b[0]))
            if a[0] == tmp_b:
                a[1].associations.append(("x-y-z", b[1]))
                a[2].associations.append(("x-y-z", b[2]))
                matches += 1
            elif a[0] == flip_xyz_xzy(tmp_b):
                a[1].associations.append(("x-z-y", b[1]))
                a[2].associations.append(("x-z-y", b[2]))
                matches += 1
            elif a[0] == flip_xyz_yxz(tmp_b):
                a[1].associations.append(("-yx-z", b[1]))
                a[2].associations.append(("-yx-z", b[2]))
                matches += 1
            elif a[0] == flip_xyz_zyx(tmp_b):
                a[1].associations.append(("-z-yx", b[1]))
                a[2].associations.append(("-z-yx", b[2]))
                matches += 1
            elif a[0] == flip_xyz_yzx(tmp_b):
                a[1].associations.append(("-y-zx", b[1]))
                a[2].associations.append(("-y-zx", b[2]))
                matches += 1
            elif a[0] == flip_xyz_zxy(tmp_b):
                a[1].associations.append(("-zx-y", b[1]))
                a[2].associations.append(("-zx-y", b[2]))
                matches += 1
            tmp_b = mirror_z(mirror_x(mirror_y(b[0])))
            if a[0] == tmp_b:
                a[1].associations.append(("-x-y-z", b[1]))
                a[2].associations.append(("-x-y-z", b[2]))
                matches += 1
            elif a[0] == flip_xyz_xzy(tmp_b):
                a[1].associations.append(("-x-z-y", b[1]))
                a[2].associations.append(("-x-z-y", b[2]))
                matches += 1
            elif a[0] == flip_xyz_yxz(tmp_b):
                a[1].associations.append(("-y-x-z", b[1]))
                a[2].associations.append(("-y-x-z", b[2]))
                matches += 1
            elif a[0] == flip_xyz_zyx(tmp_b):
                a[1].associations.append(("-z-y-x", b[1]))
                a[2].associations.append(("-z-y-x", b[2]))
                matches += 1
            elif a[0] == flip_xyz_yzx(tmp_b):
                a[1].associations.append(("-y-z-x", b[1]))
                a[2].associations.append(("-y-z-x", b[2]))
                matches += 1
            elif a[0] == flip_xyz_zxy(tmp_b):
                a[1].associations.append(("-z-x-y", b[1]))
                a[2].associations.append(("-z-x-y", b[2]))
                matches += 1
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
                    a[1].visited = True
    return unique_beacons


def locate_scanner(beacon_a: Beacon, beacon_b: Beacon, offset: Position):
    print(beacon_a.position, beacon_b.position, offset)
    """Returns a tuple representing the relative position between the same beacon as seen by two scanners."""
    return Position(
        beacon_a.position.x + beacon_b.position.x, #- offset.x,
        beacon_a.position.y - beacon_b.position.y, #- offset.y,
        beacon_a.position.z + beacon_b.position.z, #- offset.z,
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
            report_data[scanner].append(Beacon(uuid.uuid4(), scanner, Position(x, y, z)))
    return report_data


# Scanner 0 will always be assumed to be the origin point for absolute references
scanner_locations = {0: Position(0, 0, 0)}
report = read_input_file()
print(report)
for scanner_pair in list(combinations(report.keys(), 2)):
    (scanner_a, scanner_b) = scanner_pair
    if compare_fingerprints(fingerprint_beacons(report[scanner_a]), fingerprint_beacons(report[scanner_b])):
        # Find any two matching beacons
        print(f"Match on {scanner_a},{scanner_b}")
        for beacon in report[scanner_a]:
            if beacon.associations:
                if scanner_a in scanner_locations:
                    # print(locate_scanner(beacon, beacon.associations[0], scanner_locations[scanner_a]))
                    new_position = locate_scanner(beacon, beacon.associations[0][1], scanner_locations[scanner_a])
                    scanner_locations[scanner_b] = new_position
                    # Adjust all results to conform with absolute positioning
                  #  for adjusted_beacon in report[scanner_b]:
                    #    adjusted_beacon.position = Position(
                    #       adjusted_beacon.position.x + new_position.x,
                      #     adjusted_beacon.position.y + new_position.y,
                       #    adjusted_beacon.position.z + new_position.z)

                elif scanner_b in scanner_locations:
                    # print(locate_scanner(beacon, beacon.associations[0], scanner_locations[scanner_b]))
                    new_position = locate_scanner(beacon, beacon.associations[0][1], scanner_locations[scanner_b])
                    scanner_locations[scanner_a] = new_position
                    # Adjust all results to conform with absolute positioning
                 #   for adjusted_beacon in report[scanner_a]:
                 #       adjusted_beacon.position = Position(
                   #        adjusted_beacon.position.x + new_position.x,
                 #          adjusted_beacon.position.y + new_position.y,
                    #       adjusted_beacon.position.z + new_position.z)

                print(scanner_locations)
                break

for x in report[0]:
    if x.position.x == -618:
        print(x.position)
        print()
        for a in x.associations:
            print(a)
print(f"Part 1: {len(find_unique_beacons(report))}")
