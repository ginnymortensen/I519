import argparse
import numpy as np


# Function that counts the number of NW Alignments
def count_NW_alignments(n,m) :
    # initial matrix full of zeros
    mat = np.zeros([n+1,m+1],dtype=int) 
    
    # fill first row and column with ones
    mat[0,:] = np.ones(m+1)
    mat[:,0] = np.ones(n+1)
   
    # dynamical programming loop to fill the rest of it
    for i in range(1,n+1) :
        for j in range (1,m+1) : 
            mat[i][j] += sum(mat[i-1,0:j])
            mat[i][j] += sum(mat[0:i-1,j-1])

    # return the right bottom corner
    if m <= 20 and n <= 20:
        print("\n")
        print(mat)
        print("\n")
    return mat[-1][-1]

if __name__ == '__main__' :

    parser = argparse.ArgumentParser()
    parser.add_argument('-length1', type=int, default = '5', help="length 1 (positive INT)")
    parser.add_argument('-length2', type=int, default = '5', help="length 12(positive INT)")
    args = parser.parse_args()

    m = args.length1 # Length of first sequence
    n = args.length2 # Length of second sequence
    alignments_count = count_NW_alignments(m,n)
    print('For sequences of length {} and {} there are {} possible alignments calculated using the Needleman-Wunsch Algorithm.'.format(n,m,alignments_count))
