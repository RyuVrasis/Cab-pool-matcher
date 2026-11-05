while True:
    print("1.Add a new ride request.")
    print("2.See everyone who is still waiting.")
    print("3.Quit the app")

    choice = input("Choose:").strip()

    if choice == "1":
        while True:
            print("enter the city number that you want to go to 1.Delhi 2. Jaipur")

            destination = input("city:").strip()
            if destination == "1":
                city = "delhi"
                break
            elif destination == "2":
                city = "jaipur"
                break
            else:
                print("please enter either 1 or 2")
    elif choice == "2":
        print("coming soon")
    elif choice == "3":
        print("see you soon")
        break
    else:
        print("please enter 1,2,3")
