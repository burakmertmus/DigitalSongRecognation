#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Burak Mert Muş
#
#
# Copyright:   (c) Burak Mert Muş 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from peaks import peakMatris
import os

for i in os.walk("C:/Users/Burak Mert Muş/Desktop/phy/wavDB"):
    ##oran=fingerprint("'" +i[2][2]+"'",sample)
    print(i)
    print(len(i[2]))
for j in range(0,len(i[2]),1):
    print("--------------")
    matrixSM=peakMatris("C:/Users/Burak Mert Muş/Desktop/phy/wavDB/"+i[2][j].split('.')[0]+".wav")

    dosya=open("C:/Users/Burak Mert Muş/Desktop/phy/textDB/"+i[2][j].split('.')[0]+".txt", "w")
    k=0
    for k in range(0,len(matrixSM),1):
        dosya.write(str(matrixSM[k][0])+","+str(matrixSM[k][1])+"\n")
    dosya.close()

