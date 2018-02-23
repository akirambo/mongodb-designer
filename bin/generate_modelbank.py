
import pandas as pd
import sys

class Category:
    def __init__(self, id):
        self.category_id = id
        self.data = {}
        self.max_linenum = -1

    def append(self, linenum, latency):
        if len(list(self.data.keys())) > 10:
            if self.data[self.max_linenum] < latency:
               del self.data[self.max_linenum]
               self.max_linenum = linenum
               self.data[linenum] = latency
        else:
            if self.max_linenum == -1 or self.data[self.max_linenum] < latency:
                self.max_linenum = linenum
            self.data[linenum] = latency

    def output(self):
        keys = sorted(self.data, key=self.data.get)
        keys.reverse()
        return str(self.category_id) + "," + ",".join(str(x) for x in keys)

    
if __name__ == "__main__":
    filename = sys.argv[1]
    file = open(filename)
    # { categoly_id : [line number in data.csv (perfomane best 10)]}
    data = {}
    line = file.readline()
    linenum = 0
    while line:
        linenum += 1
        tmp = line.strip()
        tmp = tmp.split(",")
        latency = float(tmp[131:132][0])
        category = int(tmp[132:133][0])
        if category not in data.keys():
            data[category] = Category(category)
        data[category].append(linenum, latency)
        line = file.readline()
    file.close()
    buf = []
    for id, elem in data.items():
        buf.append(elem.output())
    with open("data/databank_meta.csv", "w") as f:
        f.write("\n".join(buf))
    
