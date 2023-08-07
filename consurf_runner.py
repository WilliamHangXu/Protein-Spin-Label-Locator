import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import requests


class ConsurfRunner:

    r"""
    Classname: ConsurfRunner
    Description: runs the Consurf server to calculate the conservation score for each residue in a protein.
    Variables:
        self.pdb_id: PDB ID of the protein
        self.email: User's email that receives notification when the job is done
        self.job_id: Job ID for the job.
        self.chain_id: Chain Identifier in the PDB file
        self.q_seq: query sequence of MSA.

    Input: the required parameters of the server, including a PDB file and a MSA file (in clustal format)
    Output: a text file containing conservation score for each amino acid.

    Reference:
    Ashkenazy H., Abadi S., Martz E., Chay O., Mayrose I., Pupko T., and Ben-Tal N. 2016
    ConSurf 2016: an improved methodology to estimate and visualize evolutionary conservation in macromolecules
    Nucl. Acids Res. 2016; DOI: 10.1093/nar/gkw408; PMID: 27166375

    Celniker G., Nimrod G., Ashkenazy H., Glaser F., Martz E., Mayrose I., Pupko T., and Ben-Tal N. 2013.
    ConSurf: Using Evolutionary Data to Raise Testable Hypotheses about Protein Function
    Isr. J. Chem. 2013 March 10, doi: 10.1002/ijch.201200096

    Ashkenazy H., Erez E., Martz E., Pupko T. and Ben-Tal N. 2010
    ConSurf 2010: calculating evolutionary conservation in sequence and structure of proteins and nucleic acids.
    Nucl. Acids Res. 2010; DOI: 10.1093/nar/gkq399; PMID: 20478830

    Landau M., Mayrose I., Rosenberg Y., Glaser F., Martz E., Pupko T. and Ben-Tal N. 2005.
    ConSurf 2005: the projection of evolutionary conservation scores of residues on protein structures.
    Nucl. Acids Res. 33:W299-W302.

    Glaser F., Pupko T., Paz I., Bell R.E., Bechor D., Martz E. and Ben-Tal N. 2003.
    ConSurf: Identification of Functional Regions in Proteins by Surface-Mapping of Phylogenetic Information.
    Bioinformatics 19:163-164.
    """

    def __init__(
            self,
            pdb_id,
            email,
            job_id
                 ):

        r"""
        Object constructor.
        :param pdb_id: PDB ID of the protein
        :param email: User's email that receives notification when the job is done
        :param job_id: Job ID for the job
        """

        self._pdb_id = pdb_id
        self._email = email
        self._chain_id = self._get_chain_id()
        # self._q_seq = self._get_q_seq()
        self._job_id = job_id

    def _get_chain_id(self) -> str:

        r"""
        Gets user's input for chain id and checks if the chain id is present in the PDB file.
        :return: A valid chain id
        """

        current_path = os.getcwd()
        PDB_path = os.path.join(current_path, f"{self._pdb_id}.pdb")
        chain_id_list = []
        with open(PDB_path, "r") as file:
            line = file.readline()
            while not line.startswith("SEQRES"):
                line = file.readline()
            chain_id = line.split()[2]
            chain_id_list.append(chain_id)
            idx = 0
            while line.startswith("SEQRES"):
                if line.split()[2] != chain_id_list[idx]:
                    chain_id_list.append(line.split()[2])
                    idx += 1
                line = file.readline()
        chain_user = input(f"Please give your chain id from {chain_id_list}: ")
        while True:
            if chain_user in chain_id_list:
                break
            else:
                chain_user = input("Chain identifier invalid. Please try again: ")
        return chain_user

    # def _get_q_seq(self) -> str:
    #
    #     r"""
    #     Gets user's input for query sequence and checks if the query sequence is present in the MSA file.
    #     :return: A valid query sequence
    #     """
    #
    #     current_path = os.getcwd()
    #     MSA_path = os.path.join(current_path, f"{self._pdb_id}.a3m")
    #     q_seq_list = []
    #     with open(MSA_path, "r") as file:
    #         line = file.readline()
    #         while line[0] == "-" or line[0] == ">" or line[0].isalpha():
    #             q_seq_list.append(line.split()[0][1:])
    #             line = file.readline()
    #             line = file.readline()
    #     q_seq_user = input("Please select query sequence: ")
    #     while True:
    #         if q_seq_user in q_seq_list:
    #             break
    #         else:
    #             q_seq_user = input("Chain identifier invalid. Please try again: ")
    #     return q_seq_user

    def out_chain_id(self) -> str:

        r"""
        Access the chain id from the main program.
        :return: chain_id
        """

        return self._chain_id

    def run_job(self):

        r"""
        The program opens a Chrome window and runs the Consurf server and download result automatically.
        THIS MAY TAKE HOURS.
        :return: N/A
        """

        current_path = os.getcwd()

        driver = webdriver.Chrome(ChromeDriverManager().install())
        server_url = "https://consurf.tau.ac.il/?redirect=NO"

        # Access the Consurf server
        print("Starting Consurf server...")
        driver.get(server_url)

        # Wait for the page to load
        WebDriverWait(driver, 90).until(
             EC.element_to_be_clickable((By.XPATH, "//*[@id='maincontentcontainer']/div/form/div[2]/label"))
        )

        # Select Amino Acid
        DNA_AA = driver.find_element(By.XPATH, "//*[@id='maincontentcontainer']/div/form/div[2]/label")
        DNA_AA.click()

        # Wait for the page to load
        WebDriverWait(driver, 90).until(
             EC.url_changes(server_url)
        )

        # Choose to upload PDB
        PDB_yes_no = driver.find_element(By.XPATH, "//*[@id='yes_no_box']/div[1]/label")
        PDB_yes_no.click()

        # Wait for the page to load
        WebDriverWait(driver, 15).until(
             EC.element_to_be_clickable((By.XPATH, "//*[@id='pdb_file_field']"))
        )

        # Upload PDB file
        pdb_FILE = driver.find_element(By.XPATH, "//*[@id='pdb_file_field']")
        PDB_path = os.path.join(current_path, f"{self._pdb_id}.pdb")
        pdb_FILE.send_keys(PDB_path)
        print("Analyzing PDB...")

        # Wait for the page to load
        WebDriverWait(driver, 15).until(
             EC.element_to_be_clickable((By.XPATH, "//*[@id='case_pdb_yes']/input[4]"))
        )

        # Go to the next page
        next_page = driver.find_element(By.XPATH, "//*[@id='case_pdb_yes']/input[4]")
        PDB_url = driver.current_url
        next_page.click()

        # Wait for the page to load
        WebDriverWait(driver, 90).until(
             EC.url_changes(PDB_url)
        )
        WebDriverWait(driver, 15).until(
             EC.presence_of_element_located((By.XPATH, "//*[@id='form']/select"))
        )

        # Get a list of options from the chain identifiers
        chainID = driver.find_element(By.XPATH, "//*[@id='form']/select")
        chainID_drop = Select(chainID)

        # Choose a chain identifier
        chainID_drop.select_by_value(self._chain_id)

        # Wait for the page to load
        WebDriverWait(driver, 15).until(
             EC.presence_of_element_located((By.XPATH, "//*[@id='yes_no_box']/div[1]/label"))
        )

        # Choose to upload MSA
        MSA_yes_no = driver.find_element(By.XPATH, "/html/body/div[3]/div/form/div[3]/div[1]/div[1]/label/input")
        MSA_yes_no.click()

        # Wait for the page to load
        WebDriverWait(driver, 15).until(
             EC.presence_of_element_located((By.XPATH, "//*[@id='fileSelect']"))
        )

        # Upload MSA
        MSA_upload = driver.find_element(By.XPATH, "//*[@id='fileSelect']")
        MSA_path = os.path.join(current_path, f"{self._pdb_id}_MSA.fasta")
        MSA_upload.send_keys(MSA_path)
        print("Fetching query sequences...")

        # Wait for the page to load
        WebDriverWait(driver, 90).until(
             EC.presence_of_element_located((By.XPATH, "//*[@id='queryName']"))
        )

        # Choose query sequence name
        QS = driver.find_element(By.XPATH, "//*[@id='queryName']")
        QS_drop = Select(QS)
        QS_drop.select_by_visible_text("101")

        # Update selection
        update_selection = driver.find_element(By.XPATH, "/html/body/div[3]/div/form/div[3]/div[2]/div[1]/div[2]/a[2]")
        update_selection.click()

        # Wait for the page to load
        WebDriverWait(driver, 15).until(
             EC.presence_of_element_located((By.XPATH, "//*[@id='yes_no_box']/div[1]/label/input"))
        )

        # No Tree file to upload
        TREE_yes_no = driver.find_element(By.XPATH, "/html/body/div[3]/div/form/div[5]/div[1]/div[2]/label/input")
        TREE_yes_no.click()

        # Wait for the page to load
        WebDriverWait(driver, 15).until(
             EC.presence_of_element_located((By.XPATH, "//*[@id='qtitle']"))
        )

        # Provide a job name
        job_name = driver.find_element(By.ID, "qtitle")
        job_name.send_keys(self._job_id)

        # Provide a Email to receive update
        email = driver.find_element(By.XPATH, "/html/body/div[3]/div/form/div[6]/div[8]/input")
        email.send_keys(self._email)

        # Submit Job
        print("Submitting job...")
        submit_button = driver.find_element(By.XPATH, "/html/body/div[3]/div/form/div[6]/input")
        final_url = driver.current_url
        submit_button.click()

        # Wait for the page to load
        WebDriverWait(driver, 90).until(
             EC.url_changes(final_url)
        )

        print(driver.find_element(By.XPATH, "/html/body/div[3]/b").text)
        job_id = driver.find_element(By.XPATH, "/html/body/div[3]/b").text.split()[7][:-1]

        WebDriverWait(driver, 36000).until(
             EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/ul[9]/li/a"))
        )

        result = requests.get(f"https://consurf.tau.ac.il/results/{job_id}/consurf.grades", verify=False)
        with open(f"{self._pdb_id}_CONS.txt", "w") as out:
            out.write(result.text)

        driver.quit()
