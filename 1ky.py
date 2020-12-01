#!/usr/bin/python

import re, os, sys, getopt
import scipy
from scipy import stats

# intput is 2 variant sequences
def compare_sequences(seq1, seq2):
    # set counter to 0 (counter counts number of equal letters)
    c = 0
    for i in range(len(seq1)):
        # seq1[i] refers to a single letter, and if they are equal, it is set to True, but must be set to an int value
        c += int(seq1[i]==seq2[i])
        # divide by float to make it a float!
        # % similarity = no. equal bases / length of seq
    return c/float(len(seq1))

def main(argv):
    # declare and initialize variables here
    inputfile = ''
    matrixfile = ''

    # h is for help, i is the input file, m is the putput matrix file
    try:
        opts, args = getopt.getopt(argv,"hi:m:",["ifile=","mfile="])
    except getopt.GetoptError:
        # if script is run erroneously, you get an error message
        print '1ky.py -i <input file> -m <matrix file>'
        sys.exit(2)
    for opt, arg in opts:
        # if only -h is set, then display this helpful how-to-run message
        if opt == '-h':
            print '1ky.py -i <input file 1> -m <matrix file>'
            sys.exit()
        # the arg matrix collects the input parameters
        # inputfile is your input variant pseudo-fasta file
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        # -m is the output sequence similarity file
        elif opt in ("-m", "--mfile"):
            matrixfile = arg

    id = '' # this is the actual sequence id for a given sequence
    ids = list() # a list to contain sequence ids
    sequences = dict() # a dictionary to contain variant sequences, its key is the sequence id

    # open both the variant seuence file and the output matrix file
    fi = open(inputfile, 'r')
    fm = open(matrixfile,'w')

    # run through thesequence file line by line
    for line in fi:
    # get rid of the trailing carriage return
        lin = line.rstrip('\n')
        # pass it back into line
        line = str(lin)
        # if you encounter a sequence id
        x = re.search(">",line)
        if x :
            # set id to the header
            id = line[1:]
            # and append it to the ids list
            ids.append(id)
            # initialize an empty dictionary entry with id as the sequence id
            sequences[id] = ''
        else:
            # if the line is not a header, then just add the sequence row
            # also, avoid empty lines
            if len(line) > 0:
                sequences[id] = sequences[id] + line

    fi.close()
    
    # sort ids in alphabetical order
    ids = sorted(ids)
    
    # write header line
    fm.write('ID') # first row, first col is an 'ID'
    for i in ids:
    # write out sequence ids separated by a tab
        fm.write('\t'+i)
    # add a carriage return at the end
    fm.write('\n')
    
    # write each line
    for i in ids:
        # write the sequence id
        fm.write(i)
        # compare each seuence with every other sequence
        for j in ids:
            # calculate the sequence similarity, i.e. ACGT and ACGA get 0.75
            p = compare_sequences(sequences[i], sequences[j])
            # write % sim. value with a tab in between values
            fm.write('\t'+str(p))
        # at the end of each line write a carriage return
        fm.write('\n')
    
    fm.close()

if __name__ == "__main__":
    main(sys.argv[1:])