import os#cikis yapmak icin
class parser(object):
    def __init__(self):
        self.operators = ["*", "/", "+", "-"]#islem onceligi
        self.numbers = list("0123456789")

    def clear_whitespace(self, data):
        return data.replace(" ", "")

    def process(self, token):#her token 3 elemandan olusmali
        chunks = [""]
        for char in token:
            if not char in self.operators:
                if not chunks[-1] in self.operators:
                    chunks[-1] += char
                else:
                    chunks.append(char)
            else:
                chunks.append(char)


        while "-" in chunks or "--" in chunks:
            if "--" in chunks:
                del chunks[chunks.index("--")]
                continue
            if "-" in chunks:
                if chunks[chunks.index("-")+1]== "+":
                    del chunks[chunks.index("-")+1]
                    continue
                if chunks[chunks.index("-")+1]== "-":
                    del chunks[chunks.index("-")+1]
                    del chunks[chunks.index("-")]
                    continue
                liste = list(chunks[chunks.index("-")+1])
                tempindex = chunks.index("-")+1
                liste.reverse()
                if not liste[-1]== "-":
                    liste += "-"
                    liste.reverse()
                    chunks[chunks.index("-")+1]= "".join(liste)
                    chunks[chunks.index("-")] = "+"
                else:
                    liste.pop()
                    liste.reverse()
                    chunks[tempindex] = "".join(liste)
                    chunks[tempindex-1] = "+"

        index = 0
        remlist = []

        for idx in chunks:
            if chunks[index] == "+":
                if chunks[index + 1] =="+":
                    remlist.append(index)
            index += 1
        remcount = 0
        for idx in remlist:
            del chunks[idx-remcount]
            remcount += 1

        index = 0
        remlist = []
        for idx in chunks:
            if idx == "/" or idx == "*":
                if chunks[index-1] == "+":
                    remlist.append(index-1)
                if chunks[index+1] == "+":
                    remlist.append(index +1)
            index += 1
        remcount = 0
        remlist_actual = []
        for idx in remlist:
            if remlist_actual.count(idx) == 0:
                remlist_actual.append(idx)
        remlist_actual = sorted(remlist_actual)
        for idx in remlist_actual:
            del chunks[idx-remcount]
            remcount += 1
        index = 0
        for idx in chunks:
            if idx == "/" and chunks[index +1] == "*":
                return False
            if idx == "*" and chunks[index + 1] == "/":
                return False
            if idx == "*" and chunks[index + 1] == "*":
                return False
            if idx == "/" and chunks[index + 1] == "/":
                return False
            index += 1
        for op in self.operators:
            while not chunks.count(op) == 0:
                index = 0
                for ndx in chunks:
                    if ndx == op:
                        print(chunks)
                        var1 = float(chunks[index-1])
                        var2 = float(chunks[index+1])
                        result = self.switch_case(op)(var1, var2)
                        chunks[index] = result
                        del chunks[index -1]
                        del chunks[index]#index 1 geriye kayiyor
                    index += 1

        return chunks[0]


    def handle(self, data):
        if not self.control(data):
            return False
        data = self.clear_whitespace(data)
        if "(" in data:
            while "(" in data:
                data = self.process_pharantesis(data)
        result = self.process(data)
        print("Islem sonucu: {}".format(str(result)))

    def control(self, data):#error throwing
        check = list(data)
        if not check.count("(") == check.count(")"):
            print("Parantezler Ile Ilgili Bir Problem Olustu..")
            return False
        return True


    def process_pharantesis(self, data):#()
        open_count = 0
        rsplitted = data.split(")")
        lsplitted = rsplitted[0]
        splitted = lsplitted.split("(")[-1]
        result = self.process(splitted)
        lsplitted = lsplitted.split("(")
        lsplitted.pop()
        lsplitted[-1]+=str(result)
        lsplitted = "(".join(lsplitted)
        rsplitted.pop(0)
        rsplitted = ")".join(rsplitted)
        return lsplitted + rsplitted


    def switch_case(self, case):
        switches = {"+":lambda x, y: x+y,
                    "-":lambda x, y: x-y,
                    "*":lambda x, y: x*y,
                    "/":lambda x, y: x/y}
        return switches[case]

def main():
    obj = parser()
    os.system("clear")
    print("\n\n\tMath Parser\n\tCreated By:Atlj\n\tgithub.com/atlj\n\n")
    while 1:
        inp = input("Lutfen Islenecek Veriyi Giriniz>> ")
        obj.handle(inp)
        print("\n")
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCikiliyor")
        os._exit(0)
