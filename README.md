# Protein Spin Label Locator
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
  1. Found on secondary structure 
  2. Not affiliated to membrane The program `topcons_runner.py` checks this using 
  3. Not conserved
From the residues that satisfy the above three criteria, we select pairs where the distance between two residues are in an appropriate range.

When `main.py` is run, the user is asked for the PDB ID of a protein, and these criteria are checked by the `DSSPRunner` class defined in `dssp_runner.py`, the `TopconsRunner` class defined in `topcons_runner.py`, and the `ConsurfRunner` class defined in `consurf_runner.py`, respectively, and the results are stored in a `Protein` object constructed based on the protein the user provided. 
After getting a set of qualified residues, the distances between each pair of residue are calculated, and the qualified pairs are displayed.
## Acknowledgement
Thank the Mchaourab Lab of Vanderbilt University, especially Julia, Richard and Hassane for their generous instructions on Bioinformatics. Thank former lab member Diego for his effort on the `MMseqs2Runner` class. <br />
Thank brianshan974 for his thoughtful advice on programming.<br />
Thanks to the scholars who have been contributing to the Computational Biology world.
## Reference
Please read the headers of the programs to see details.<br />

    Ashkenazy H., Abadi S., Martz E., Chay O., Mayrose I., Pupko T., and Ben-Tal N. 2016<br />
    ConSurf 2016: an improved methodology to estimate and visualize evolutionary conservation in macromolecules<br />
    Nucl. Acids Res. 2016; DOI: 10.1093/nar/gkw408; PMID: 27166375<br />

    Celniker G., Nimrod G., Ashkenazy H., Glaser F., Martz E., Mayrose I., Pupko T., and Ben-Tal N. 2013.<br />
    ConSurf: Using Evolutionary Data to Raise Testable Hypotheses about Protein Function<br />
    Isr. J. Chem. 2013 March 10, doi: 10.1002/ijch.201200096<br />

    Ashkenazy H., Erez E., Martz E., Pupko T. and Ben-Tal N. 2010<br />
    ConSurf 2010: calculating evolutionary conservation in sequence and structure of proteins and nucleic acids.<br />
    Nucl. Acids Res. 2010; DOI: 10.1093/nar/gkq399; PMID: 20478830<br />

    Landau M., Mayrose I., Rosenberg Y., Glaser F., Martz E., Pupko T. and Ben-Tal N. 2005.<br />
    ConSurf 2005: the projection of evolutionary conservation scores of residues on protein structures.<br />
    Nucl. Acids Res. 33:W299-W302.<br />

    Glaser F., Pupko T., Paz I., Bell R.E., Bechor D., Martz E. and Ben-Tal N. 2003.<br />
    ConSurf: Identification of Functional Regions in Proteins by Surface-Mapping of Phylogenetic Information.<br />
    Bioinformatics 19:163-164.<br />
    
    A series of PDB related databases for everyday needs.<br />
    Wouter G Touw, Coos Baakman, Jon Black, Tim AH te Beek, E Krieger, Robbie P Joosten, Gert Vriend.<br />
    Nucleic Acids Research 2015 January; 43(Database issue): D364-D368.<br />

    Dictionary of protein secondary structure: pattern recognition of hydrogen-bonded and geometrical features.<br />
    Kabsch W, Sander C, Biopolymers. 1983 22 2577-2637.<br />
    PMID: 6667333; UI: 84128824.<br />
    
    Clustering huge protein sequence sets in linear time<br />
    https://doi.org/10.1038/s41467-018-04964-5<br />
    
    MMseqs2 enables sensitive protein sequence searching for the analysis<br />
    of massive data sets"<br />
    https://doi.org/10.1038/nbt.3988<br />
    
    Madeira F, Pearce M, Tivey ARN, et al.<br />
    Search and sequence analysis tools services from EMBL-EBI in 2022.<br />

    Nucleic Acids Research. 2022 Apr:gkac240.<br />
    DOI: 10.1093/nar/gkac240. PMID: 35412617; PMCID: PMC9252731.<br />
    
    The TOPCONS web server for combined membrane protein topology and signal peptide prediction.<br />
    Tsirigos KD*, Peters C*, Shu N*, Käll L and Elofsson A (2015) Nucleic Acids Research 43 (Webserver issue), W401-W407.<br />
