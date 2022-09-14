from amino_acid import AminoAcid


class Protein:

    r"""
    Class name: Protein
    Description: A Protein object is a list of AminoAcid objects. It is convenient for mass operations on AminoAcids.
    Variables:
        self.pdb_id: PDB ID of the protein
        self.seqdict: A dictionary with keys being chain ids and values being lists of AminoAcids.
    """

    def __init__(self, pdb_id: str):

        r"""
        Object constructor.
        :param pdb_id: PDB ID of the protein
        """

        self._pdb_id = pdb_id
        self._seqdict = {}
        with open(f"{self._pdb_id}.pdb", "r") as file:
            line = file.readline()
            while not line.startswith("ATOM"):
                line = file.readline()
            while line.startswith("ATOM") or line.startswith("TER"):
                chainID = line.split()[4]
                self._seqdict[chainID] = []
                while line.startswith("ATOM"):
                    order = line.split()[5]
                    aa = AminoAcid(num=line.split()[5], chain_id=chainID, aa=line.split()[3])
                    self._seqdict[chainID].append(aa)
                    while line.startswith("ATOM") and line.split()[5] == order:
                        line = file.readline()
                if line.startswith("TER"):
                    line = file.readline()

    def display(self):

        r"""
        Print the Protein object
        :return: N/A
        """

        for i in self._seqdict:
            for j in self._seqdict[i]:
                j.aa_display()

    def get_length(self) -> int:

        r"""
        Get the number of residues stored in the Protein object.
        :return:
        """

        length = 0
        for i in self._seqdict:
            length += len(self._seqdict[i])
        return length

    def check_secstruct(self):

        r"""
        Reads the .dssp file and sets secondary structures for each AminoAcid.
        :return: N/A
        """

        with open(f"{self._pdb_id}.dssp", "r") as file:
            line = file.readline()
            while not line.startswith("  #  RESIDUE AA STRUCTURE"):
                line = file.readline()
            line = file.readline()
            while line != "":
                chainID = line.split()[2]
                idx = 0
                while line != "" and line.split()[2] == chainID:
                    if line.split()[4] in "HBEGITS":
                        self._seqdict[line.split()[2]][idx].set_secstruct(line.split()[4])
                    else:
                        self._seqdict[line.split()[2]][idx].set_secstruct("n")
                    idx += 1
                    line = file.readline()
                if line != "":
                    line = file.readline()
                else:
                    break

    def check_mem(self):

        r"""
        TO BE COMPLETED
        Sets membrane affiliation for each AminoAcid
        :return: N/A
        """

        # with open(f"{self._pdb_id}_MEM.txt", "r") as file:





        return 0


    def check_cons(self):

        r"""
        TO BE COMPLETED
        Sets conservation scores for each AminoAcid
        :return: N/A
        """

        return 0

    def result(self) -> str:

        r"""
        Display all information in the Protein in a text file.
        :return: the path to which the file is stored
        """

        with open(f"{self._pdb_id}_SUMMARY.txt", "w") as out:
            out.write("")

        return ""
