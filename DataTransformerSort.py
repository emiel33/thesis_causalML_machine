import csv


timestep=50
machines=10000
with open("trainData.csv") as f, open("Dtrainout.csv", "w") as out:
    headers = next(f).split(",")[2:]  # keep headers(for not id)
    out.write("id,time,variable,value\n")

    for j in range(machines):
        matrix=[]
        for i in range(timestep):
            row=next(f).split(",")
            matrix.append(row)
        for var in range(len(headers)):
            for val in range(timestep):
                case=matrix[val][0]
                time=matrix[val][1]
                head=headers[var]
                waarde= matrix[val][var+2]
                out.write("{},{},{},{}\n".format(case,time,head.strip('\n'),waarde.strip('\n')))


