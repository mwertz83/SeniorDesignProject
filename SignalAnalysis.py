import urllib.request


BEGIN_VALUE = -75
next_value = BEGIN_VALUE*1.
prev_value = next_value
file_seek = 0
f = open("Data.txt",'r')
f.seek(file_seek)
filter_limit = -100.
peak = 0
start = 0
next = 0
last_value=0.
spam = 150

def Uannounce(peak,next,start):
    print ("Peak! "+str(peak)+" change:"+str(next-start))
def Bannounce(peak,next,start):
    print ("Brady! "+str(peak)+" change:"+str(next-start))
def Tannounce(peak,next,start):
    print ("Tachy! "+str(peak)+" change:"+str(next-start))

with urllib.request.urlopen('http://76.184.112.40:8280/tachy.csv') as f:
    for line in f:
        measure = str(line).split(",")[1]
        #print("Measure:" + measure)
        next+=1
        value = float(measure)*1000
        if last_value == peak:
            pass
        else:
            if value <= peak and peak > filter_limit and peak >= last_value and value > filter_limit:
                if next - start < 150:
                    Tannounce(value, next, start)
                    spam = 10
                else:
                    Uannounce(peak,next,start)
                    spam = 10
                start=next

        if next - start > 600:
            if spam > 149:
                Bannounce(value, next, start)
                spam =0
            else:
                spam+=1
        if value > filter_limit:
            last_value = peak
            peak=value
        next_value = next_value*.9 + value*.1
        filter_limit = next_value*2 - prev_value + 200
        prev_value = next_value
        #print (filter_limit)