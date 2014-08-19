# Project Euler 015
# Lattice Paths

lattice_values = []

first_row = []

for x in range(21):
    first_row.append(1)

lattice_values.append(first_row)

for x in range(20):
    generic_row = []
    generic_row.append(1)
    for y in range(20):
        generic_row.append(-1)
    lattice_values.append(generic_row)

for x in range(21):
    for y in range(21):
#        print "examining ", x, " ", y
#        print lattice_values[x][y]
        if lattice_values[x][y] == -1:
            lattice_values[x][y] = lattice_values[x-1][y] + lattice_values[x][y-1]
#            print lattice_values[x-1][y]
#            print lattice_values[x][y-1]
#            print lattice_values[x][y]

print lattice_values[20][20]

