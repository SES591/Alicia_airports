import numpy as np
import matplotlib.pyplot as plt

L=np.genfromtxt('airports_top20',dtype=None)
N=np.genfromtxt('boolean_matrix.txt')
C=np.genfromtxt('adjacency_list_top20')

def TE(a1,a2,k):
    a=np.where(L==a1)[0][0]
    b=np.where(L==a2)[0][0]
    #time series for each airport
    N1=N[a]
    N2=N[b]
    M=np.zeros((2**k,2,2))
    for i in range(0,24-k):
        dec=str(int(N1[i]))
        for w in range(1,k):
            dec+=str(int(N1[i+w]))
        y0=N2[i+k-1]
        p4=N1[i+k]
        x1=int(dec,2)
        M[x1,p4,y0]+=1
        #print i, dec, x1, p4, y0
    M2=M/(24.-k)
    #print M
    te=0
    for i in range(0,2**k):
        for j in range(0,2):
            for k2 in range(0,2):
                #first element
                x1=M2[i,j,k2]
                if x1!=0:
                    #numerator of the logarithm
                    x2=M[i,j,k2]/(M[i,0,k2]+M[i,1,k2])
                    
                    #denominator of the logarithm
                    r=0
                    for v in range(0,2**k):
                        r+=M[v,j,0]+M[v,j,1]
                    x3=(M[i,j,0]+M[i,j,1])/r
                                        
                    #total for this triplet
                    x4=x1*np.log2(x2/x3)
                    #print i,j, k, x1, x2, x3, x4, r
                else:
                    x4=0
                te+= x4
                
    #y=sum(sum(sum(M2)))*C[a][b]
    return te


n1=int(raw_input('Number of plots (1-6):'))
colors=['r','b','k','m','g','y']
for g in range(0,n1):
    k=int(raw_input('History length (k):'))
    TE_matrix=np.zeros((len(L),len(L)))
    Y=[]
    for i in range(0,len(L)):
        for j in range(0, len(L)):
            if i!=j:
                a1=L[i]
                a2=L[j]
                t=TE(a1,a2,k)
                #print a1, a2, t
                TE_matrix[i,j]=t
                Y.append(t)

    X=np.arange(380)
    Y=np.sort(Y)
    Y[:]=Y[::-1]
    lab='k='+str(k)
    
    plt.plot(X,Y,'.',color=colors[g],label=lab)        

#print TE_matrix   
plt.xlabel('rank')
plt.ylabel('TE(bits)')
plt.legend(loc='best',numpoints = 1)   
plt.show()


