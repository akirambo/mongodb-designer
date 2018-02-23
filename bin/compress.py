

import sys

if __name__ == "__main__":
    elems = []
    outputfile = "workload_pattern.csv"
    inputfile = sys.argv[1]
    f = open(inputfile)
    line = "first"
    while len(line) > 0:
        line = f.readline()
        __tmp__ = line.split(",")
        elem = ",".join(__tmp__[0:70])
        if (elem not in elems) and len(elem) > 0:
            elems.append(elem)
    f.close
    with open(outputfile, "w") as f:
        f.write("\n".join(elems))
