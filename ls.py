import os, sys
if len(sys.argv) > 1:
    print("\n".join(os.listdir(sys.argv[1])))
else:
    print("\n".join(os.listdir()))