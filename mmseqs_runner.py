import hashlib
import numpy as np
import os
import re
import requests
import tarfile
import time

from absl import logging
from typing import NoReturn


class MMSeqs2Runner:

    r"""Runner object
    NOTE: This is a slightly modified version of Diego del Alamo (github: delalamo)'s mmseqs2.py

    Fetches sequence alignment and templates from MMSeqs2 server
    Based on the function run_mmseqs2 from ColabFold (sokrypton/ColabFold)
    Version 62d7558c91a9809712b022faf9d91d8b183c328c
    Relevant publications
    ----------
    * "Clustering huge protein sequence sets in linear time"
      https://doi.org/10.1038/s41467-018-04964-5
    * "MMseqs2 enables sensitive protein sequence searching for the analysis
      of massive data sets"
      https://doi.org/10.1038/nbt.3988
    Private variables
    ----------
    self.job: Job ID (five-char string)
    self.seq: Sequence to search
    self.host_url: URL address to ping for data
    self.t_url: URL address to ping for templates from PDB
    self.n_templates = Number of templates to fetch (default=20)
    self.path: Path to use
    self.tarfile: Compressed file archive to download
    """

    def __init__(
        self,
        job: str,
        seq: str,
        host_url: str = "https://a3m.mmseqs.com",
        t_url: str = "https://a3m-templates.mmseqs.com/template",
        n_templates: int = 20,
    ):

        r"""Initialize runner object
        Parameters
        ----------
        job : Job name
        seq : Amino acid sequence
        host_url : Website to ping for sequence data
        t_url : Website to ping for template info
        """

        # Clean up sequence
        self.seq = self._cleanseq(seq.upper())

        # Come up with unique job ID for MMSeqs
        self.job = self._define_jobname(job)

        # Save everything else
        self.host_url = host_url
        self.t_url = t_url
        self.n_templates = n_templates

        self.path = "mmseqs_result"

        if not os.path.isdir(self.path):
            os.system(f"mkdir { self.path }")

        self.tarfile = f"{ self.path }/out.tar.gz"

    def _cleanseq(self, seq) -> str:

        r"""Cleans the sequence to remove whitespace and noncanonical letters
        Parameters
        ----------
        seq : Amino acid sequence (only all 20 here)
        Returns
        ----------
        Cleaned up amin acid sequence
        """

        if any([aa in seq for aa in "BJOUXZ"]):
            logging.warning("Sequence contains non-canonical amino acids!")
            logging.warning("Removing B, J, O, U, X, and Z from sequence")
            seq = re.sub(r"[BJOUXZ]", "", seq)

        return re.sub(r"[^A-Z]", "", "".join(seq.split()))

    def _define_jobname(self, job: str) -> str:

        r"""Provides a unique five-digit identifier for the job name
        Parameters
        ----------
        job : Job name
        Returns
        ----------
        Defined job name
        """

        return "_".join(
            (
                re.sub(r"\W+", "", "".join(job.split())),
                hashlib.sha1(self.seq.encode()).hexdigest()[:5],
            )
        )

    def _submit(self) -> dict:

        r"""Submit job to MMSeqs2 server
        Parameters
        ----------
        None
        Returns
        ----------
        None
        """

        data = {"q": f">101\n{ self.seq }", "mode": "env"}

        res = requests.post(f"{ self.host_url }/ticket/msa", data=data)

        try:
            out = res.json()

        except ValueError:
            out = {"status": "UNKNOWN"}

        return out

    def _status(self, idx: str) -> dict:

        r"""Check status of job
        Parameters
        ----------
        idx : Index assigned by MMSeqs2 server
        Returns
        ----------
        None
        """

        res = requests.get(f"{ self.host_url }/ticket/{ idx }")

        try:
            out = res.json()

        except ValueError:
            out = {"status": "UNKNOWN"}

        return out

    def _download(self, idx: str, path: str) -> NoReturn:

        r"""Download job outputs
        Parameters
        ----------
        idx : Index assigned by MMSeqs2 server
        path : Path to download data
        Returns
        ----------
        None
        """

        res = requests.get(f"{ self.host_url }/result/download/{ idx }")

        with open(path, "wb") as out:
            out.write(res.content)

    def _search_mmseqs2(self) -> NoReturn:

        r"""Run the search and download results
        Heavily modified from ColabFold
        Parameters
        ----------
        None
        Returns
        ----------
        None
        """

        if os.path.isfile(self.tarfile):
            return

        out = self._submit()

        time.sleep(5 + np.random.randint(0, 5))
        while out["status"] in ["UNKNOWN", "RATELIMIT"]:
            # resubmit
            time.sleep(5 + np.random.randint(0, 5))
            out = self._submit()
        print("MMSeqs job submitted...")

        logging.debug(f"ID: { out[ 'id' ] }")

        while out["status"] in ["UNKNOWN", "RUNNING", "PENDING"]:
            time.sleep(5 + np.random.randint(0, 5))
            out = self._status(out["id"])

        if out["status"] == "COMPLETE":
            print("Starting to download .a3m file...")
            self._download(out["id"], self.tarfile)

        elif out["status"] == "ERROR":
            raise RuntimeError(
                " ".join(
                    (
                        "MMseqs2 API is giving errors.",
                        "Please confirm your input is a valid protein sequence.",
                        "If error persists, please try again in an hour.",
                    )
                )
            )

    # Modifications here
    def run_job(self, pdb_id):

        r"""
        Run sequence alignments using MMseqs2
        Parameters
        ----------
        use_templates: Whether to use templates
        Returns
        ----------
        Tuple with [0] string with alignment, and [1] path to template
        :param pdb_id: pdb id
        """

        self._search_mmseqs2()

        # extract a3m files
        if not os.path.isfile(os.path.join(self.path, "uniref.a3m")):
            with tarfile.open(self.tarfile) as tar_gz:
                tar_gz.extractall(self.path)
                for member in tar_gz.getmembers():
                    if "uniref.a3m" in member.name:
                        tar_gz.extract(member)
        os.rename("uniref.a3m", f"{pdb_id}.a3m")