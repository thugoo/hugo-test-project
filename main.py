import math
import json
import random


def getPatrolStartTime(fileName):
    """

    :param fileName: Name of text file that contains information about patrol and platoon
    :return: String, value is start time of nightly routine (hours:minutes format)
    """
    with open(fileName) as f:
        lines = f.readlines()

        for line in lines:
            return line.split(",")[0]


# ------------------------------------------------------------------------------------------------------------------------------------------------


def getPatrolEndTime(fileName):
    """

    :param fileName: Name of text file that contains information about patrol and platoon
    :return: String, value is end time of nightly routine ('hours:minutes' format)
    """
    with open(fileName) as f:
        lines = f.readlines()

        for line in lines:
            return line.split(",")[1]


# ------------------------------------------------------------------------------------------------------------------------------------------------


def getTotalPatrolTime(fileNameOrString, isString):
    """

    :param fileNameOrString: String, which either contains the name of text file
            or the time of start and end of the nighly routine
            ('hours:minutes,hours:minutes' format)
    :param isString: Boolean, that makes the function use the first parameter as a file name
            or a string with start/end times
    :return: Double, value is the total duration of nightly routine
    """

    # if the information is given by command line
    if len(fileNameOrString) == 0:
        timeStartString = input("When does nightly routine begin? (Format: \"HH:MM\"): ")
        timeEndString = input("When does nightly routine end? (Format: \"HH:MM\"): ")

    # if the first parameter contains the beginning and end times of nighly routine
    elif isString:
        timeStartString = fileNameOrString[0].split(",")[0]
        timeEndString = fileNameOrString[0].split(",")[1]

    # if the first parameter contains the name of the file, where information about patrol times are in
    else:
        with open(fileNameOrString) as f:

            lines = f.readlines()

            timeStartString = lines[0].split(",")[0]
            timeEndString = lines[0].split(",")[1]

    if timeStartString[:1] == 0:
        timeStart = float(timeStartString[1:2])
    else:
        timeStart = float(timeStartString[:2])

    if timeStartString[3:4] == 0:
        timeStartMinutes = float(timeStartString[4:])
    else:
        timeStartMinutes = float(timeStartString[3:])

    timeStart += timeStartMinutes / 60

    if timeEndString[:1] == 0:
        timeEnd = float(timeEndString[1:2])
    else:
        timeEnd = float(timeEndString[:2])

    if timeStartString[3:4] == 0:
        timeEndMinutes = float(timeEndString[4:])
    else:
        timeEndMinutes = float(timeEndString[3:])

    timeEnd += timeEndMinutes / 60

    if timeStart > timeEnd:
        timeEnd += 24

    return timeEnd - timeStart


# ------------------------------------------------------------------------------------------------------------------------------------------------


def getPlatoonInfo(fileName):
    """

    :param fileName: Name of text file that contains information about patrol and platoon

    :return: List that contains information about the platoon
        Each element in list is a tuple that holds information about its squad:
            first element: list which contains the soldiers of the squad
            second element: list - stove watch timetable with times and names for each timeslot
            third element: list - patrol timetable with times and names for each timeslot
    :raises valueError: if given input doesn't only contain numbers
    :raises fileNotFoundError: if file with given name doesn't exist
    """
    platoon = []

    # if the information is given through command line
    if len(fileName) == 0:

        try:

            while True:
                squadCount = int(input("How many squads are in the platoon? (1-4): "))
                if 1 <= int(squadCount) <= 4:
                    break
                else:
                    print("There can only be 1 to 4 squads in a platoon!")

            squadSizes = []

            for i in range(squadCount):

                while True:
                    squadSize = int(input("How many soldiers are in the squad #" + str((i + 1)) + "? (5-12): "))
                    if 5 <= squadSize <= 12:
                        squadSizes.append(squadSize)
                        break
                    else:
                        print("There can only be 5 to 12 soldiers in a squad!")

            whichSquad = 1

            for i in squadSizes:
                squad = []

                print()
                print("Information about squad #" + str(whichSquad) + " soldiers.")
                whichSquad += 1
                print()

                drivers = 0
                canBeMoreDrivers = True

                for j in range(i):
                    rank = input(
                        "Enter the " + str(j + 1) + ". soldier's rank "
                                                    "in shortened format (Private = PVT, Sergeant = SGT): ")
                    name = input("Enter the " + str(j + 1) + ". soldier's name: ")

                    while True:
                        isDriver = input("Is the " + str(j + 1) + ". soldier a driver? (yes/no): ")

                        if isDriver == "yes" and not canBeMoreDrivers:
                            print("There can only be maximum of two drivers per squad!")

                        elif isDriver == "yes" or isDriver == "no":
                            if isDriver == "yes":
                                drivers += 1
                                if drivers == 2:
                                    canBeMoreDrivers = False
                            break

                        else:
                            print("Input has to be either a 'yes' or 'no'!")

                    soldier = (rank, name, isDriver)
                    squad.append(soldier)

                squadInfo = {
                    "soldiers": squad,
                    "stoveWatchTimetable": [],
                    "patrolTimetable": []
                }

                platoon.append(squadInfo)

            return platoon

        except ValueError:
            print("Input has to be a whole number!")

    # if the information is given from a text file
    else:

        squad = []
        i = 0

        try:
            with open(fileName) as f:
                lines = f.readlines()

                # https://stackoverflow.com/questions/24982993/pythondetect-if-the-current-line-in-file-read-is-the-last-one
                last = lines[-1]

                for line in lines:
                    i += 1
                    line = line.strip()

                    if len(line) == 0:

                        squadInfo = {
                            "soldiers": squad,
                            "stoveWatchTimetable": [],
                            "patrolTimetable": []
                        }

                        platoon.append(squadInfo)
                        squad = []

                    elif not line[:1].isnumeric():

                        soldierList = line.split(",")

                        # soldier is in tuple format: rank, name, are they a driver ('yes'/'no')
                        soldier = (soldierList[0], soldierList[1], soldierList[2])

                        squad.append(soldier)

                    if last == line and i == len(lines):
                        squadInfo = {
                            "soldiers": squad,
                            "stoveWatchTimetable": [],
                            "patrolTimetable": []
                        }

                        platoon.append(squadInfo)

            return platoon

        except FileNotFoundError:
            print("This file doesn't exist!")

    return platoon


# ------------------------------------------------------------------------------------------------------------------------------------------------


def getTimePerSolder(fileName, squadInfo):
    """

    :param fileName: Name of text file that contains information about patrol and platoon
    :param squadInfo: Tuple that holds information about given squad
    :return: Double, has the value of patrol length per soldier in squad
    """
    return getTotalPatrolTime(fileName, False) / len(squadInfo["soldiers"])


# ------------------------------------------------------------------------------------------------------------------------------------------------


def makeTimetable(fileName, squadInfo, platoon):
    """

    :param fileName: Name of text file that contains information about patrol and platoon
    :param squadInfo: Tuple that holds information about given squad
    :param platoon: List that holds the squads in platoon
    :return: List, elements are in tuple format
            first element: time of shift
            second element: name of the soldier on this shift
    """
    timetable = []

    startTime = getPatrolStartTime(fileName)

    hours = int(startTime[:2])
    minutes = int(startTime[3:])

    if minutes >= 50:
        hours += 1

    minutes = 0

    endTime = getPatrolEndTime(fileName)

    endHours = int(endTime[:2])
    endMinutes = int(endTime[3:])

    if endMinutes >= 10:
        endHours += 1

    endMinutes = 0

    timetable.append(("%d:%02d" % (hours, minutes), ""))

    # if there is only one squad
    if len(platoon) == 1:

        timePerSoldier = getTimePerSolder(fileName, squadInfo)

        perHours = math.floor(timePerSoldier)
        perMinutes = 60 * (timePerSoldier % 1)

        while True:
            minutes += perMinutes

            if minutes >= 60:
                minutes -= 60
                hours += 1

            hours += perHours

            if hours >= 24:
                hours -= 24
            if hours == endHours and minutes == endMinutes:
                break

            timetable.append(("%d:%02d" % (hours, minutes), ""))

        return timetable

    # if there are multiple squads, in that case makes the timeslots one hour each
    else:
        perHours = 1

        while True:
            hours += perHours

            if hours >= 24:
                hours -= 24
            if hours == endHours and minutes == endMinutes:
                break

            timetable.append(("%d:%02d" % (hours, minutes), ""))

        return timetable


# ------------------------------------------------------------------------------------------------------------------------------------------------


def makePatrolTimeTable(fileName, squadInfo, platoon):
    """

    :param fileName: Name of text file that contains information about patrol and platoon
    :param squadInfo: Tuple that holds information about given squad
    :param platoon: List that holds the squads in platoon
    :return: List, elements are in tuple format
            first element: time of shift
            second element: tuple, name of the two soldiers on this shift
    """
    patrolTimeTable = []
    timetable = makeTimetable(fileName, squadInfo, platoon)

    totalTime = getTotalPatrolTime(fileName, False)

    squadPatrolIndex = platoon.index(squadInfo)

    # if there is only one squad
    if len(platoon) == 1:
        return timetable

    # if there are two squads
    elif len(platoon) == 2:

        for squadCheck in platoon:
            if squadInfo != squadCheck:
                otherSquad = squadCheck

        # if one squad is not at least two times larger than other one
        if len(squadInfo["soldiers"]) * 2 > len(otherSquad["soldiers"]) \
                and len(squadInfo["soldiers"]) < len(otherSquad["soldiers"]) * 2:

            equalPatrolTime = int(len(timetable) / 2)

            for time in range(squadPatrolIndex * equalPatrolTime, equalPatrolTime * (squadPatrolIndex + 1)):
                patrolTimeTable.append(timetable[time])

            return patrolTimeTable

        # if one squad is atleast two times larger than the other squad
        # in this case the smaller squad gets less patrol timeslots
        else:

            lesserPatrolTime = math.floor(len(timetable) * (1 / 3))

            if len(squadInfo["soldiers"]) * 2 <= len(otherSquad["soldiers"]):

                firstOrSecondStart = squadPatrolIndex * (len(timetable) - (squadPatrolIndex * lesserPatrolTime))
                firstOrSecondEnd = lesserPatrolTime + (
                        squadPatrolIndex * (len(timetable) - (squadPatrolIndex * lesserPatrolTime)))

                for time in range(firstOrSecondStart, firstOrSecondEnd):
                    patrolTimeTable.append(timetable[time])

            elif len(squadInfo["soldiers"]) >= len(otherSquad["soldiers"]) * 2:

                firstOrSecondStart = squadPatrolIndex * (len(timetable) - (
                        squadPatrolIndex * (len(timetable) - (squadPatrolIndex * lesserPatrolTime))))
                firstOrSecondEnd = len(timetable) - lesserPatrolTime + (squadPatrolIndex * 2)

                for time in range(firstOrSecondStart, firstOrSecondEnd):
                    patrolTimeTable.append(timetable[time])

            return patrolTimeTable

    # if there are more than two squads
    # divides timeslots by squad sizes, bigger squads get more timeslots
    else:

        # https://stackoverflow.com/questions/20348717/algo-for-dividing-a-number-into-almost-equal-whole-numbers
        times = [totalTime // len(platoon) + (1 if number < totalTime % len(platoon) else 0) for number in
                 range(len(platoon))]

        squadSizes = []
        index = 0

        for squadCheck in platoon:
            squadSizes.append((index, len(squadCheck["soldiers"])))
            index += 1

        # https://stackoverflow.com/questions/8459231/sort-tuples-based-on-second-parameter
        times.sort()
        squadSizes.sort(key=lambda x: x[1])

        for squadTuple in squadSizes:
            if squadTuple[0] == squadPatrolIndex:
                index = squadSizes.index(squadTuple)

        summa = 0

        for n in range(index):
            summa += times[n]

        for time in range(int(summa), int(summa + times[index])):
            patrolTimeTable.append(timetable[time])

        return patrolTimeTable


# ------------------------------------------------------------------------------------------------------------------------------------------------


def organizeTable(fileName, squadInfo, platoon):
    """
        METHOD WASN'T FINISHED, CURRENTLY PUTS SOLDIERS RANDOMLY INTO TIMESLOTS

    :param fileName: Name of text file that contains information about patrol and platoon
    :param squadInfo: Tuple that holds information about given squad
    :param platoon: List that holds the squads in platoon
    :return: Organizes squad members into patrol/stove watch timeslots,
            while optimizing the amount of consecutive sleep each soldier gets
    """
    canDriversPatrol = True
    canDriversWatchStove = True
    drivers = []

    timetable = squadInfo["stoveWatchTimetable"]
    totalTime = getTotalPatrolTime(fileName, False)

    firstPatrolTime = squadInfo["patrolTimetable"][0]
    lastPatrolTime = squadInfo["patrolTimetable"][len(squadInfo["patrolTimetable"]) - 1]

    for soldier in squadInfo["soldiers"]:
        if soldier[2] == "yes":
            drivers.append(soldier)

    if len(drivers) == 0:
        canDriversPatrol = False
        canDriversWatchStove = False

    if firstPatrolTime != timetable[0] and lastPatrolTime != timetable[len(timetable) - 1]:
        canDriversPatrol = False

    if totalTime - 2 < 6:
        canDriversPatrol = False
        if totalTime - 1 < 6:
            canDriversWatchStove = False

    if canDriversPatrol:

        if len(drivers) > 1:
            otherSoldier = drivers[1]
        else:
            for soldier in squadInfo["soldiers"]:
                if soldier != drivers[0]:
                    otherSoldier = soldier
                    break

        if firstPatrolTime == timetable[0]:
            for time in range(2):
                squadInfo["patrolTimetable"][time][1] = (drivers[0], otherSoldier)
        elif lastPatrolTime == timetable[len(timetable) - 1]:
            for time in range(2):
                squadInfo["patrolTimetable"][len(squadInfo["patrolTimetable"]) - time][1] = (drivers[0], otherSoldier)

    # fills timeslots with random soldiers
    for time in squadInfo["patrolTimetable"]:
        timeIndex = squadInfo["patrolTimetable"].index(time)
        timeClock = time[0]
        newTime = (timeClock, random.choice(squadInfo["soldiers"]))
        squadInfo["patrolTimetable"][timeIndex] = newTime

    for time in squadInfo["stoveWatchTimetable"]:
        timeIndex = squadInfo["stoveWatchTimetable"].index(time)
        timeClock = time[0]
        newTime = (timeClock, random.choice(squadInfo["soldiers"]))
        squadInfo["stoveWatchTimetable"][timeIndex] = newTime

    if not canDriversPatrol and canDriversWatchStove:
        driverAvailable = totalTime - 6


# ------------------------------------------------------------------------------------------------------------------------------------------------
    """
    
    main method
    """


file = input(
    "To enter information from a text file, input the name of the textfile; "
    "to enter information from the command line, give an empty input: ")

platoonList = getPlatoonInfo(file)
stoveWatch = makeTimetable(file, platoonList[0], platoonList)

for squadIndex in range(len(platoonList)):
    platoonList[squadIndex]["stoveWatchTimetable"] = stoveWatch
    platoonList[squadIndex]["patrolTimetable"] = makePatrolTimeTable(file, platoonList[squadIndex], platoonList)
    organizeTable(file, platoonList[squadIndex], platoonList)

squadIndex = 1
print()
for squadDict in platoonList:
    print("SQUAD #" + str(squadIndex))
    print()
    for soldierInfo in squadDict["soldiers"]:
        print(soldierInfo)
    squadIndex += 1
    print(squadDict["stoveWatchTimetable"])
    print(squadDict["patrolTimetable"])
    print()

while True:
    saveInput = input("Do you wish to save the output into a file? (yes/no): ")
    if saveInput == "yes" or saveInput == "no":
        break
    else:
        print("Input has to be either a 'yes' or 'no'!")

if saveInput == "yes":
    with open('output.txt', 'w') as newFile:
        json.dump(platoonList, newFile, indent=4)
