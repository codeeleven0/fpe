import sys
exec(compile(open(sys.argv[1],encoding="utf-8").read(),sys.argv[1],"exec"), globals(), locals())