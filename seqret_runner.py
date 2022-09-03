import requests
import time


r"""
This is a MSA file format converter runner.

Input: A MSA file in any format
Output: A MSA file in expected format (default: CLUSTAL)

Reference:
Madeira F, Pearce M, Tivey ARN, et al. 
Search and sequence analysis tools services from EMBL-EBI in 2022. 
Nucleic Acids Research. 2022 Apr:gkac240. 
DOI: 10.1093/nar/gkac240. PMID: 35412617; PMCID: PMC9252731.
"""


class SeqretRunner:
    def __init__(
            self,
            email: str="",
            job_id: str="",
            server_url: str="https://www.ebi.ac.uk/Tools/services/rest/emboss_seqret/run",
            mode: str="",
            seq: str="",
            out_name: str=""
    ):
        self.email = email
        self.job_id = job_id
        self.seq = seq
        self.mode = mode
        self.server_url = server_url
        self.out_name = out_name

    def run_job(self):
        print("Submitting job...")
        values = {
            "email": self.email,
            "title": self.job_id,
            "stype": "protein",
            "inputformat": "unknown",
            "outputformat": self.mode,
            "feature": "true",
            "firstonly": "false",
            "reverse": "false",
            "outputcase": "none",
            "seqrange": "START-END",
            "sequence": self.seq
        }
        result = requests.post(self.server_url, data=values).text
        result_url = f"https://www.ebi.ac.uk/Tools/services/rest/emboss_seqret/result/{result}/out"
        print("Converting...")
        while not (requests.get(result_url).text.startswith(self._init_id())):
            time.sleep(1)
        print(f"Fetching {self.mode.upper()} file...")
        with open(self.out_name + self._post_id(), "w") as out:
            out.write(requests.get(result_url).text)
        return self.out_name + self._post_id()

    def _init_id(self):
        if self.mode == "fasta":
            return ">"
        if self.mode == "clustal":
            return "CLUSTAL"

    def _post_id(self):
        if self.mode == "fasta":
            return ".fasta"
        if self.mode == "clustal":
            return ".aln"

