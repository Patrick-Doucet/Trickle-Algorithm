f = open("test-cases/1024-case.txt", "a")

for i in range(32):
    for j in range(32):
        name = chr(65+i) + chr(65+j)
        f.write(name + ' ' + str(i) + ' ' + str(j) + ' ' + '3' +'\n')

f.close()