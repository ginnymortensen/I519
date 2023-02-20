#Genevieve Mortensen
#09/29/2022
#Quiz 3 Part B

# Calculate the optimal score of Smith-Waterman alignments

#import modules
import argparse
import numpy as np
import pandas as pd

#This function calculates our score pertaining to gaps. 
# It gives us a 0 if there is no gap penalty multiplier, else it returns a gap multiplier.
# The gap multiplier is that we deduct alpha points for gap of size beta.
def gap_penalty(g,alpha,beta):
    # ... affine gap penalty for gap of length g:
    return 0 if g==0 else -alpha-beta*g

#This function calculates our points regarding mismatches and identities.
# This function returns the identity score ids if the sequence value a matches sequence value b.
# If it doesn't then it returns the mismatch score.
def sigma(a,b,ids,mms):
    # ... simple scoring for identities (ids) and mismatches (mms):
    return ids if a==b else mms


#Function to calculate the optimal SW global alignment score. Here we give sequences A and B, the identity score ids and mismatch score mms,
# and alpha score deduction for gap of size beta. 
def score_lSW(A,B,ids,mms,alpha,beta) :
    '''
    Sequence A is of length m (labeling rows)
    Sequence B is of length n (labeling columns)
    '''
    #give length of sequences A and B
    m = len(A)
    n = len(B)

    # Adding a blank space at the beginning of the string to account for corner in matrix:
    A = ' '+A
    B = ' '+B

    # Initializing the score matrix with zeroes:
    score_matrix = np.zeros([m+1,n+1],dtype=int)

    # Setting initial conditions: - for SW algorithm, we start with zeroes and do not allow negative numbers.

    #initialize a score of zero for assignment to our matrix location
    score = 0
    # Calculations:
    for i in range(1,m+1):
        for j in range(1,n+1):
            d = [score_matrix[i-1,j-1] + sigma(A[i],B[j],ids,mms)] #Calculate the diagonal alignment score
            h = [score_matrix[i-1,j-1-k] + sigma(A[i],B[j-k],ids,mms) + gap_penalty(k,alpha,beta) for k in range(1,j)] #The horizontally gapped alignment score
            v = [score_matrix[i-1-l,j-1] + sigma(A[i-l],B[j],ids,mms) + gap_penalty(l,alpha,beta) for l in range(1,i)] # The vertical alignment score
            # The calculation is the same as in our gNW.py program, but this time we only allow scores greater than zero to populate our matrix per SW scoring.
            #Loop which fills matrix with maximal score by adding all alignment scores and taking the maximum value if it is greater than zero, else fill w/ zero.
            score = max(d+v+h)
            if score > 0:
                score_matrix[i,j] = max(d+h+v)
            else:
                score_matrix[i,j] = 0

    #Prints a matrix of our scores.
    print("\nlSW score matrix (for debugging):\n")
    smdf = pd.DataFrame(score_matrix)
    smdf.set_axis(list(A),axis=0,inplace=True)
    smdf.set_axis(list(B),axis=1,inplace=True)
    print(smdf)
    print("")

    return score_matrix.max()


if __name__ == '__main__' :

    parser = argparse.ArgumentParser()
    parser.add_argument('-seq1', type=str, default = 'CGA', help="Sequence 1 (string)")
    parser.add_argument('-seq2', type=str, default = 'CCG', help="Sequence 2 (string)")
    parser.add_argument('-ids', type=int, default = 1, help="Identity score (positive INT)")
    parser.add_argument('-mms', type=int, default = -1, help="Mismatch score (non-positive INT)")
    parser.add_argument('-alpha', type=int, default = 1, help="alpha (non-negative INT)")
    parser.add_argument('-beta', type=int, default = 1, help="beta (non-negative INT)")
    args = parser.parse_args()
    os = score_lSW(args.seq1,args.seq2,args.ids,args.mms,args.alpha,args.beta)

    print("The optimal lSW alignment score of sequences:\n", args.seq1, "\n", args.seq2)
    print("for scoring scheme ids=",args.ids," mms=",args.mms," w(g)=",-args.alpha,"-",args.beta,"*g")
    print("is ",os)

# What is observed when testing the gSW.py script with the gNW.py script is that we see different scores given and a matrix
# which uses zeroes in place of any value less than zero, whereas the the NW score matrix shows negative values.
# This is because the SW score calculates the maximal diagonal, horizontal, and vertical alignment score with 0 as the lower bound.
# This means that calculations are made from zero. Between algorithms, we see that the bottom right cell is still the optimal score
# for both methods. The score returned by the SW scoring method is more efficient because we ignore all values less than optimal.
# With both methods, there are some optimal alignment scores which would match more than one alignment. We can clearly see why
# when our optimal score for SW algorithm is zero.