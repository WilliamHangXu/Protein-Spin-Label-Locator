import requests
import time


class SeqretRunner:

    r"""
    Class name: SeqretRunner
    Description: Runs seqret, a sequence/MSA format converter.
    Variables:
        self.email: user email that gets notification when the job is done.
        self.job_id: job id
        self.seq: sequence/MSA to be converted
        self.mode: the output format. In this context, fasta or clustal.
        self.server_url: seqret server url
        self.out_name: output file name

    Reference:
    Madeira F, Pearce M, Tivey ARN, et al.
    Search and sequence analysis tools services from EMBL-EBI in 2022.

    Nucleic Acids Research. 2022 Apr:gkac240.
    DOI: 10.1093/nar/gkac240. PMID: 35412617; PMCID: PMC9252731.
    """

    def __init__(
            self,
            email: str="",
            job_id: str="",
            seq: str="",
            mode: str = "",
            server_url: str = "https://www.ebi.ac.uk/Tools/services/rest/emboss_seqret/run",
            out_name: str=""
    ):

        r"""
        Object constructor.
        :param email: user email that gets notification when the job is done.
        :param job_id: job id
        :param seq: the sequence/MSA to be converted
        :param mode: the output format. In this context, fasta or clustal.
        :param server_url: url of seqret server
        :param out_name: output file name
        """

        self._email = email
        self._job_id = job_id
        self._seq = seq
        self._mode = mode
        self._server_url = server_url
        self._out_name = out_name

    def _init_id(self) -> str:

        r"""
        Returns the starting text of the output file depending on mode. Used to determine whether the job is finished or not.
        :return: the starting text of the output file
        """

        if self._mode == "fasta":
            return ">"
        if self._mode == "clustal":
            return "CLUSTAL"

    def _post_id(self) -> str:

        r"""
        Returns the postfix of the output file depending on mode.
        :return: the postfix of the output file.
        """

        if self._mode == "fasta":
            return ".fasta"
        if self._mode == "clustal":
            return ".aln"

    def run_job(self):

        r"""
        Runs the job.
        :return: the name of the output file
        """

        print("Submitting job...")
        values = {
            "email": self._email,
            "title": self._job_id,
            "stype": "protein",
            "inputformat": "unknown",
            "outputformat": self._mode,
            "feature": "true",
            "firstonly": "false",
            "reverse": "false",
            "outputcase": "none",
            "seqrange": "START-END",
            "sequence": self._seq
        }
        result = requests.post(self._server_url, data=values).text
        result_url = f"https://www.ebi.ac.uk/Tools/services/rest/emboss_seqret/result/{result}/out"
        print("Converting...")
        while not (requests.get(result_url).text.startswith(self._init_id())):
            time.sleep(1)
        print(f"Fetching {self._mode.upper()} file...")
        with open(self._out_name + self._post_id(), "w") as out:
            out.write(requests.get(result_url).text)
        return self._out_name + self._post_id()



