def eread(filer):
    try:
        with open(filer, "r") as file:
            return file.readlines(0)[0]
    except Exception as e:
        print(e)
        file = open(filer, "w") 
        file.write('')
        file.close()
        return '0'

def ewrite(filer, txt):
    file = open(filer, "w") 
    file.write(str(txt))
    file.close()