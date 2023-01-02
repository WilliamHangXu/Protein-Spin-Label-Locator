import json
import requests
import time


class DSSPRunner:

    r"""
    Class name: DSSPRunner
    Description: This program runs Dictionary of Secondary Structure of Proteins (DSSP) through the XSSP API.
                 Uploads a PDB file and get a .dssp file.
                 https://github.com/cmbi/xssp-api
                 Modified from the provided sample API.
                 The server crashes very often. In that case, please contact the developer on GitHub.
    Variables:
        self.file_name: the PDB file to be uploaded
        self.server_url: the url of the server
        self.job_id: job id

    Reference:
    A series of PDB related databases for everyday needs.
    Wouter G Touw, Coos Baakman, Jon Black, Tim AH te Beek, E Krieger, Robbie P Joosten, Gert Vriend.
    Nucleic Acids Research 2015 January; 43(Database issue): D364-D368.

    Dictionary of protein secondary structure: pattern recognition of hydrogen-bonded and geometrical features.
    Kabsch W, Sander C,
    Biopolymers. 1983 22 2577-2637.
    PMID: 6667333; UI: 84128824.
    """

    def __init__(
            self,
            file_name: str = "",
            server_url: str = "https://www3.cmbi.umcn.nl/xssp/",
    ):

        r"""
        Object constructor
        :param file_name: the PDB file to be uploaded
        :param server_url: the server url
        """

        self._file_name = file_name
        self._server_url = server_url
        self._job_id = ""

    def _submit_job(self):

        r"""
        Submits job.
        :return: N/A
        """

        # Upload PDB file
        print("Submitting DSSP job to server...")
        with open(f"{self._file_name}.pdb", 'rb') as PDB_file:
            url_create = f"{self._server_url}api/create/pdb_file/dssp/"
            files = {'file_': PDB_file}
            r = requests.post(url_create, files=files)
        r.raise_for_status()
        job_id = json.loads(r.text)['id']
        self._job_id = job_id
        print("Job submitted successfully. Id is: '{}'".format(job_id))
        print("Processing your job...")


    def _get_status(self, r) -> str:

        r"""
        Gets job status.
        :param r: a requests object of the server
        :return: the status of the job
        """

        r.raise_for_status()
        status = json.loads(r.text)['status']
        return status

    def _get_result(self):

        r"""
        Downloads the result as a .dssp file
        :return: N/A
        """

        url_result = '{}api/result/pdb_file/dssp/{}/'.format(self._server_url, self._job_id)
        r = requests.get(url_result)
        r.raise_for_status()
        result = json.loads(r.text)['result']

        with open(f"{self._file_name}.dssp", "w") as out:
            out.write(result)

    def run_job(self):

        r"""
        Runs the job.
        :return: N/A
        """

        self._submit_job()
        ready = False
        while not ready:
            url_status = f'{self._server_url}api/status/pdb_file/dssp/{self._job_id}/'
            r = requests.get(url_status)
            status = self._get_status(r)
            if status == 'SUCCESS':
                ready = True
            elif status in ['FAILURE', 'REVOKED']:
                raise Exception(json.loads(r.text)['message'])
            else:
                time.sleep(5)
        self._get_result()
        print(f"{self._file_name}.dssp generated successfully.")