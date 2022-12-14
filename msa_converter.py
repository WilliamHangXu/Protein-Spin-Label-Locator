import re


def msa_convert(pdb_id):

    r"""
    Converts the MSA file generated by mmseqs2 from a3m format into fasta-like format. Deletes entries with same name.
    Generates a file named pdb_id_MSA.fasta
    :param pdb_id: the PDB ID of the protein
    :return: N/A
    """

    with open(f"{pdb_id}.a3m", "r") as a3:
        lines = a3.readline()
        emt_arr = []
        seen = set()
        while lines[0] == "-" or lines[0] == ">" or lines[0].isalpha():
            if lines.split()[0] not in seen:
                seen.add(lines.split()[0])
                emt_arr.append(lines.split()[0])
            lines = a3.readline()
            lines = a3.readline()
        a3.seek(0)
        with open(f"{pdb_id}_MSA.fasta", "w") as fast:
            line = a3.readline()
            while line[0] == "-" or line[0] == ">" or line[0].isalpha():
                if line.split()[0] in emt_arr:
                    fast.write(line)
                    emt_arr.remove(line.split()[0])
                    line = a3.readline()
                    string = line
                    string = re.sub("[a-z]", "", string)
                    fast.write(string)
                line = a3.readline()
