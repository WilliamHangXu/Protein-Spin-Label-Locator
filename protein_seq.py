from amino_acid import AminoAcid

class Protein:

    def __init__(self, seq, pdb_id):
        self.pdb_id = pdb_id
        self.seqlist = []
        idx = 1
        for i in seq:
            aa = AminoAcid()
            aa.setnum(f"{idx}")
            aa.settype(i)
            self.seqlist.append(aa)
            idx += 1

    def display(self):
        for i in self.seqlist:
            i.aadisplay()

    # def checksecstruct(self, secstruct=[]):
    #
    #
    # def checksmem(self):
    #
    #
    # def checkcons(self, bound):
    #
    # def result(self):
    #     with open(f"{self.pdb_id}_SUMMARY.txt", "w") as out:
    #         out.write("")
