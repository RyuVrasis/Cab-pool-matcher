# Cab Pool Matcher

An app in Python that matches BITSians to shared cabs going to Delhi or Jaipur. Students submit ride requests, which wait in a queue for their trip (destination + time slot). Cabs are filled later, and when seats are short, seniors board first.

## How to run

Requirements to run : Python 3 installed

```
python main.py 

Execute this command in your terminal after pulling from github to the project folder, so the app can find 'cabs.json'.

## Files

|Files used|What it contains|
|-|-|
|'main.py'|The menu and all app logic|
|'classes.py'|The 'RideRequest' and 'Cab' classes|
|'cabs.json'|The list of available cabs, loaded when the app starts|

## Menu

```
1. Add a new ride request
2. See everyone who is still waiting (plus all cabs)
3. Find matches
4. Dispatch a cab
5. Quit the app
```

* **Add a new ride request** asks for name, city, time slot and year. Every answer is checked, so bad input (a city we don't serve, "Year 7", letters instead of a number) shows a friendly message instead of crashing.
* **See everyone waiting** lists every waiting student in boarding order, then every cab with its seats taken (like `2/4`) and whether it has left.
* **Find matches** is a preview only. For each open cab, it shows which students would get a seat if the cab left now. Nothing is changed.
* **Dispatch a cab** fills a cab with the most senior students waiting for its trip, up to its free seats, removes them from the waiting list, and marks the cab as left.

## The cab file

Cabs are loaded from `cabs.json` when the app starts. It is a list with one entry per cab:
\[
    {"driver": "XYZA", "seats": 3, "destination": "Delhi", "time": "Morning"},
    {"driver": "XYZB", "seats": 4, "destination": "Jaipur", "time": "Evening"},
    {"driver": "XYZC", "seats": 1, "destination": "Delhi", "time": "Afternoon"},
    {"driver": "XYZD", "seats": 3, "destination": "Jaipur", "time": "Night"},
    {"driver": "XYZE", "seats": 2, "destination": "Jaipur", "time": "Afternoon"}
]


|Key|Meaning|Allowed values|
|-|-|-|
|`driver`|Driver's name|Any text|
|`seats`|Number of seats|1 to 4|
|`destination`|Where the cab goes|"Delhi" or "Jaipur"|
|`time`|When it leaves|"Morning", "Afternoon", "Evening" or "Night"|

The values that are being  inputted are case  sensitive. If 'cabs.json' is missing, the app prints a message and starts with no cabs instead of crashing.

Each cab always starts as not left, with no passengers, so those are set inside the `Cab` class and are not part of the file.

## How it works

**One priority queue per trip. -**  Waiting students are stored in a dictionary. The key is the trip, for example `("Delhi", "Morning")`, and the value is a heap (priority queue) of the students waiting for that trip. The queue belongs to the trip, not to any one cab. A cab's passenger list is a normal list.

**Seniors first.** Python's 'heapq' is a min-heap, so it always gives the smallest item first. Each student is pushed as a tuple:

python (-year, request\_number, request)


* '-year' puts the highest year first: a 5th year is stored as -5, which is smaller than -1 for a 1st year.
* 'request\_number' breaks ties between students in the same year (explained below).
* 'request' is the actual 'RideRequest' object, used when printing or boarding.

**Find Matches and Dispatch agree.** Find Matches uses 'heapq.nsmallest', which shows the students who would come out first without removing them. Dispatch uses 'heapq.heappop', which removes them in the same order. So the preview always shows exactly who Dispatch would take.

**Fixed order.** Cabs are always checked in the order they appear in 'cabs.json', so the app gives the same result every time.

## Tricky situations

### 1\. Half-empty cab

A cab can leave with fewer students than its seats. Dispatch takes as many students as are waiting for that trip, up to the free seats, and stops when either the cab is full or nobody is left. The cab then shows, for example, '1/4' and "has left". It can't take anyone else after it leaves, because only cabs that haven't left are ever offered for matching or dispatch.

### 2\. No cabs left

Students are never lost. A new request is always added to its trip's waiting list, whether or not a cab is available. If no open cab exists for that trip (all have left, or there never was one), the student sees:
"No open cab for this trip right now. You will stay in the waiting list."

They stay visible in "See everyone waiting". If every cab has left, Dispatch shows "No cabs available" and changes nothing.

### 3\. Same year

Every request gets a request number from a counter that only goes up (1, 2, 3 ...) and never resets. A lower number means the student asked earlier. This number is the second item in the heap tuple, so when two students have the same year, the one with the lower number comes out first.

This also stops a crash. Python compares tuples item by item, and comparing two 'RideRequest' objects directly would raise a `TypeError`. Because no two requests share a request number, the comparison is always decided by the first two items and never reaches the objects.

### 4\. Lots of students (1,000 waiting)

Here 'n' is the number of students waiting for a trip and 'C' is the number of cabs.

|Operation|Big-O|Why|
|-|-|-|
|Adding one request|O(log n + C)|`heappush` is O(log n). Finding the trip's queue in the dictionary is O(1) on average. Checking whether an open cab exists for that trip looks at each cab once, which is O(C).|
|Adding all 1,000|O(n log n)|1,000 pushes at O(log n) each.|
|Sending off one cab (up to 4 students)|O(C + log n)|Listing the open cabs is O(C). Then up to 4 `heappop` calls at O(log n) each; 4 is a constant, so that part is O(log n).|
|Finding an open cab for a trip|O(C)|The app goes through the cab list and checks each cab's destination, time and whether it has left.|

For 1,000 students, log n is about 10, so taking the most senior students from a heap needs about 10 steps per student instead of searching all 1,000.

## Why JSON

The cab list is stored as JSON because:

* **People can read and edit it.** Anyone can open `cabs.json` in a text editor and add a cab.
* **It is in the standard library.** Python's `json` module reads it, so no packages need installing.



## Input validation

|Input|Rule|On bad input|
|-|-|-|
|Menu choice|1 to 5|Message, menu again|
|Name|Not empty, letters and spaces only|Message, ask again|
|City|Picked from a numbered list|Message, ask again|
|Time slot|Picked from a numbered list|Message, ask again|
|Year|Whole number from 1 to 5|Message, ask again|
|Cab number (dispatch)|A number from the list shown|Message, ask again|


