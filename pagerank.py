'''
Created on Oct 7, 2014

@author: Swapna Bhi
'''
from math import log
import operator


M = {}                  # M(p) is the set (without duplicates) of pages that link to page p
L = {}                  # L(q) is the number of out-links (without duplicates) from page q
P = set()               # P is the set of all pages; |P| = N
S = []                  # S is the list of sink nodes, i.e., pages that have no out links
W = {}                  # W(p) is number of inlinks from page p
PR = {}                 # PR is set of pageranks of pages in P 
d = 0.85                # d is the PageRank damping/teleportation factor
newPR = {}              # newPR is set to store temporary pagerank of pages in P 
perplexity = []         # Stores perplexities for all iterations    
# Initialization Block
num_iterations =0       # number of iteratios to perform 
converg_option = '0'    # option for convergence; can be 1 or 2, any othe value is invalid
   
#===============================================================================
# Check of convergence option and performe operation to check convergence
# option 1 for halting program after certain iterations 
# option 2 for halting program after perplexity value converges  
# any other option is invalid
#===============================================================================
def check_converge(iteration):
    if converg_option =='1':
        return not_conv_iteration(iteration)
    elif converg_option =='2':
        return not_conv_perplex(iteration)
    else:
        print('please enter the right option! ')
        return False
        
#===============================================================================
# function to halt program if current iteration is i'th iteration
# returns False if halting condition is satisfied
# returns True otherwise
#===============================================================================
def not_conv_iteration(i):
    if str(i) == num_iterations:
        return False
    else:
        return True

#===============================================================================
# function to halt program if perplexity is converged
# returns False if halting condition is satisfied
# returns True otherwise
#===============================================================================
def not_conv_perplex(i):
    per = calculate_perplex(i)
    
    perplexity.append(per)
    if (len(perplexity) >  4):
        if ((int(perplexity[i]))==(int(perplexity[i-1]))==(int(perplexity[i-2]))==(int(perplexity[i-3]))): 
            return False
        else:
            return True
    else:
        return True
    
#===============================================================================
# function to calculate perplexity
# returns perplexity value
#===============================================================================    
def calculate_perplex(i):
    entropy = 0
    for p in L.keys():
        entropy += PR[p] * log(1/PR[p],2) 
    return 2**entropy
    
#===============================================================================
# function to sort pagerank values and write sorted value in a file
#===============================================================================  
def sortPR():
    sorted_list = sorted([(PR, pages) for (pages, PR) in PR.items()], reverse=True)
    if len(P) > 50:
        num_pages = 50
    else:
        num_pages = len(P)
    for item in sorted_list:
            f2.write(str(item)+'\n')
    print("First ", num_pages," pages are:")
    for n in range(num_pages):
        print(sorted_list[n][1], " : ", sorted_list[n][0], "  :: ",len(M[sorted_list[n][1]]) )
        
#===============================================================================
# function to sort inlinks for pages in P and write sorted value in a file
#===============================================================================  
def sortInlinks():
    for p in P:
        W[p] = len(M[p])
    sorted_lnl = sorted([(W, pages) for (pages, W) in W.items()], reverse=True)
    for item in sorted_lnl:
            f3.write(str(item)+'\n')
    
# accept inlinks file from user
inlink_file = input('Enter filename of the file to process :: ')
# accept halting condition from user

#converg_option = input('Enter 1 to stop the algorithm after a certain iterations \nEnter 2 to stop the algorithm after pagerank converges \n ')
#if converg_option == '1':
    # accept number of iterations from user
#    num_iterations = input('Enter Number of iterations :: ')

f=open(inlink_file,'r')

f2 = open('sortedPR.txt','w')
f3 = open('sortedInlinks.txt','w')
# read inlinks file and use it to create all sets
content = f.readlines()
inlinks=set()
for c in content:
    l=c.split()
    # if source already in M, append the old values with new values in file
    if l[0] in M:
        for x in M[l[0]]:
            inlinks.add(x)
        for links in l[1:]:
            inlinks.add(links)
        del(M[l[0]])
        M[l[0]] = inlinks
        inlinks = ()
    # Add all inlinks of p to M[p]    
    else:
        M[l[0]] = set()
        for links in l[1:]:
            M[l[0]].add(links)
    # add p in P
    P.add(l[0])

# initialize outlinks of all pages in P to 0 
for p in P:
    L[p]=0

# calculate number of outlinks of pages in P
for val in M.values():
    for x1 in val:
        if x1 in L:
            L[x1] +=1               

# N is numebr of pages in graph
N = float(len(P))

# populate sink page set
for p in L.keys():
    if L[p] == 0:
        S.append(p)

# initialize 
for p in P:
    PR[p] = 1.0/N
# initialize iteration number to 0
iteration = 0
# actual pagerank calulation
while not_conv_perplex(iteration):
    print(iteration, calculate_perplex(iteration))
    sinkPR = 0
    # calculate pagerank of sink pages
    for p in S:
        sinkPR += PR[p]
    # calculate pagerank for all the pages in P
    for p in P:
        newPR[p] = (1 - d) / N
        newPR[p] += (d * sinkPR) / N
        for q in M[p]:
            # avoiding key error
            if q in P:
                newPR[p]+= (d*PR[q]) / L[q]
    # update PR with newly calculated PR
    for p in P:
        PR[p] = newPR[p]
    iteration+=1
    
# if checking for perplexity convergence: print first 50 pages, sort pageranks and write in a file 
#----------------------------------------------------- if converg_option == '2':
    #------------------------------------------------------------------ sortPR()
#------------------------------- # sort pageranks and write everything in a file
#------------------------------------------------------------------------- else:
    #------------------------- x = sorted(PR.items(),key=operator.itemgetter(0))
    #-------------------------------------------------------------- for x1 in x:
            #-------------------------------------------- f2.write(str(x1)+'\n')
        
# sort inlinks and write in a file  
sortPR()          
sortInlinks()
            
f.close()
f2.close()
f3.close()