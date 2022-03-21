import csv

with open("in.csv") as f, open("out.csv", "w") as out:
    headers = next(f).split()[1:]  # keep headers(for not id)
    for row in f:
        row = row.split()
        time = row[0]
        data = zip(headers, row[1:])  # match correct temp to row item
        for a, b in data:
            out.write("{} {} {}\n".format(time, a.lower(), b))
            print("{} {} {}".format(time, a.lower(), b))

