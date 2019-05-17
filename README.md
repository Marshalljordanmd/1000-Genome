# 1000-Genome
python scripts to analyze VCF data from NCBI 1000 Genome Browser

i have written several python scripts which i am using to extract Allele Frequencies (AFs) from data downloaded from
the NCBI 1000 Genome Browser. Bascically, the scripts ask input from the keyboard for file name, and start and stop 
positions on the genome. Then the file is converted to a Pandas DataFrame. Then a loop is setup to iterate over all of the 
rows, each of which is a variant position in the database compared to the reference genome. For each row, the information line, column 7, is chosen because it contains the AFs of interest. This slice of information is converted to a dictionary  
