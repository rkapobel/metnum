import csv
import settings

class Data:
    dim = 0
    time = 0
    counter = 0

dataList = []
with open('resultados/complejidad.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    lastDim = 0
    d = Data()
    for row in reader:
        if(row[0] != "n"):
            d.dim = int(row[0])
            d.time += float(row[1])
            d.counter += 1
        
        if d.counter == settings.muestras:
            dataList.append(d)
            d = Data()

with open('promedios/complejidad.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["n"] + ["Time"]);
    for data in dataList:
        writer.writerow([data.dim] + [data.time / settings.muestras])