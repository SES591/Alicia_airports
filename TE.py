import numpy as np
import matplotlib.pyplot as plt

L=np.genfromtxt('airports_top20',dtype=None)
N=np.genfromtxt('boolean_matrix.txt')
C=np.genfromtxt('adjacency_list_top20')

def TE(a1,a2):
    a=np.where(L==a1)[0][0]
    b=np.where(L==a2)[0][0]
    #time series for each airport
    N1=N[a]
    N2=N[b]
    M=np.zeros((8,2,2))
    for i in range(0,21):
        p1=int(N1[i])
        p2=int(N1[i+1])
        p3=int(N1[i+2])
        y0=N2[i+2]
        p4=N1[i+3]
        dec=str(p1)+str(p2)+str(p3)
        x1=int(dec,2)
        M[x1,p4,y0]+=1
        #print i, dec, x1, p4, y0
    y=M[0,0,0]    
    M2=M/21.0
    #print M
    te=0
    for i in range(0,8):
        for j in range(0,2):
            for k in range(0,2):
                #first element
                x1=M2[i,j,k]
                if x1!=0:
                    #numerator of the logarithm
                    x2=M[i,j,k]/(M[i,0,k]+M[i,1,k])
                    
                    #denominator of the logarithm
                    r=0
                    for v in range(0,8):
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



TE_matrix=np.zeros((len(L),len(L)))
Y=[]
for i in range(0,len(L)):
    for j in range(0,len(L)):
        if i!=j:
            a1=L[i]
            a2=L[j]
            t=TE(a1,a2)
            TE_matrix[i,j]=t
            #print a1, a2, t
            Y.append(t)

X=np.arange(380)
Y=np.sort(Y)
Y[:]=Y[::-1]
plt.plot(X,Y,'.',color='r')        
#print TE_matrix   
plt.xlabel('rank')
plt.ylabel('TE(bits)')   
plt.show()


