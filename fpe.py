# fpe - Fast Packaging Engine
# Creates .fpe files
import json, sys, os, requests
def dispgreen(x):
    sys.stdout.write('\x1b[32m')
    sys.stdout.write(x)
    sys.stdout.write('\x1b[39m')
    sys.stdout.flush()
def makefile(manifest, out, code):
    with open(out + ".fpe","wb") as f:
        f.write(("FPEMANIFESTSTART " + json.dumps(manifest) + " FPEMANIFESTEND \27"+code+"\27").encode("utf-8"))
def readfile(name):
    with open(name + ".fpe","rb") as f:
        e = f.read().decode("utf-8")
        m = json.loads(e.split(" FPEMANIFESTEND \27")[0].split("FPEMANIFESTSTART ")[-1])
        co = e.split(" FPEMANIFESTEND \27")[-1][0:-1]
        return m, co
def display_details(x):
    manifest, code = readfile(x)
    print("Name: ")
    dispgreen("\t" + manifest.get("name","unknown"))
    dispgreen("\n")
    print("Description: ")
    dispgreen("\t" + manifest.get("desc"," "))
    dispgreen("\n")
    print("Approximate Size:")
    dispgreen("\t" + str(len(code))+"B")
    dispgreen("\n")
def display_bulk_details(x):
    print("Packages: ")
    s = 0
    dispgreen("\t")
    for package in x:
        man, c = readfile(package)
        dispgreen(man.get("name","unknown") + " ")
        s += len(c)
    dispgreen("\n")
    print("Approximate Size: ")
    dispgreen("\t")
    dispgreen(str(s)+"B")
    dispgreen("\n")
def get_home_directory():
    cd = os.getcwd()
    x = ""
    if os.environ.get("USERPROFILE", "HOME") != "HOME":
        os.chdir(os.environ["USERPROFILE"])
        if not ("fpeenv" in os.listdir()):
            os.mkdir("fpeenv")
        os.chdir("fpeenv")
        x = os.getcwd()
    else:
        os.chdir(os.environ["HOME"])
        if not ("fpeenv" in os.listdir()):
            os.mkdir("fpeenv")
        os.chdir("fpeenv")
        x = os.getcwd()
    os.chdir(cd)
    return x
def get_pkg(x):
    return readfile(os.path.join(get_home_directory(), x))
def install_pkg(x):
    where = os.path.join(get_home_directory(), x)
    man, c = readfile(x)
    makefile(man, where, c)
def print_install_loc():
    print("Installation Location: ")
    dispgreen("\t" + get_home_directory() + "\n")
def ask_yn():
    return (True if input("Install [y/n]? ").strip().lower() == "y" else False)
def abort():
    print("Abort.")
def interactive_installer(pkg):
    if type(pkg) == str:
        display_details(pkg)
        print_install_loc()
        if ask_yn():
            dispgreen("* Installing " + pkg + "...\r")
            install_pkg(pkg)
            dispgreen("* Installing " + pkg + "... Done!\n")
        else:
            abort()
    else:
        display_bulk_details(pkg)
        print_install_loc()
        if ask_yn():
            for p in pkg:
                dispgreen("* Installing " + p + "...\r")
                install_pkg(p)
                dispgreen("* Installing " + p + "... Done!\n")
        else:
            abort()
def run_package(x,a):
    c = compile(readfile(x)[1], "FPE Package "+x, "exec")
    sys.argv = a
    if len(sys.argv) > 0:
        sys.argv = [x] + sys.argv
    else:
        sys.argv = [x]
    globs = {'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': __import__("_frozen_importlib").BuiltinImporter, '__spec__': None, '__annotations__': {}, '__builtins__': __builtins__, 'sys': sys}
    exec(c,globs,globs)
def argv_parse():
    sys.argv.pop(0)
    if len(sys.argv) == 0:
        abort()
    a = sys.argv
    op = a[0]
    if op == "run":
        pn = a.pop(1)
        run_package(os.path.join(get_home_directory(), pn),a)
        sys.exit(0)
    elif op == "install":
        a.pop(0)
        if len(a) > 1:
            interactive_installer(a)
        else:
            interactive_installer(a[0])
        sys.exit(0)
    elif op == "remove":
        try:
            os.remove(os.path.join(get_home_directory(),a[1]+".fpe"))
        except:
            print("Not Installed or Access Denied.")
    elif op == "package":
        n = a[1]
        c = a[2]
        o = a[3]
        cc = ""
        with open(c, encoding="utf-8") as f:
            cc = f.read()
        mm = {"name":n, "desc":"Created Using FPE Package Manager"}
        makefile(mm, o, cc)
    elif op == "disphome":
        dispgreen(get_home_directory()+"\n")
    elif op == "help":
        dispgreen("fpe 1.0\nCreated by codeeleven0\nTHIS SOFTWARE COMES WITH ABSOLUTELY NO WARRANTY!\n\nfpe [operation] [options]\n\n\tinstall [package/packages]\n\t\tInstalls packages.\n\trun [package]\n\t\tRuns a package from FPE Home.\n\tremove [package]\n\t\tRemoves package.\n\tpackage [name] [pyfile] [outfile]\n\t\tCreates FPE packages.\n\tdisphome\n\t\tDisplays FPE Home Directory.\n\thelp\n\t\tDisplays this message.\n\tsh\n\t\tInteractive Shell\n")
    elif op == "sh":
        while True:
            try:
                a = input("% ").strip()
                if a:
                    b = a.split(" ")
                    if len(b) > 0:
                        if b[0] == "exit":
                            sys.exit(0)
                            exit(0)
                            break
                        try:
                            run_package(os.path.join(get_home_directory(),b.pop(0)),b)
                        except:
                            continue
            except KeyboardInterrupt:
                exit()
    else:
        abort()
try:
    argv_parse()
except Exception as x:
    dispgreen("\nDon't panic!\nInstaller had encountered an error.\nException: "+str(x)+"\n")