import json
from classes import RideRequest, Cab

def load_cabs(filename):
    cabs = []
    try:
        with open(filename) as f:
            data = json.load(f)
        for item in data:
            cab = Cab(item["driver"],item["seats"],item["destination"],item["time"])
            cabs.append(cab)
    except FileNotFoundError:
        print(f"Could not find {filename}.Starting with no cabs")
    return cabs

cabs = load_cabs("cabs.json")      

for cab in cabs:
    print(cab)

waiting_list = []
request_counter = 0

while True:
    print("1.Add a new ride request.")
    print("2.See everyone who is still waiting.")
    print("3.Quit the app")

    choice = input("Choose:").strip()

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
                city = "delhi"
                break
            elif destination == "2":
                city = "jaipur"
                break
            else:
                print("please enter either 1 or 2")

        while True:
            print("choose the time zone : 1. morning 2. afternoon 3.evening 4.night")
            slot = input("time slot:").strip()
            if slot == "1":
                time = "morning"
                break
            elif slot == "2":
                time = "afternoon"
                break
            elif slot == "3":
                time = "evening"
                break
            elif slot == "4":
                time = "night"
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
        waiting_list.append(request)
        print("Added:", request)

    elif choice == "2":
        if len(waiting_list) == 0:
            print("Nobody is waiting")
        else:
            print("Waiting students:")
            for request in waiting_list:
                print(" ", request)

    elif choice == "3":
        print("see you soon")
        break
    else:
        print("please enter 1,2,3")
