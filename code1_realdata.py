import numpy as np
import flights
import parameters
from parameters import *
import initialize
from initialize_realdata import *
    
def main():
    #Load starting queues into the system
    start_system(parameters.all_flights)
    N_flights_total=len(all_flights)
    N_flights_remaining=len(all_flights)
    tau=t0
    N=parameters.N
    #the code will run until: the day is over OR  there are no flights remaining
    #file1=open('delays.txt','w',buffering=0)
    
    while tau in range(t0,t_max) and N_flights_remaining!=0:
        hour=np.digitize([tau],parameters.time_bins)
        
        for l, m in parameters.remaining_flights.items():
            
            #if l==0:
                #just for testing, to force the first flight in ATL to depart
                #m.flight_status='S'
                #m.service_time=30
                #m.queue_first=True
                #m.connections=False
                #m.real_arr_time==tau
                #m.flight_status, m.real_arr_time    
            
            
            #plane ready to be serviced
            if tau>=(m.real_dep_time - 30) and m.flight_status=='L' and m.legs==1:
                m.flight_status = 'S'
            
            #plane in service
            if tau>=(m.real_dep_time - 30) and m.flight_status=='S' and m.service_time<30:
                m.service_time += 1
                
                    
            if tau>=m.real_dep_time:
                
                if m.flight_status=='S' and m.service_time>=30 and m.queue_first==True and m.connections==False:
                    #check if the capacity of the airport is not surpased
                                  
                    if parameters.SAAR_matrix[nodes.index(m.origin),hour[0]-1]>=1:
                        parameters.SAAR_matrix[nodes.index(m.origin),hour[0]-1]-=1
                    
                        #print tau, 'aircraft can depart', m.ID, m.origin, m.destination 
                        #change flight status
                        m.flight_status='F'
                        #print m.ID, 'departed', m.real_dep_time, tau
                        #remove flight from departure queue
                        origin=m.origin
                        a=np.where(N==origin)[0][0]
                    
                        for j in range(0,len(parameters.tail_queues[a])):
                            if parameters.tail_queues[a][j][0]==l:
                                b=j
                        parameters.tail_queues[a]=np.delete(parameters.tail_queues[a],b,0)
                        #make the next plane in the queue the first --> but first reorder the list
                        U=[]
                        for u in range(0,len(parameters.tail_queues[a])):
                            U.append(parameters.tail_queues[a][u][0])
                        U2=[]
                        #figure out the real departure time of all the remaining flights in the airport and find the next one 
                        for u in U:
                            for l2, m2 in parameters.remaining_flights.items():
                                if m2.ID==u:
                                    U2.append(m2.real_dep_time)
                        U3=sorted(zip(U2,U))
                        if len(U3)!=0:
                            first=U3[0][1]
                    
                        parameters.remaining_flights[first].queue_first=True
                        #print b, parameters.remaining_flights[b].queue_first, parameters.remaining_flights[b].origin, parameters.remaining_flights[b].destination
                    #else:
                        #m.dep_delay += 1
                        #m.queue_delay += 1    
                elif m.flight_status!='L' and m.legs>1:
                    #previous legs are not completed
                    m.dep_delay += 1
                    m.inb_delay += 1
                    m.real_dep_time += 1
                    m.real_arr_time += 1
                    print 'inb_delayed!'
                elif m.flight_status=='S' and m.service_time<30:
                    #aircraft is in service
                    m.dep_delay += 1
                    m.service_time += 1
                    m.real_dep_time += 1
                    m.real_arr_time += 1
                    #print 'in service!'
                elif m.flight_status =='S' and m.service_time==30 and m.queue_first=='False':
                    #aircraft in airport's queue
                    m.dep_delay += 1
                    m.queue_delay += 1
                    m.real_dep_time += 1
                    m.real_arr_time += 1
                elif m.flight_status=='S' and m.service_time==30 and m.connections=='True':
                    #connections not landed
                    m.dep_delay += 1
                    m.conn_delay += 1
                    m.real_dep_time += 1
                    m.real_arr_time += 1
            
                #if m.flight_status=='L' and m.real_dep_time>=tau and m.legs==1:
                    #plane ready to be serviced
                    #m.flight_status=='S'
            
                if m.flight_status=='F' and tau >= m.real_arr_time:
                    #print tau, 'flight can land', m.ID, m.origin, m.destination
                    m.flight_status = 'L'
                    m.completed = True
                    for q, r in parameters.remaining_flights.items():
                        if r.plate==m.plate and r!=m:
                            r.legs-=1
                            if r.legs<=0:
                                print r.ID, r.plate, r.origin, r.destination, tau, r.real_dep_time 
                        if r.connections==True and r.connecting_flight==m.ID:
                            #print 'connection landed!'
                            r.connections=False
        
        
            #check that all flights are either completed or remaining
            #if parameters.N_flights_total != parameters.N_flights_completed + parameters.N_flights_remaining:
                #print 'Some flights are in limbo!'
                #break
    
        #if tau/200 == tau/200.0 or tau==t_max-1 or tau==t0:
        if tau in parameters.time_bins:
            filename = ('Flights_tau%i.txt' % (tau))
            file = open(filename, 'w')
            file.write('#ID' +'\t'+ 'plate' +'\t'+ 'origin' +'\t'+ 'destination' +'\t'+ 'departure' +'\t'+ 'CRS_dep'+'\t'+ 'CRS_arr'+'\t'+ 'arrival' +'\t'+ 'flight_status' +'\t'+ 'queue_first' +'\t'+ 'service_time' +'\t'+ 'legs' +'\t'+ 'initial_delay' +'\t'+ 'completed' + '\t' + 'connections' + '\t' + 'connecting_flight' + '\n')
            
            filename2 = ('Delays_tau%i.txt' % (tau))
            file2 = open(filename2, 'w')
            file2.write('#ID'+'\t'+ 'plate' +'\t'+ 'origin' +'\t'+ 'destination'+'\t'+ 'CRS_dep' +'\t'+ 'departure' +'\t'+ 'total_delay' +'\t'+ 'dep_delay' + '\t' + 'initial_delay' + '\t' + 'inbound_delay' +'\t'+ 'queue_delay' + '\t' + 'connection_delay' + '\n')
            for l, m in parameters.remaining_flights.items():
                #print ID, seq
                #print seq.sequence, seq.tot, seq.bond_struct
                file.write(str(m.ID)+ '\t' + str(m.plate)  + '\t' + str(m.origin)+ '\t' + str(m.destination)+ '\t' + str(m.real_dep_time) + '\t'+ str(m.CRS_dep_time) +  '\t' + str(m.CRS_arr_time) +  '\t' + str(m.real_arr_time) + '\t' + str(m.flight_status)+ '\t' + str(m.queue_first)+ '\t' + str(m.service_time)+ '\t' + str(m.legs) + '\t' + str(m.initial_delay) + '\t' + str(m.completed) + '\t' + str(m.connections) + '\t' + str(m.connecting_flight) + '\n')
                
            file.close()
            
            filename = ('Airport_summary_tau%i.txt' % (tau))
            file = open(filename, 'w')
            for r in range(0,20):
                file.write(str(len(parameters.tail_queues[r])) + '\n')
            
            file.close()
                
        #remove all the completed flights from the list:
        #update_system(parameters.remaining_flights)
        N_flights_remaining=0
        for l,m in parameters.remaining_flights.items():
            #r=0
            if m.completed==True:
                if m.CRS_dep_time!=m.real_dep_time:
                    m.delayed=True
                    
                parameters.N_flights_completed+=1
               
                if tau in parameters.time_bins:
                    if m.delayed==True:
                        file2.write(str(m.ID)+'\t'+str(m.plate)+'\t'+str(m.origin)+'\t'+str(m.destination)+'\t'+str(m.CRS_dep_time) + '\t'+str(m.real_dep_time) + '\t'+ str(m.real_dep_time - m.CRS_dep_time ) + '\t'+ str(m.dep_delay) + '\t'+ str(m.initial_delay) + '\t'+ str(m.inb_delay)+ '\t'+ str(m.queue_delay) + '\n')
                        
                #print l,m
                #r+=1
                del parameters.remaining_flights[l]
                
            else:
                N_flights_remaining+=1
        
        
        file2.close()            
        
        
        #print tau, len(parameters.remaining_flights)
        tau+=1
        #print tau
    print  tau, parameters.N_flights_completed
    execfile("output.py")
   
    
if __name__=="__main__":
    main()
