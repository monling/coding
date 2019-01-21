import time
lineLength = 20
delaySeconds = 1.05
frontSymbol = '='
frontSymbol2 = ['—', '\\', '|', '/']
backSymbol  = ' '

for i in range(10):
    lineTmpla = "{:%s<%s} {} {:<2}"%(backSymbol, lineLength)
    for j in range(lineLength):
        tmpSymbol = frontSymbol2[j%(len(frontSymbol2))]
        print("\r" + lineTmpla.format(frontSymbol * j, tmpSymbol, j), end='')
        time.sleep(delaySeconds)

