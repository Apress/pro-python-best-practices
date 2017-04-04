

# Chapter 14: loading tile positions from a file

# CODE GOLF: using as few key strokes as possible (bad practice)

xyconv = lambda x: [x[0], int(x[1]), int(x[2])]
tile_positions = list(map(xyconv, [l.split('\t') for l in open('tiles.txt') if l[0]!='R']))

print(tile_positions)
