import requests
import os


class PDBDownloader:

    def __init__(
            self,
            host_url: str = "https://files.rcsb.org/view/",
    ):
        self._host_url = host_url
        self._pdb_id = ""

    def get_user_input(self):
        pdbid = input("Please give your PDB ID: ")
        url = f"{self._host_url}{pdbid}.pdb"
        while not requests.get(url).text.startswith("HEADER"):
            pdbid = input("PDB ID invalid. Please try again: ")
            url = f"{self._host_url}{pdbid}.pdb"
        self._pdb_id = pdbid
        return pdbid

    def download_pdb(self):
        current_dir = os.getcwd()
        with open(self._pdb_id + ".pdb", "w") as out:
            out.write(requests.get(f"{self._host_url}{self._pdb_id}.pdb").text)
        return os.path.join(current_dir, f"{self._pdb_id}.pdb")