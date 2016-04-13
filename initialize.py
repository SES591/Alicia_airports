import numpy as np
from flights import *

def time_minutes(t):
    h=t/100
    m=t-100*h
    y=60*h+m
    return y
    
################################################################################
    
def start_system(all_flights):
    import parameters
    import random
    parameters.N=np.genfromtxt('airports_top20',dtype=None)
    parameters.connectivity_fraction=np.genfromtxt('fraction_connecting_passengers')
    N_flights_total=parameters.N_flights_total
    N_flights_remaining=parameters.N_flights_remaining
    delayed=0
    for i in range(0,len(parameters.N)):
        n=parameters.N[i]
        A=np.genfromtxt('top20_airports_tail_queue_%s' % (n),dtype=None)
        a=len(A)
        for j in range(0,a):
            A[j][4] = time_minutes(A[j][4])
            A[j][5] = time_minutes(A[j][5])
        B=np.genfromtxt('top20_airports_arrival_queue_%s' % (n),dtype=None)
        for j in range(0,len(B)):
            B[j][4] = time_minutes(B[j][4])
            B[j][5] = time_minutes(B[j][5])
        parameters.tail_queues.append(A)
        parameters.arrival_queues.append(B)
        
        N_flights_total+=a
        N_flights_remaining+=a
     
    M=np.genfromtxt('0528_filtered.csv', dtype=None)
    m=len(M)
     
    #the first element needs to be considered separately (just an indexing issue)
    l=0
    #check how many flights the same aircraft has to do that day
    for p in range(0,len(parameters.N)):
        if M[i][1]==M[p][1]:
            l+=1
    r=random.random()
    #first flight is always delayed
    in_delay=random.randint(30,60) 
    all_flights[0] = Flight(0, M[0][6], M[0][1], M[0][2], M[0][3], time_minutes(M[0][4]), time_minutes(M[0][5]),l,in_delay)
    
    all_flights[0].queue_first=True
    all_flights[0].flight_status='S'
    all_flights[0].service_time=30 
    #create rest of elements in dictionary
    b=0
    for i in range(1,m):
        l=0
        #check how many flights the same aircraft has to do that day
        for p in range(0,m):
            if M[i][1]==M[p][1] and M[i][4]>=M[p][4]:
                l+=1
        #r=random.random()
        #if r<=0.5:
            #in_delay=random.randint(10,60)
            #in_delay=random.randint(30,120)
            #delayed+=1
        if l==1:
            in_delay=random.randint(0,60)
            delayed+=1
        else:
            in_delay=0          
        all_flights[i] = Flight(i, M[i][6], M[i][1], M[i][2], M[i][3], time_minutes(M[i][4]), time_minutes(M[i][5]), l,in_delay)
        if l==1:
            all_flights[i].service_time=30
        if M[i][2]!=M[i-1][2]:
            all_flights[i].queue_first=True
            all_flights[i].flight_status='S'
            all_flights[i].service_time=30
        
        #any flight that is not the first of the day could have to wait for connecting flights    
        
        if all_flights[i].queue_first==False:
            h1=all_flights[i].origin
            h=np.where(h1 in parameters.nodes)[0][0]
            w=parameters.connectivity_fraction[h]
            r=random.random()
            if r<=w:
                all_flights[i].connections=True
                b+=1
    
    for i in range(1,m):
        if all_flights[i].connections==True:
            C=[]
            for j in range(1,m):
                if i!=j and all_flights[i].origin==all_flights[j].destination and  all_flights[j].CRS_arr_time< all_flights[i].CRS_dep_time and (all_flights[j].CRS_arr_time + 180) >= all_flights[i].CRS_dep_time and all_flights[j].CRS_dep_time< all_flights[j].CRS_arr_time:
                    C.append(j)
        #choose random flight from all the possible connections
            l=len(C)
            if l==1:
                cf=C[0]
                all_flights[i].connecting_flight = cf
            elif l==0:
                #if there are no available connections
                all_flights[i].connections=False
                #print i, all_flights[i].connections
            else:
                r=random.randint(0,l-1)
                cf=C[r]
                all_flights[i].connecting_flight = cf
    
    if all_flights[0].real_dep_time>all_flights[1].real_dep_time:
        all_flights[0].queue_first=False
        all_flights[1].queue_first=True
    
               
    parameters.remaining_flights=all_flights
    parameters.SAAR_matrix=np.genfromtxt('SAAR_matrix_top20')
    print delayed, b
################################################################################
            
def update_system(remaining_flights):
    import parameters
    
    parameters.N_flights_remaining=0
    for l,m in parameters.remaining_flights.items():
        r=0
        if m.completed==True:
            parameters.N_flights_completed+=1
            #print l,m
            r+=1
            del parameters.remaining_flights[l]
            print len(parameters.remaining_flights)
        else:
            parameters.N_flights_remaining+=1
    
