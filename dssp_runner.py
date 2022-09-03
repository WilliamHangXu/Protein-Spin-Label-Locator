import json
import requests
import time


r"""
This program runs Dictionary of Secondary Structure of Proteins (DSSP) through the XSSP API.
Modified from the provided sample API.
The server crashes very often. In that case, please contact the developer on GitHub.

Input: a PDB file (default) or a PDB ID
Output: a .dssp file

Reference:
A series of PDB related databases for everyday needs.
Wouter G Touw, Coos Baakman, Jon Black, Tim AH te Beek, E Krieger, Robbie P Joosten, Gert Vriend.
Nucleic Acids Research 2015 January; 43(Database issue): D364-D368.

Dictionary of protein secondary structure: pattern recognition of hydrogen-bonded and geometrical features.
Kabsch W, Sander C,
Biopolymers. 1983 22 2577-2637.
PMID: 6667333; UI: 84128824.
"""


class DSSPRunner:
    def __init__(
            self,
            file_name: str = "",
            server_url: str = "https://www3.cmbi.umcn.nl/xssp/",
    ):
        self.server_url = server_url
        self.file_name = file_name
        self.job_id = ""

    def _submit_job(self):
        # Upload PDB file
        print("Submitting DSSP job to server...")
        with open(f"{self.file_name}.pdb", 'rb') as PDB_file:
            url_create = f"{self.server_url}api/create/pdb_file/dssp/"
            files = {'file_': PDB_file}
            r = requests.post(url_create, files=files)
        r.raise_for_status()
        job_id = json.loads(r.text)['id']
        self.job_id = job_id
        print("Job submitted successfully. Id is: '{}'".format(job_id))
        print("Processing your job...")


    def _get_status(self, r):
        # Check the status of the running job. If an error occurs an exception
        # is raised and the program exits. If the request is successful, the
        # status is returned.
        r.raise_for_status()
        status = json.loads(r.text)['status']
        return status

    def _get_result(self):
        # Requests the result of the job. If an error occurs an exception is
        # raised and the program exits. If the request is successful, the result
        # is returned.
        url_result = '{}api/result/pdb_file/dssp/{}/'.format(self.server_url, self.job_id)
        r = requests.get(url_result)
        r.raise_for_status()
        result = json.loads(r.text)['result']

        # Return the result to the caller, which prints it to the screen.
        with open(f"{self.file_name}.dssp", "w") as out:
            out.write(result)

    def run_job(self):
        self._submit_job()
        ready = False
        while not ready:
            url_status = f'{self.server_url}api/status/pdb_file/dssp/{self.job_id}/'
            r = requests.get(url_status)
            status = self._get_status(r)
            if status == 'SUCCESS':
                ready = True
            elif status in ['FAILURE', 'REVOKED']:
                raise Exception(json.loads(r.text)['message'])
            else:
                time.sleep(5)
        self._get_result()
        print(f"{self.file_name}.dssp generated successfully.")