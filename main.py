import os
from pdb_downloader import PDBDownloader
from primary_sequence import get_seq
from protein_seq import Protein
from seqret_runner import SeqretRunner
from mmseqs_runner import MMSeqs2Runner
from dssp_runner import DSSPRunner
from datetime import datetime
from topcons_runner import run_topcons
from consurf_runner import ConsurfRunner


email = "willxh.68209@gmail.com"
now = datetime.now()
dt = now.strftime("%m_%d_%Y_%H_%M_%S")


# Ask the user for a PDB ID and then download the PDB file.
pdbD = PDBDownloader()
pdb_id = pdbD.get_user_input()
job_id = f"{dt}_{pdb_id}"
download_path = os.path.join(os.getcwd(), f"{job_id}")
os.mkdir(download_path)
os.chdir(download_path)
PDB_path = pdbD.download_pdb()

# Extract primary sequence from the PDB file
seq = get_seq(PDB_path)

# create AA sequence
protein = Protein(pdb_id=pdb_id, seq=seq)

print("Starting to convert the sequence into FASTA format...")

# get a fasta file of the sequence
getF = SeqretRunner(email=email, job_id=job_id, mode="fasta", seq=seq, out_name=f"{pdb_id}_SEQ")
fasta_path = getF.run_job()

print("Starting to fetch MSA...")
# get MSA file in a3m format and convert it into clustal format
getMSA = MMSeqs2Runner(job=job_id, seq=seq)
getMSA.run_job(pdb_id)
print("MSA fetched. Starting to convert MSA into CLUSTAL format...")
with open(f"{pdb_id}.a3m", "r") as a3m:
    MSA_str = a3m.read()
MSA_conv = SeqretRunner(email=email, job_id=job_id, mode="clustal", seq=MSA_str, out_name=f"{pdb_id}_MSA")
MSA_path = MSA_conv.run_job()

print("Predicting secondary structures...")
# Run DSSP
getSecStruct = DSSPRunner(file_name=pdb_id)
getSecStruct.run_job()

print("Predicting membrane exposure...")
# Run Topcons
run_topcons(pdb_id)

print("Calculating conservation score...")
# Run Consurf
getCons = ConsurfRunner(pdb_id=pdb_id, email=email, job_id=job_id)
chain_id = getCons.out_chain_id()
getCons.run_job()

print("Calculating distances between qualified residues...")
# # Calculate distance
# runDistance(file_path, protein)
#
# output_result(protein)
