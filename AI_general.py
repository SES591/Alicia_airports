import numpy as np
import matplotlib.pyplot as plt

L=np.genfromtxt('airports_top20',dtype=None)
N=np.genfromtxt('boolean_matrix.txt')
C=np.genfromtxt('adjacency_list_top20')

def AI(a1,k):
    a=np.where(L==a1)[0][0]
    #time series for each airport
    N1=N[a]
    M=np.zeros((2**k,2))
    for i in range(0,24-k):
        dec=str(int(N1[i]))
        for w in range(1,k):
            dec+=str(int(N1[i+w]))
        p4=N1[i+k]
        x1=int(dec,2)
        M[x1,p4]+=1
        #print x1, p4
    #y=M[0,0]    
    M2=M/(24.-k)
    
    #M2=np.zeros((2,2,2))
    ai=0
    for i in range(0,2**k):
        for j in range(0,2):
            #numerator of the logarithm
            x1=M2[i,j]
            if x1!=0:
                #denominator of the logarithm (1)
                x2=M2[i,0]+M2[i,1]         
                #denominator of the logarithm (2)
                x3=0
                for v in range(0,2**k):
                    x3+=M2[v,j]
                #total for this triplet
                x4=np.log2(x1/(x2*x3))
            else:
                x4=0
            #print i,j,x1, x2, x3, x4
            
            ai+= x4/(2*(2**k))
                
    #y=sum(sum(sum(M2)))*C[a][b]
    return ai


n1=int(raw_input('Number of plots (1-6):'))
colors=['r','b','k','m','g','y']
for g in range(0,n1):
    k=int(raw_input('History length (k):'))
    Y=[]
    for i in range(0,len(L)):
        a1=L[i]
        y=AI(a1,k)
        Y.append(y)

    Y=np.sort(Y)
    Y[:]=Y[::-1]
    X=np.arange(20)
    lab='k='+str(k)
    plt.plot(X,Y,'.',color=colors[g],label=lab)

plt.ylabel('AI')
plt.legend(loc='best',numpoints = 1)       
plt.show()






