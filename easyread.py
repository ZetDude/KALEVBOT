def eread(filer):
    try:
        file = open(filer, "r") 
        file.close()
        return file.readlines(0)[0]
    except:
        file = open(filer, "w") 
        file.write('')
        file.close()
        return '0'

def ewrite(filer, txt):
    file = open(filer, "w") 
    file.write(str(txt))
    file.close()