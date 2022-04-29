import csv

with open("test.csv") as f, open("Dtestout.csv", "w") as out:
    headers = next(f).split(",")[2:]  # keep headers(for not id)
    for row in f:
        row = row.split(",")
        time = row[1]
        case = row[0]
        data = zip(headers, row[2:])  # match correct value to row item
        for a, b in data:
            out.write("{},{},{},{}\n".format(case,time, a.lower().strip('\n'), b.strip('\n')))
            print("{} {} {} {}".format(case,time, a.lower(), b))

