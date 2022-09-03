from amino_acid import AminoAcid


r"""
Class name: Protein
Description: A Protein object is a list of AminoAcid objects. It is convenient for mass operations on AminoAcids.
Variables:
    self.pdb_id: PDB ID of the protein
    self.seqlist: A list of Amino Acids
"""

class Protein:

    def __init__(self, seq: str, pdb_id: str):

        r"""
        Object constructor
        :param seq: A string of protein sequence
        :param pdb_id: PDB ID of the protein
        """

        self._pdb_id = pdb_id
        self._seqlist = []
        idx = 1
        for i in seq:
            aa = AminoAcid()
            aa.setnum(f"{idx}")
            aa.setaa(i)
            self._seqlist.append(aa)
            idx += 1

    def display(self):

        r"""
        Print the Protein object
        :return: N/A
        """

        for i in self._seqlist:
            i.aadisplay()

    def checksecstruct(self):

        r"""
        TO BE COMPLETED
        Sets secondary structures for each AminoAcid
        :return: N/A
        """

        return 0


    def checksmem(self):

        r"""
        TO BE COMPLETED
        Sets membrane affiliation for each AminoAcid
        :return: N/A
        """

        return 0


    def checkcons(self):

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
