import  random
fplan = open("randomplan.csv", "w")
fplan.write("id,starttime,step1,step2,step3,step4,step5\n")

for i in range(0,100):
    line = "{},20,{},{},{},{},{}\n".format(i, random.randint(0,1), random.randint(0,1),
                                           random.randint(0, 1), random.randint(0,1),
                                           random.randint(0, 1))
    fplan.write(line)

fplan.close()