#Day starts at 3 AM (=180 min)
t0=179
#Day finishes at 2:59 AM (=180min + 1439 min)
t_max=1618

#Delimiters of each "clock hour"
time_bins=[179,239,299,359,419,479,539,599,659,719,779,839,899,959,1019,1079,1139,1199,1259,1319,1379,1439,1499,1559]

#List of airports
nodes=['ATL','ORD','DFW','DEN','LAX','IAH','PHX','DTW','LAS','SFO','CLT','MSP','MCO','SLC','BOS','EWR','JFK','LGA','BWI','SEA']


N=[]
all_flights = {} #Dictionary of all the flights for the day
remaining_flights = {} #Dictionary of all the remaining flights for the day
completed_flights = {} #Dictionary of all the completed flights 
N_flights_total = 0 #Total number of flights
N_flights_completed = 0 #Number of completed flights
N_flights_remaining = 0 #Number of flights remaining
tail_queues=[] #Lists of remaining flights (organized by departing airport)
arrival_queues=[] #Lists of remaining flights (organized by arrival airport)
SAAR_matrix=[] #List of airport capacity each hour
connectivity_fraction=[] #List of fraction of connecting passengers for each airport
