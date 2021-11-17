import sys

infile = sys.argv[1]
outfile = sys.argv[2]

file = open(infile, "r")
data = file.readlines()
out = open(outfile, "w")

metadata = data[0]
w, h, COLORSPACE = metadata.split()
WIDTH = int(w)
HEIGHT = int(h)


def list_to_str(arr=list) -> str:
    """ Turns a list in to a string """
    output = ""
    for i in arr:
        output += i
    return output


# everything = [["x"] * (WIDTH * HEIGHT)] * (len(data))
everything = [["x" for i in range(WIDTH * HEIGHT)] for j in range(len(data))]

for line in range(1, len(data)):
    for pixel in range(WIDTH * HEIGHT):
        everything[line][pixel] = data[line][pixel]

rotated = list(zip(*everything))[::-1]

# writes it out to the file
out.write("    array<string> animation = []\n")

for e in rotated:
    out.write(f'    animation.append( "{list_to_str(e)}" )\n')

