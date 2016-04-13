class Flight(object):

    def __init__(self, ID, airline, plate, origin, destination, CRS_dep_time, CRS_arr_time,legs,initial_delay):
    
        self.ID = ID
        self.airline = airline
        self.plate = plate
        self.origin = origin
        self.destination = destination
        self.CRS_dep_time = CRS_dep_time
        self.CRS_arr_time = CRS_arr_time
        self.legs = legs
        self.BTB_time = CRS_arr_time - CRS_dep_time
        self.initial_delay = initial_delay
        self.flight_status = 'L'
        self.service_time = 0
        self.queue_first = False
        self.connections = False
        self.connecting_flight = -1
        self.inb_delay = 0
        self.queue_delay = 0
        self.conn_delay = 0
        self.dep_delay = self.initial_delay + self.inb_delay + self.queue_delay + self.conn_delay
        self.delayed = False
        self.completed = False
        self.real_dep_time = self.CRS_dep_time + self.dep_delay 
        self.real_arr_time = self.real_dep_time + self.BTB_time
