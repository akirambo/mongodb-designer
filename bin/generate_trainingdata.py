
import pandas as pd
import sys

def get_answer_array(cid, num_of_categories):
    ans = []
    for i in range(num_of_categories):
        if str(i) == cid:
            ans.append("1")
        else:
            ans.append("0")
    return ",".join(ans)


if __name__ == "__main__":
    data = sys.argv[1]
    category = sys.argv[2]
    pattern = sys.argv[3]

    # workload -> id
    w2category_id = {}
    cfile = open(category)
    cline = cfile.readline()
    pfile = open(pattern)
    pline = pfile.readline()
    while cline and pfile:
        workload = pline.strip()
        category_id = cline.strip()
        w2category_id[workload] = category_id
        cline = cfile.readline()
        pline = pfile.readline()
    cfile.close()
    pfile.close()
    with open("data/training_data.csv", "w") as f:
        for workload, cid in w2category_id.items():
            f.write(workload + "," + get_answer_array(cid, 3) + "\n")
    
    dfile = open(data)
    dline = dfile.readline()
    limit = 10
    with open("data/data_with_category.csv", "w") as f:
        while dline:
            data = dline.strip().split(",")[0:70]
            performance = dline.strip().split(",")[80:81][0]
            cid = w2category_id[",".join(data)]
            #print(cid)
            f.write(dline.strip() + "," + performance + "," + cid + "\n")
            dline = dfile.readline()
    dfile.close()
    
