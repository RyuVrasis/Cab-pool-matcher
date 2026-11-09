import heapq
import json
from classes import RideRequest, Cab

def load_cabs(filename):
    cabs = []
    try:
        data = json.load(open(filename))
        for item in data:
            cab = Cab(item["driver"],item["seats"],item["destination"],item["time"])
            cabs.append(cab)
      
    except FileNotFoundError:
        print(f"Could not find {filename}.Starting with no cabs")
    return cabs

cabs = load_cabs("cabs.json")  
waiting = {}
request_counter = 0

while True:
    print("\n1.Add a new ride request.")
    print("2.See everyone who is still waiting for their cab.")
    print("3.Find your perfect match ( in cabs ofcourse)")
    print("4.Dispatch Cabs")
    print("5.Quit the app")

    choice = input("Choose:\n").strip()

    if choice == "1":
        while True:
            name = input("Name: ").strip()
            if name == "":
                print("Name can't be empty son")
            elif not name.replace(" ", "").isalpha():
                print("Sonion ring,Name should contain only letters and spaces")
            else:
                break

        while True:
            print("enter city number 1.Delhi 2. Jaipur")    
            destination = input("city num:").strip()
            if destination == "1":
                city = "Delhi"
                break
            elif destination == "2":
                city = "Jaipur"
                break
            else:
                print("enter either 1 or 2 son")

        while True:
            print("choose the time zone : 1. morning 2. afternoon 3.evening 4.night")
            slot = input("time slot:").strip()
            if slot == "1":
                time = "Morning"
                break
            elif slot == "2":
                time = "Afternoon"
                break
            elif slot == "3":
                time = "Avening"
                break
            elif slot == "4":
                time = "Night"
                break
            else:
                print("goddamn enter smth between 1-4")
        while True:
            try:
                year = int(input("Year (1-5): ").strip())
                if 1 <= year <= 5:
                    break
                print("Year must be between 1 and 5")
            except ValueError:
                print("Please enter a number")

        request_counter += 1
        request = RideRequest(name, city, time, year, request_counter)
        key = (request.city,request.time)
        if key not in waiting:
            waiting[key] = []
        heapq.heappush(waiting[key],(-request.year,request.request_num,request))
        print("Added:", request)
        open_cab_found = False
        for cab in cabs:
            if cab.destination == request.city and cab.dep_time == request.time and not cab.has_left:
                open_cab_found= True
        if not open_cab_found:
            print("Tough luck gng,No open cab for this trip right now.You have been placed in the waiting list for now lol")  


    elif choice == "2":
        print("waiting students:")
        anyone_waiting = False
        for key in waiting:
            for item in sorted(waiting[key]):
                print("",item[2])
                anyone_waiting = True
        if not anyone_waiting:
            print("nobody is waiting") 
        print("Cabs:")
        for cab in cabs:
            print("",cab)

    #find matches
    elif choice =="3":  
        for cab in cabs:
            if cab.has_left == True:
                continue
            elif cab.has_left == False:
                trip_key = (cab.destination,cab.dep_time)
                trip_list = waiting.get(trip_key,[])
                queue = heapq.nsmallest(cab.free_seats(),trip_list)
                print(cab)
                if len(queue) == 0:
                    print("nobody is wating for the trip")
                else:
                    for request in queue:
                        print(" -->",request)

    #dispatching students               
    elif choice =="4":
        open_cabs = []
        for cab in cabs:
            if cab.has_left == False :
                open_cabs.append(cab)
            
        if len(open_cabs) == 0:
            print("No cabs available")
            continue

        for i in range(len(open_cabs)):
            print(f"{i+1}-{open_cabs[i]}")

        while True:
            try:
               cab_number = int(input("enter the cab number:"))
            except:
                print("enter an integral cab number son")
                continue
            if cab_number <= 0 or cab_number > len(open_cabs):
                print("sonion enter a number in cab range")
                continue  
            chosen = open_cabs[cab_number - 1]
            break
        trip_key = (chosen.destination,chosen.dep_time)
        trip_list = waiting.get(trip_key,[])
        seats = chosen.free_seats()
        queue = []
        while len(queue) < seats and len(trip_list)> 0:
            item = heapq.heappop(trip_list)
            queue.append(item[2])
        chosen.student_list.extend(queue)
        chosen.has_left = True
        print(f"Cab driver {chosen.driver_name} has left with {len(queue)} passengers")
        for item in queue:
            print(f"-->{item}")                         

    elif choice == "5":
        print("bye-bye.Be sure to rate ts broskii.Any feedback is much appreciated.")
        break
    else:
        print("enter 1,2,3,4 or 5 boii")
