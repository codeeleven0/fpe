import os
a = os.listdir()
na = []
for x in a:
    if x == "compile.py":
        continue
    elif x == "README.md":
        continue
    elif x.endswith(".fpe"):
        continue
    elif x.endswith(".py"):
        n = x.split(".py")[0]
        os.system("python fpe.py package {} {} {}".format(n,x,n))
        na.append(n)
    else:
        continue
os.system("python fpe.py install " + " ".join(na))