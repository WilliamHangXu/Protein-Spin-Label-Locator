class AminoAcid:

    def __init__(
            self,
            num = "",
            aa = "",
            cons = False,
            mem = False,
            secstruct = False
                 ):
        self._num = num
        self._aa = aa
        self._cons = cons
        self._mem = mem
        self._secstruct = secstruct

    def setnum(self, num):
        self._num = num

    def settype(self, aatype):
        self._aa = aatype

    def setcons(self):
        self._cons = True

    def setmem(self):
        self._mem = True

    def setsecstruct(self):
        self._secstruct = True

    def getnum(self):
        return self._num

    def gettype(self):
        return self._aa

    def getcons(self):
        return self._cons

    def getmem(self):
        return self.getmem()

    def getsecstruct(self):
        return self._secstruct

    def aadisplay(self):
        str = ""
        str += self._num
        str += self._aa
        if self._cons:
            str += "1"
        else:
            str += "0"
        if self._mem:
            str += "1"
        else:
            str += "0"
        if self._secstruct:
            str += "1"
        else:
            str += "0"
        print(str)



