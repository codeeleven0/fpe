import os
a = os.listdir()
na = []
for x in a:
    if x == "compile.py":
        continue
    elif x.endswith(".fpe"):
        continue
    else:
        n = x.split(".py")[0]
        os.system("python fpe.py package {} {} {}".format(n,x,n))
        na.append(n)
os.system("python fpe.py install " + " ".join(na))