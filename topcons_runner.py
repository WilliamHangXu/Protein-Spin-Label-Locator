import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def run_topcons(pdb_id, chainID):

    r"""
    Runs the topcons server to determine membrane affiliation of residues
    :param pdb_id: PDB ID of the protein
    :return: N/A

    Reference:
    The TOPCONS web server for combined membrane protein topology and signal peptide prediction.
    Tsirigos KD*, Peters C*, Shu N*, Käll L and Elofsson A (2015) Nucleic Acids Research 43 (Webserver issue), W401-W407.
    """

    # Data preparation. Extract sequence from the MSA fasta file
    # with open(f"{pdb_id}_MSA.fasta", "r") as infile:
    #     with open(f"{pdb_id}_SEQ.fasta", "w") as outfile:
    #         for i in range(2):
    #             line = infile.readline()
    #             outfile.write(line)
    # with open(f"{pdb_id}_SEQ.fasta", "w") as outfile:



    # Starts a webdriver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    server_url = "https://topcons.cbr.su.se/pred/"
    driver.get(server_url)
    current_path = os.getcwd()

    # Provide the sequence
    seq_FILE = driver.find_element(By.XPATH, "/html/body/table[2]/tbody/tr/td[2]/table/tbody/tr/td/div/table[1]/tbody/tr/td/form/p[2]/input")
    seq_path = os.path.join(current_path, f"{pdb_id}_{chainID}_SEQ.fasta")
    seq_FILE.send_keys(seq_path)

    # Submit job
    submit = driver.find_element(By.XPATH, "/html/body/table[2]/tbody/tr/td[2]/table/tbody/tr/td/div/table[1]/tbody/tr/td/form/p[5]/input[1]")
    submit.click()

    # Wait until the job is finished
    WebDriverWait(driver, 90).until(
         EC.url_changes(server_url)
    )

    WebDriverWait(driver, 90).until(
         EC.element_to_be_clickable((By.XPATH, "/html/body/table[2]/tbody/tr/td[2]/table/tbody/tr/td/div/table[1]/tbody/tr/td/p[2]/a"))
    )

    final_url = driver.current_url

    # Get result
    result = driver.find_element(By.XPATH, "/html/body/table[2]/tbody/tr/td[2]/table/tbody/tr/td/div/table[1]/tbody/tr/td/p[2]/a")
    result.click()

    # Wait for the result to load
    WebDriverWait(driver, 90).until(
         EC.url_changes(final_url)
    )

    result_url = driver.current_url

    # Fetch result
    with open(f"{pdb_id}_{chainID}_MEM.txt", "w") as out:
        out.write(requests.get(result_url).text)

    print(f"{pdb_id}_{chainID}_MEM.txt has been successfully generated.")

    driver.quit()


