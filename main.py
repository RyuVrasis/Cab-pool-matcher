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

for cab in cabs:
    print(cab)

waiting = {}
request_counter = 0

while True:
    print("\n1.Add a new ride request.")
    print("2.See everyone who is still waiting.")
    print("3.Find matches")
    print("4.Dispatch Cabs")
    print("5.Quit the app")

    choice = input("Choose:\n").strip()

    if choice == "1":
        while True:
            name = input("Name: ").strip()
            if name == "":
                print("Name can't be empty")
            elif not name.replace(" ", "").isalpha():
                print("Name should contain only letters and spaces")
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
                print("please enter either 1 or 2")

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
                print("please enter either 1,2,3 or 4")
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
        waiting[key].append(request)
        print("Added:", request)

    elif choice == "2":
        print("waiting students:")
        anyone_waiting = False
        for key in waiting:
            for request in waiting[key]:
                print("",request)
                anyone_waiting = True
        if not anyone_waiting:
            print("nobody is waiting") 

    elif choice =="3":  
        for cab in cabs:
            if cab.has_left == True:
                continue
            elif cab.has_left == False:
                trip_key = (cab.destination,cab.dep_time)
                trip_list = waiting.get(trip_key,[])
                queue = trip_list[:cab.free_seats()]
                print(cab)
                if len(queue) == 0:
                    print("nobody is wating for the trip")
                else:
                    for request in queue:
                        print(" -->",request)

                    
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
        queue = trip_list[:chosen.free_seats()]

        waiting[trip_key] = trip_list[chosen.free_seats():]
        chosen.student_list.extend(queue)
        chosen.has_left = True
        print(f"{chosen.driver_name} has left with {len(queue)} passengers")
        for item in queue:
            print(f"-->{item}")                         

    elif choice == "5":
        print("see you soon")
        break
    else:
        print("please enter 1,2,3,4 or 5")
