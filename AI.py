import numpy as np
import matplotlib.pyplot as plt

L=np.genfromtxt('airports_top20',dtype=None)
N=np.genfromtxt('boolean_matrix.txt')
C=np.genfromtxt('adjacency_list_top20')

def AI(a1):
    a=np.where(L==a1)[0][0]
    #time series for each airport
    N1=N[a]
    M=np.zeros((8,2))
    for i in range(0,21):
        p1=int(N1[i])
        p2=int(N1[i+1])
        p3=int(N1[i+2])
        p4=N1[i+3]
        dec=str(p1)+str(p2)+str(p3)
        x1=int(dec,2)
        M[x1,p4]+=1
        #print x1, p4
    #y=M[0,0]    
    M2=M/21.0
    
    #M2=np.zeros((2,2,2))
    ai=0
    for i in range(0,8):
        for j in range(0,2):
            #numerator of the logarithm
            x1=M2[i,j]
            if x1!=0:
                #denominator of the logarithm (1)
                x2=M2[i,0]+M2[i,1]         
                #denominator of the logarithm (2)
                x3=0
                for v in range(0,8):
                    x3+=M2[v,j]
                #total for this triplet
                x4=np.log2(x1/(x2*x3))
            else:
                x4=0
            #print i,j,x1, x2, x3, x4
            
            ai+= x4/16.0
                
    #y=sum(sum(sum(M2)))*C[a][b]
    return ai

Y=[]
for i in range(0,len(N)):
    a1=L[i]
    y=AI(a1)
    print a1, y
    Y.append(y)


Y=np.sort(Y)
Y[:]=Y[::-1]
X=np.arange(20)

plt.plot(X,Y,'.',color='b')
plt.show()






