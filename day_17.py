# 
# Part 2 Only - See Javascript for Part 1
#
from dataclasses import dataclass

@dataclass
class Target:
    x_min: int
    x_max: int
    y_min: int
    y_max: int

class Shot:
    x: int
    y: int
    vx: int
    vy: int
    hit: bool

    def __init__(self, vx: int, vy: int):
        self.x = 0
        self.y = 0
        self.vx = vx
        self.vy = vy
        self.hit = False

    def step(self) -> None:
        self.x += self.vx
        self.y += self.vy
        if self.vx > 0:
            self.vx -= 1
        if self.vx < 0:
            self.vx += 1
        self.vy -= 1

    def check_for_hit(self, target: Target) -> bool:
        if target.x_min <= self.x and self.x <= target.x_max and target.y_min <= self.y and self.y <= target.y_max:
            self.hit = True

    def __str__(self):
        return f"({self.x},{self.y}) - Hit? {self.hit}"

def run_firing_solution(vx: int, vy: int, target: Target):
    shot = Shot(vx, vy)
    while True:
        shot.step()
        shot.check_for_hit(target)
        if shot.y < target.y_min or shot.hit:
            return shot

target = Target(153, 199, -114, -75)

hits = 0
for x in range(0, 200):
    for y in range(-abs(target.x_min), (target.x_min)):
        if (run_firing_solution(x, y, target).hit):
            hits += 1
print(f"Total Hits: {hits}")



