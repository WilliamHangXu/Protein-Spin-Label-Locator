# Protein Spin Label Locator
NOTE: This project is still under construction.
## Description
### Purpose
We attach spin labels onto specific pairs of residues in a protein to study its conformational change. This set of programs takes a PDB ID of a protein as an input and returns a text file that contains all possible pairs of amino acid residues onto which spin labels can be attached. TL;DR: download all source codes and run `main.py`.
### Dependencies
Selenium (Make sure Google Chrome is properly installed)<br />
Requests<br />
Biopython<br />
Numpy
### How it works
In a protein, amino acid residues onto which a spin label can be attached have the following characteristics:
  1. Found on secondary structure<br />
  2. Not affiliated to membrane<br />
  3. Not conserved<br />

From the residues that satisfy the above three criteria, we select pairs where the distance between two residues are in an appropriate range.

When `main.py` is run, the user is asked for the PDB ID of a protein, and these criteria are checked by the `DSSPRunner` class defined in `dssp_runner.py`, the `TopconsRunner` class defined in `topcons_runner.py`, and the `ConsurfRunner` class defined in `consurf_runner.py`, respectively, and the results are stored in a `Protein` object constructed based on the protein the user provided. 
After getting a set of qualified residues, the distances between each pair of residue are calculated, and the qualified pairs are displayed.
## Acknowledgement
Thank the Mchaourab Lab of Vanderbilt University, especially Julia, Richard, Kevin and Hassane for their generous instructions on Bioinformatics. Thank former lab member Diego for his effort on the `MMseqs2Runner` class. <br />
Thank brianshan974 for his thoughtful advice on programming.<br />
Thanks to the scholars who have been contributing to the Computational Biology world.
## Reference
Please read the headers of the programs to see details.<br />

    Ashkenazy H., Abadi S., Martz E., Chay O., Mayrose I., Pupko T., and Ben-Tal N. 2016
    ConSurf 2016: an improved methodology to estimate and visualize evolutionary conservation in macromolecule
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
    
    A series of PDB related databases for everyday needs.
    Wouter G Touw, Coos Baakman, Jon Black, Tim AH te Beek, E Krieger, Robbie P Joosten, Gert Vriend.
    Nucleic Acids Research 2015 January; 43(Database issue): D364-D368.
    
    Dictionary of protein secondary structure: pattern recognition of hydrogen-bonded and geometrical features.
    Kabsch W, Sander C, Biopolymers. 1983 22 2577-2637.
    PMID: 6667333; UI: 84128824.
    
    Clustering huge protein sequence sets in linear time
    https://doi.org/10.1038/s41467-018-04964-5
    
    MMseqs2 enables sensitive protein sequence searching for the analysis
    of massive data sets"
    https://doi.org/10.1038/nbt.3988
    
    Madeira F, Pearce M, Tivey ARN, et al.
    Search and sequence analysis tools services from EMBL-EBI in 2022.

    Nucleic Acids Research. 2022 Apr:gkac240.
    DOI: 10.1093/nar/gkac240. PMID: 35412617; PMCID: PMC9252731.
    
    The TOPCONS web server for combined membrane protein topology and signal peptide prediction.
    Tsirigos KD*, Peters C*, Shu N*, Käll L and Elofsson A (2015) Nucleic Acids Research 43 (Webserver issue), W401-W407.
