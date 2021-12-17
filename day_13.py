from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

with open('inputs/day_13.txt') as f:
    lines = f.read().split("\n")
    points = []
    for row in lines:
        if "" == row:
            break
        else:
            [x, y] = row.split(",")
            points.append([int(x), int(y)])

def count_dots(points):
    pass

def get_dimensions(points):
    max_x = 0
    max_y = 0
    for point in points:
        if point[0] > max_x: max_x = point[0]
        if point[1] > max_y: max_y= point[1]
    return [max_x, max_y]

def build_image(points):
    with Drawing() as draw:
        for point in points:
            draw.fill_color = Color('black')
            draw.point(point[0], point[1])
        [width, height] = get_dimensions(points)
        print(get_dimensions(points))
        with Image(width=width, height=height, background=Color('transparent')) as image:
            draw(image)
            image.save(filename='day_13.png')