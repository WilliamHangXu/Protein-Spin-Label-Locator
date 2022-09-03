# Protein Spin Label
## Description
### Purpose
This set of programs takes a PDB ID of a protein as an input and returns a text file that contains all possible pairs of amino acid residues onto which spin labels can be attached. TL; DR: download all source codes and run `main.py`.
### How it works
We attach spin labels onto specific pairs of residues in a protein to study its conformational change.
In a protein, amino acid residues onto which a spin label can be attached have the following characteristics:
  1. Found on secondary structure 
  2. Not affiliated to membrane The program `topcons_runner.py` checks this using 
  3. Not conserved
From the residues that satisfy the above three criteria, we select pairs where the distance between two residues are in an appropriate range.

When `main.py` is run, the user is asked for the PDB ID of a protein, and these criteria are checked by the `DSSPRunner` class defined in `dssp_runner.py`, the `TopconsRunner` class defined in `topcons_runner.py`, and the `ConsurfRunner` class defined in `consurf_runner.py`, respectively, and the results are stored in a `Protein` object constructed based on the protein the user provided. 
After getting a set of qualified residues, the distances between each pair of residue are calculated, and the qualified pairs are displayed.
## Acknowledgement
Thank the Mchaourab Lab of Vanderbilt University, especially Julia, Richard and Hassane for their generous instructions on Bioinformatics.
Thank brianshan974 for his thoughtful advice on programming.
