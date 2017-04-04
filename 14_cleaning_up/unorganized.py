
# Chapter 14: Organizing code

# unstructured code containing redundancies (bad practice)


TILE_POSITIONS = []

for line in open('tiles.txt'):
    print([line])
    # print(dat)
    # if 'REMARK' in dat == True: # didn't work
    TILE_POSITIONS.append([line[0]])
    if line.find('REMARK') != 0:
        x = line[2]
        y = line[4]
        TILE_POSITIONS[-1].append(int(x))
        TILE_POSITIONS[-1].append(int(y))
        # print(TILE_POSITIONS[-1])
    else:
        TILE_POSITIONS.pop()
        line = line.strip()
        print(line[7:])
        continue

print(TILE_POSITIONS)
