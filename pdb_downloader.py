import requests
import os


class PDBDownloader:

    r"""
    Class name: PDBDownloader
    Description: given a PDB ID, downloads the PDB file from Protein Data Bank
    Variables:
        self._host_url: the url of Protein Data Bank
        self._pdb_id: PDB ID
    """

    def __init__(
            self,
            host_url: str = "https://files.rcsb.org/view/",
    ):

        r"""
        Object constructor.
        :param host_url: the url of Protein Data Bank
        """

        self._host_url = host_url
        self._pdb_id = ""

    def get_user_input(self) -> str:

        r"""
        Gets user input for PDB ID and verify.
        :return: A valid PDB ID
        """

        pdbid = input("Please give your PDB ID: ")
        url = f"{self._host_url}{pdbid}.pdb"
        while not requests.get(url).text.startswith("HEADER"):
            pdbid = input("PDB ID invalid. Please try again: ")
            url = f"{self._host_url}{pdbid}.pdb"
        self._pdb_id = pdbid
        return pdbid

    def download_pdb(self) -> str:

        r"""
        Downloads the PDB file.
        :return: The path to which the PDB file is stored
        """

        current_dir = os.getcwd()
        with open(self._pdb_id + ".pdb", "w") as out:
            out.write(requests.get(f"{self._host_url}{self._pdb_id}.pdb").text)
        return os.path.join(current_dir, f"{self._pdb_id}.pdb")