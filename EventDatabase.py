import time
import os
import random

class DataCollection:
    name = {}
    count = 0
    basepath = 'C:\\EventDatabase\\'
    unevent = 'Unevent.txt'
    brady = 'Brady.txt'
    tachy = 'Tachy.txt'
    datasize = 21
    #'2016 01 01 24 59 59\n'
    #'YYYY MM DD HH MM SS\n'
    #'123456789012345678901' = 21
    #print (time.strftime('%Y %m %d %H %M %S'))

    def __init__(self, name):
        self.count += 1
        self.name[self.count]=name
        #person's name
        if not os.path.exists(self.basepath + name):
            os.makedirs(self.basepath + name)
        self.path = self.basepath + name + "\\"
        if not os.path.exists(self.path + "data.txt"):
            os.makedirs(self.path + "data.txt")
            self.countTachy = 0
            self.countBrady = 0
            self.countUnevent = 0
        else:
            with open(self.path + "data.txt", 'r') as f:
                string = f.readline()
                string = string.split(" ")
                self.countTachy = int(string[2])
                self.countBrady = int(string[0])
                self.countUnevent = int(string[1])

    def findLast(self, event, date):
        def compare(date1, date2):
            test = date1.split(" ")
            #print("compare splitting: "+str(test))
            test[0] = int(test[0]) - 2016
            test[1] = int(test[1])
            test[2] = int(test[2])
            test[3] = int(test[3])
            test[4] = int(test[4])
            test[5] = int(test[5])
            first = ((((test[0] * 12 + test[1]) * 31 + test[2]) * 24 + test[3]) * 60 + test[4]) * 60 + test[5]
            test = date2.split(" ")
            test[0] = int(test[0]) - 2016
            test[1] = int(test[1])
            test[2] = int(test[2])
            test[3] = int(test[3])
            test[4] = int(test[4])
            test[5] = int(test[5])
            second = ((((test[0] * 12 + test[1]) * 31 + test[2]) * 24 + test[3]) * 60 + test[4]) * 60 + test[5]
            return first - second
        location = 0
        #print ("Start of findLast: "+event+" "+ date)
        if event == "Unevent":
            location = self.countUnevent - 1
        if event == "Tachy":
            location = self.countTachy - 1
        if event == "Brady":
            location = self.countBrady - 1

        if location == -1:
            print ("No Data Found!")
            return
        print("Location: " + str(location)+" count:"+str(self.countUnevent))
         #f = open( self.path+event+'.txt', 'r')
        with open(self.path+event+'.txt', 'r') as f:
            f.seek(location*self.datasize)
            f.seek(location * self.datasize)
            line = f.readline()
            while compare(line,date)>0 and location >= 0:
                f.seek(location * self.datasize)
                line = f.readline()
                print (line,end="")
                location -= 1

    def getrange(self, begin, end):
        def compare(date1, date2):#date1 is younger, > 0
            test = date1.split(" ")
            #for i in test:
                #print ("date1: "+date1[:-1]+" i:"+i)
            test[0] = int(test[0]) - 2016
            test[1] = int(test[1])
            test[2] = int(test[2])
            test[3] = int(test[3])
            test[4] = int(test[4])
            test[5] = int(test[5])
            first = ((((test[0] * 12 + test[1]) * 31 + test[2]) * 24 + test[3]) * 60 + test[4]) * 60 + test[5]
            test = date2.split(" ")
            if test == '':
                return -1
            test[0] = int(test[0]) - 2016
            test[1] = int(test[1])
            test[2] = int(test[2])
            test[3] = int(test[3])
            test[4] = int(test[4])
            test[5] = int(test[5])
            second = ((((test[0] * 12 + test[1]) * 31 + test[2]) * 24 + test[3]) * 60 + test[4]) * 60 + test[5]
            return first - second
            #date1 is sooner, > 0
        def output(date, string):# create output function
            print(date[:-1] +" "+string )
        def merge(path, datasize, spots, compare, output):
            try:
                fb = open(path + "Brady.txt", 'r')
                fu = open(path + "Unevent.txt", 'r')
                ft = open(path + "Tachy.txt", 'r')
                fb.seek(spots[0][1] * datasize)
                brady = fb.readline()
                fu.seek(spots[1][1] * datasize)
                unevent = fu.readline()
                ft.seek(spots[2][1] * datasize)
                tachy = ft.readline()
                while spots[0][1] - spots[0][0] != 0 or spots[1][0] - spots[1][1] != 0 or spots[2][1] - \
                        spots[2][0] != 0:
                    #print("marker: " + str(spots[0][1] - spots[0][0]))
                    if compare(brady, unevent) >= 0:
                        if compare(brady, tachy) >= 0 and spots[0][1] - spots[0][0]!=0:
                            output(brady, "B")
                            spots[0][1] -= 1
                            fb.seek(spots[0][1] * datasize)
                            brady = fb.readline()
                        elif spots[2][1] - spots[2][0]!=0:
                            output(tachy, "T")
                            spots[2][1] -= 1
                            ft.seek(spots[2][1] * datasize)
                            tachy = ft.readline()
                    else:
                        if compare(unevent, tachy) >= 0 and spots[1][1] - spots[1][0]!=0:
                            output(unevent, "U")
                            #print("spots: "+str(spots[1][1]))
                            spots[1][1] -= 1
                            fu.seek(spots[1][1] * datasize)
                            unevent = fu.readline()
                        elif spots[2][1] - spots[2][0]!=0:
                            output(tachy, "T")
                            spots[2][1] -= 1
                            ft.seek(spots[2][1] * datasize)
                            tachy = ft.readline()

                ft.close()
                fu.close()
                fb.close()
            except IOError:
                print ("ERROR!: While merging: unable to open files!")
        def seek(f, high, datasize, value, compare):
            low = 0
            f.seek(low * datasize)
            testval = f.readline()
            if compare(testval, value) == 0:
                return low
            f.seek(high * datasize)
            testval = f.readline()
            if compare(testval, value) == 0:
                return high
            testloc = int((high - low) / 2)+low
            while high - testloc > 1 and testloc - low > 1:
                f.seek(testloc * datasize)
                testval = f.readline()
                #print("testval: "+testval+" value:" +value)
                if compare(testval, value) == 0:  # found the value
                    #print("found value")
                    break
                elif compare(testval, value) < 0:
                    low = testloc
                    testloc = int((high - low) / 2)+low
                else:  # value > test
                    high = testloc
                    testloc = int((high - low) / 2)+low
                #print("high: " + str(high) + " low:" + str(low) + " testloc:" + str(testloc))
            return testloc
        # find seek spots for brady

        with open(self.path + "Brady.txt", 'r') as f:
            a = seek(f, self.countBrady - 1, self.datasize, begin, compare)
            b = seek(f, self.countBrady - 1, self.datasize, end, compare)
        # find seek spots for unevent
        with open(self.path + "Unevent.txt", 'r') as f:
            c = seek(f, self.countUnevent - 1, self.datasize, begin, compare)
            d = seek(f, self.countUnevent - 1, self.datasize, end, compare)
        # find seek spots for tachy
        with open(self.path + "Tachy.txt", 'r') as f:
            e = seek(f, self.countTachy - 1, self.datasize, begin, compare)
            f = seek(f, self.countTachy - 1, self.datasize, end, compare)
        spots = [[a, b], [c, d], [e, f]]
        # 3 way merge with brady, unevent, tachy
        # piped into the blocking queue of another function
        merge(self.path, self.datasize, spots, compare, output)

    def addEvent(self, event, date):
        try:
            f = open(self.path + event + '.txt', 'a+')
            f.write(date + '\n')
        except IOError:
            return "IOError! Could Not Open File!"
        finally:
            f.close()
        if event == "Unevent":
            self.countUnevent += 1
        if event == "Tachy":
            self.countTachy += 1
        if event == "Brady":
            self.countBrady += 1
        return 0


# '2016 01 01 24 59 59\n'
# 'YYYY MM DD HH MM SS\n'
# '123456789012345678901' = 21
# print (time.strftime('%Y %m %d %H %M %S'))

bob = DataCollection("Bob")
bob.getrange("2016 06 17 19 25 11","2016 06 17 19 31 40")

