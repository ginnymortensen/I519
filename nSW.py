#Genevieve Mortensen
#09/29/2022
#Quiz 3 Part B : Modify nNW.py script to give nSW.py script.

#First import necessary modules. argparse lets us pass arguments 
import argparse
import numpy as np

# Function that counts the number of SW Alignments
def count_SW_alignments(n,m) :
    # initial matrix full of zeros
    mat = np.zeros([n+1,m+1],dtype=int) 
    
    # fill first row and column with ones - we do this because our initial condition is 1 alignment, same as NW
    mat[0,:] = np.ones(m+1)
    mat[:,0] = np.ones(n+1)
   
    # dynamical programming loop to fill the rest of it
    # The loop will go to location i, j and fill it with the sum of the values in the boxes adjacent
    # These adjacent values are at i-1, j; i, j-1; and i-1, j-1. Adding in this way allows double gaps
    # to be included in the alignment counting.
    for i in range(1,n+1) :
        for j in range (1,m+1) :
            mat[i][j] += mat[i, j-1] #This line was changed to capture the vertically adjacent value
            mat[i][j] += mat[i-1, j] #Horizontally adjacent
            mat[i][j] += mat[i-1, j-1] #diagonally adjacent.

    # return the right bottom corner - change to allow m=n=20
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
    alignments_count = count_SW_alignments(m,n)
    print('For sequences of length {} and {} there are {} possible alignments calculated using the Smith-Waterman Algorithm.'.format(n,m,alignments_count))

# The NW algorithm produces fewer alignments than the SW algorithm because the SW allows double gaps in an alignment and the NW algorithm does not.
# Therefore there will be more SW alignments than NW alignments for two sequences of equal length. SW algorithm adds the values adjacent
# to the value being calculated in the matrix while the NW algorithm adds the range of values in the row and column diagonally adjacent to the 
# cell (i, j). By adding the values in all adjacent cells, we are including alignments resulting in a gap in our calcualtion from both
# the horizontal and vertical directions in our matrix (or in both sequence 1 and sequence 2). The SW algorithm also exceeds the computational
# power of the computer for sequences approaching 20 while NW algorithm does not. This is because there are more steps to our calculation
# in the SW algo than in the NW algo and it's time complexity is greater.