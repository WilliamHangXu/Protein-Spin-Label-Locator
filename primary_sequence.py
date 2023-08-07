def get_seq(PDB_path: str) -> str:

    r"""
    Given a protein sequence where all residues are denoted by 3-letter codes, converts it into a sequence where
    residues are denoted by 1-letter codes.
    :param PDB_path: The path that contains the PDB file
    :return: a protein sequence
    """

    # A dictionary that converts three-letter codes into one-letter codes for amino acids
    d3to1 = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
     'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N',
     'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W',
     'ALA': 'A', 'VAL':'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'}

    # Read file
    with open(PDB_path, "r") as file:
        line = file.readline()
        while not line.startswith("SEQRES"):
            line = file.readline()
        chain_id = line.split()[2]
        seq = ""
        while line.split()[2] == chain_id:
            for aa_3 in line.split()[4:]:
                seq += d3to1[aa_3]
            line = file.readline()

    return seq







