
treatmentplans= ["ones","zeros","interval","random"]
#treatmentplans= ["ones"]

for plan in treatmentplans:
    with open(plan+".csv") as f, open("evalplan.csv", "a") as out:
        headers=next(f)
        totals=[0]*100
        for row in f:
            row=row.split(",")
            id=int(row[0])
            time=int(row[1])
            volume=float(row[7])
            if time>=20 and time<=24:
                totals[id]+=volume
        out.write(plan+","+str(totals).strip("[").strip("]")+"\n")