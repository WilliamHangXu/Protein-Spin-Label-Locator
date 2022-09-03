import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def run_topcons(pdb_id):

    driver = webdriver.Chrome(ChromeDriverManager().install())
    server_url = "https://topcons.cbr.su.se/pred/"
    driver.get(server_url)
    current_path = os.getcwd()

    seq_FILE = driver.find_element(By.XPATH, "/html/body/table[2]/tbody/tr/td[2]/table/tbody/tr/td/div/table[1]/tbody/tr/td/form/p[2]/input")
    seq_path = os.path.join(current_path, f"{pdb_id}_SEQ.fasta")
    seq_FILE.send_keys(seq_path)

    submit = driver.find_element(By.XPATH, "/html/body/table[2]/tbody/tr/td[2]/table/tbody/tr/td/div/table[1]/tbody/tr/td/form/p[5]/input[1]")
    submit.click()

    WebDriverWait(driver, 90).until(
         EC.url_changes(server_url)
    )

    WebDriverWait(driver, 90).until(
         EC.element_to_be_clickable((By.XPATH, "/html/body/table[2]/tbody/tr/td[2]/table/tbody/tr/td/div/table[1]/tbody/tr/td/p[2]/a"))
    )

    final_url = driver.current_url

    result = driver.find_element(By.XPATH, "/html/body/table[2]/tbody/tr/td[2]/table/tbody/tr/td/div/table[1]/tbody/tr/td/p[2]/a")
    result.click()

    WebDriverWait(driver, 90).until(
         EC.url_changes(final_url)
    )

    result_url = driver.current_url

    with open(pdb_id + "_MEM.txt", "w") as out:
        out.write(requests.get(result_url).text)

    print(f"{pdb_id}_MEM.txt has been successfully generated.")

    driver.quit()


