class AminoAcid:

    r"""
    Class name: AminoAcid
    Description: An AminoAcid object represents an amino acid residue in a protein sequence. It records the identity, position,
                 conservation score, secondary structure assignment, and membrane affiliation.
    Variables:
        self._num: the position of the residue in the protein
        self._aa: the identity of the residue (single-letter amino acid name)
        self._cons: the conservation score of the residue (from the ConSurf server)
        self._mem: the membrane affiliation (from the Topcons server)
        self._secstruct: the type of secondary structure the residue is in (from DSSP)
    """

    def __init__(
            self,
            num = "",
            aa = "",
            cons: float = 0,
            mem: str = "",
            secstruct: str = ""
                 ):

        r"""
        Object constructor.
        :param num: the position of the residue in the protein
        :param aa: the identity of the residue (single-letter amino acid name)
        :param cons: the conservation score of the residue (from the ConSurf server)
        :param mem: the membrane affiliation (from the Topcons server, should be a single letter)
        :param secstruct: the type of secondary structure the residue is in (from DSSP, should be a single letter or empty)
        """

        self._num = num
        self._aa = aa
        self._cons = cons
        self._mem = mem
        self._secstruct = secstruct

    def set_num(self, num: str):

        r"""
        Sets num.
        :param num
        :return: N/A
        """

        self._num = num

    def set_aa(self, aatype: str):

        r"""
        Sets amino acid identity.
        :param aatype: single letter amino acid code
        :return: N/A
        """

        self._aa = aatype

    def set_cons(self, cons: float):

        r"""
        Sets conservation score.
        :param cons: conservation score
        :return: N/A
        """

        self._cons = cons

    def set_mem(self, mem: str):

        r"""
        Sets membrane affiliation information
        :param mem: membrane affiliation
        :return: N/A
        """

        self._mem = mem

    def set_secstruct(self, secstruct):

        r"""
        Sets secondary structure information
        :param secstruct: secondary structure
        :return: N/A
        """

        self._secstruct = secstruct

    def get_num(self) -> str:

        r"""
        Returns num.
        :return: num
        """

        return self._num

    def get_aa(self) -> str:

        r"""
        Returns aa.
        :return: aa
        """

        return self._aa

    def get_cons(self) -> float:

        r"""
        Returns cons.
        :return: cons
        """

        return self._cons

    def get_mem(self) -> str:

        r"""
        Returns mem.
        :return: mem
        """

        return self._mem

    def get_secstruct(self) -> str:

        r"""
        Returns secstruct.
        :return: secstruct
        """

        return self._secstruct

    def aa_display(self):

        r"""
        Prints all stored information in the amino acid object in a ordered manner.
        :return: N/A
        """

        str = f"{self._num} {self._aa} {self._mem} {self._cons} {self._secstruct}"
        print(str)



