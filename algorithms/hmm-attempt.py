#Two-state Hidden Markov Model for I519
#Genevieve Mortensen 
#10/19/22

#Import required modules
import argparse
import random

#Input our arrays for initiation, transition, and probability
#Output our sequence  
def hmm(alpha, beta, init, trans, out):

    state = '' #empty state string
    obs = '' #empty obs string
    pr_lst = [] #empty list of transition and initiation probability multipliers
    out_pr_lst = [] #empty list of output probability multipliers

    #Initialize sequence by randomly selecting a state based on initialization probabilities
    state = ''.join(random.choices(alpha, weights = init, k = 1)) 

    #Create initial states and observations
    if state[0] == alpha[0]: #if the initial state is external
        obs = ''.join(random.choices(beta, weights = out[0], k = 1)) #create an observation based on the probability of the state being external
        pr_lst += [init[0]] #cat to probability list
        if obs[-1] == beta[0]: 
            out_pr_lst += [out[0][0]] #cat prob{o|e} if external and hydrophilic
        elif obs[-1] == beta[1]:
            out_pr_lst += [out[0][1]] #cat prob{o|e} if external and hydrophobic
    else: 
        obs = ''.join(random.choices(beta, out[1], k=1)) #create obs based on membrane bound initial state
        pr_lst += [init[1]]
        if obs[-1] == beta[0]:
            out_pr_lst += [out[1][0]] #cat prob{o|e} if membrane-bound and hydrophilic
        elif obs[-1] == beta[1]:
            out_pr_lst += [out[1][1]] #cat prob{o|e} if "" and hydrophobic

    #Generate the remaining sequence and also calculate state probability in tandem

    for i in range(1, 3):
        if state[i-1] == alpha[0]:  #if the previous state is external 
            state += ''.join(random.choices(alpha, weights = trans[0], k=1)) #select another state based on the transition probabilities from E to something else
            obs += ''.join(random.choices(beta, weights = out[0], k=1)) #select another observation based on the probability it is external and hydrophilic/phobic
            if state[i-1] == alpha[0]: #if the new state is external
                pr_lst += [trans[0][0]] #update prob list with transition prob between E and E
            else:
                pr_lst += [trans[0][1]] #otherwise update with trans prob between E and Membrane bound
            if obs[i-1] == beta[0]: #if the new obs is hydrophilic
                out_pr_lst += [out[0][0]] #cat prob{h|e}
            elif obs[i-1] == beta[1]: #if new obs is hydrophobic
                out_pr_lst += [out[0][1]] #cat prob{t|e}
        if state[i-1] == alpha[1]: #if the previous state in membrane-bound
            state += ''.join(random.choices(alpha, weights = trans[1], k=1))
            obs += ''.join(random.choices(beta, weights = out[1], k=1))
            if state[i-1] == alpha[0]: #if the new state is external
                pr_lst += [trans[1][0]] #trans prob b/t M and E 
            else:
                pr_lst += [trans[1][1]] #trans prob b/t M and M
            if obs[i-1] == beta[0]:
                out_pr_lst += [out[1][0]] #cat prob{h|m}
            elif obs[i-1] == beta[1]:
                out_pr_lst += [out[1][1]] #cat prob{t|m} 
    return state, obs, pr_lst, out_pr_lst

#By forward algorithm
def by_forward(obs, init, out, trans, pr_lst, out_pr_lst):
    
    out = [item for sublist in out for item in sublist]
    trans = [item for sublist in trans for item in sublist]

    #Initialize probability results using observations
    res_e = []
    res_m = []
    if out_pr_lst[0] == out[0] or out_pr_lst[0] == out[1]:
        res_e += [pr_lst[0]*out_pr_lst[0]]
        if out_pr_lst[0] == out[0]:
            res_m += [init[1]*out[2]]
        else:
            res_m += [init[1]*out[3]]
    elif out_pr_lst[0] == out[2] or out_pr_lst[0] == out[3]:
        res_m += [pr_lst[0]*out_pr_lst[0]]
        if out_pr_lst[0] == out[2]:
            res_e += [init[0]*out[0]]
        else:
            res_e += [init[0]*out[1]]

    obs = obs[1:]
    # Induction 
    for i in obs:
        if i == 'T':
            res_e += [(res_e[0]*trans[0]+res_m[0]*trans[2])*out[1]]; res_m += [(res_e[0]*trans[1]+res_m[0]*trans[3])*out[3]]
            res_e = res_e[1:]
            res_m = res_m[1:]
        else:
            res_e += [(res_e[0]*trans[0]+res_m[0]*trans[2])*out[0]]; res_m += [(res_e[0]*trans[1]+res_m[0]*trans[3])*out[2]]
            res_e = res_e[1:]
            res_m = res_m[1:]
    #Termination
    full_res = res_e[-1] + res_m[-1]
    return full_res, res_e[-1]

#Viterbi Algorithm
def viterbi(obs, init, out, trans, pr_lst, out_pr_lst, full_res):
    
    out = [item for sublist in out for item in sublist]
    trans = [item for sublist in trans for item in sublist]

    #Initialize probability results using observations
    res_e = []
    res_m = []
    if out_pr_lst[0] == out[0] or out_pr_lst[0] == out[1]:
        res_e += [pr_lst[0]*out_pr_lst[0]]
        if out_pr_lst[0] == out[0]:
            res_m += [init[1]*out[2]]
        else:
            res_m += [init[1]*out[3]]
    elif out_pr_lst[0] == out[2] or out_pr_lst[0] == out[3]:
        res_m += [pr_lst[0]*out_pr_lst[0]]
        if out_pr_lst[0] == out[2]:
            res_e += [init[0]*out[0]]
        else:
            res_e += [init[0]*out[1]]

    obs = obs[1:]
    # Induction 
    for i in obs:
        if i == 'T':
            res_e += [max((res_e[0]*trans[0]), (res_m[0]*trans[2]))*out[1]]
            res_m += [max((res_e[0]*trans[1]), (res_m[0]*trans[3]))*out[3]]
            res_e = res_e[1:]
            res_m = res_m[1:]
        else:
            res_e += [max((res_e[0]*trans[0]), (res_m[0]*trans[2]))*out[0]]
            res_m += [max((res_e[0]*trans[1]), (res_m[0]*trans[3]))*out[2]]
            res_e = res_e[1:]
            res_m = res_m[1:]
    #Termination
    vit_res = max(res_e[-1], res_m[-1])/full_res
    return vit_res

#Backwards algorithm
def by_backward(res_e_f, obs, init, out, trans, pr_lst, out_pr_lst, full_res):
    out = [item for sublist in out for item in sublist]
    trans = [item for sublist in trans for item in sublist]
    sbo = str(reversed(obs))

    #Initialize probability results using observations
    res_e = [1]
    res_m = [1]

    # Induction  
    for i in range(0, len(sbo)):
        if sbo[i] == 'T':
            res_e += [res_e[i]*trans[0]*out[0]+res_m[i]*trans[1]*out[2]]
            res_m += [res_e[i-1]*trans[2]*out[0]+res_m[i]*trans[3]*out[2]]
        else:
            res_e += [res_e[i]*trans[0]*out[1]+res_m[i]*trans[2]*out[3]]
            res_m += [res_e[i-1]*trans[1]*out[1]+res_m[i]*trans[3]*out[3]]

    #Termination
    back_res = res_e[0]*res_e_f
    back_res = back_res/full_res
    return back_res

#Viterbi Backtracking Algorithm
def backtrack(obs, init, out, trans, pr_lst, out_pr_lst, full_res):
    
    out = [item for sublist in out for item in sublist]
    trans = [item for sublist in trans for item in sublist]
    sbo = reversed(obs)

    #Initialize probability results using observations starting at end of list


    if out_pr_lst[-1] == out[0] or out_pr_lst[-1] == out[1]:
        res_e += [pr_lst[0]*out_pr_lst[-1]]
        if out_pr_lst[0] == out[0]:
            res_m += [init[1]*out[2]]
        else:
            res_m += [init[1]*out[3]]
    elif out_pr_lst[-1] == out[2] or out_pr_lst[-1] == out[3]:
        res_m += [pr_lst[0]*out_pr_lst[-1]]
        if out_pr_lst[0] == out[2]:
            res_e += [init[0]*out[0]]
        else:
            res_e += [init[0]*out[1]]    

    # Induction 
    for i in range(1, 3):
        if sbo[i-1] == 'T':
            res_e += [max((res_e[i-1]*trans[0]), (res_m[i-1]*trans[2]))*out[1]]
            res_m += [max((res_e[i-1]*trans[1]), (res_m[i-1]*trans[3]))*out[3]]
        else:
            res_e += [max((res_e[i-1]*trans[0]), (res_m[i-1]*trans[2]))*out[0]]
            res_m += [max((res_e[i-1]*trans[1]), (res_m[i-1]*trans[3]))*out[2]]
    print(res_e, res_m)

    #Termination
    predicted_seq = ''
    for i in range(len(state)):
        if res_e[i] > res_m[i]:
            predicted_seq += 'E'
        else: predicted_seq += 'M'
    return predicted_seq

if __name__ == '__main__' :
    
    #Arguments for each algorithm
    parser = argparse.ArgumentParser()
    #parser.add_argument('-n', type=int, default=3, help="sequence length")
    parser.add_argument('-alpha', type=list, default=['E', 'M'], help="list of states")
    parser.add_argument('-beta', type=list, default=['H', 'T'], help="list of observations")
    parser.add_argument('-init', type=list, default = [float(7/8), float(1/8)], help="list of initialization probabilities")
    parser.add_argument('-trans', type=list, default = [[float(3/5), float(2/5)], [float(4/7), float(3/7)]], help="list of transition probabilities")
    parser.add_argument('-out', type=list, default = [[float(3/4), float(1/4)], [float(1/3), float(2/3)]], help="list of outcome probabilities")
    args = parser.parse_args()

    #Testing
    state, obs, pr_lst, out_pr_lst = hmm(args.alpha, args.beta, args.init, args.trans, args.out)
    print(f'{state}\n{obs}')
    full_res, res_e_f = by_forward(obs, args.init, args.out, args.trans, pr_lst, out_pr_lst)
    print(full_res)
    print(viterbi(obs, args.init, args.out, args.trans, pr_lst, out_pr_lst, full_res))
    print(by_backward(res_e_f, obs, args.init, args.out, args.trans, pr_lst, out_pr_lst, full_res))
    print(backtrack(obs, args.init, args.out, args.trans, pr_lst, out_pr_lst, full_res))

# Our complete possibilities of our state sequences of length n. We have 8 states in a two state
# model. The probabilities are multiplicative to the transitions and the initiations.
# Now we can find the maximal probability of the unknown state sequence based on observation.
# We should be able to send someone else a sequence and then try to calculate what the state
# of the sequence is. We can't see these points but we can see the sequence. 
