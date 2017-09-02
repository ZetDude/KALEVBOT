def eread(filer):
    file = open(filer, "r") 
    return file.readlines(0)[0]
    file.close()

def ewrite(filer, txt):
    file = open(filer, "w") 
    file.write(str(txt))
    file.close()