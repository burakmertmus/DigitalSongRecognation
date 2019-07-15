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

import os
from peaks import peakMatris
import numpy as np
## İki peak matrisini Kıyaslama kaç adet benzerlik olduğunu bulma
DEFAULT_RECOGNATION_INTERVAL=0.7
def recognationCount(matrix1,matrix2):
    basIndex=0
    maxBenzerlik=0
    while(len(matrix1)>=basIndex+len(matrix2)):
        benzerlik=0
        for i in range(0,len(matrix2),1):
            ##if(matrix1[i+basIndex][0]>=matrix2[i][0]-DEFAULT_RECOGNATION_INTERVAL and matrix1[i+basIndex][0]<=matrix2[i][0]+DEFAULT_RECOGNATION_INTERVAL):
            if(matrix1[i+basIndex][0]==matrix2[i][0]):
                benzerlik=benzerlik+1
        """
        print("O anki bulduğu benzerlik sayısı")
        print(benzerlik)"""
        if maxBenzerlik < benzerlik:
            ##print("Maximum benzerlik değişti")
            ##print("baslangıc indexi "+str(basIndex)+" Orjinal klibin baslangıc saniyesi"+str(matrix1[basIndex][1]))
            maxBenzerlik=benzerlik
        """print(" Ararken şimdiye kadar bulduğu maximum benzerlik sayısı")
        print(" "+str(maxBenzerlik))
        print("Basindex:")
        print(basIndex)
        print("---------------------------------------------------------------")"""
        basIndex=basIndex+1
    return maxBenzerlik

def score(matrixSM,matrixSS):
    durum=recognationCount(matrixSM,matrixSS)
    print(str(durum)+" kadar eşlelme bulundu")
    return durum/len(matrixSS)*100
scoreList=[]
nameList=[]
def textDB():
    ##kıyaslanacak sample
    matrixSS=peakMatris("ercan1_sample.wav")
    print(matrixSS)
    for i in os.walk("C:/Users/Burak Mert Muş/Desktop/phy/textDB"):
        ##oran=fingerprint("'" +i[2][2]+"'",sample)
        print(i)

    for j in range(0,len(i[2]),1):
        print("--------------")
        dosya=open("C:/Users/Burak Mert Muş/Desktop/phy/textDB/"+i[2][j].split('.')[0]+".txt", "r")
        satir=dosya.read()
        textAll = satir.split("\n")
        ##print(len(textAll))
        matrixSM=np.array([[0]*2]*(len(textAll)-1),dtype = float)
        for s in range(0,len(textAll)-1,1):
            matrixSM[s][0] = float(textAll[s].split(",")[0])
            matrixSM[s][1] = float(textAll[s].split(",")[1])
            ##print(str(matrixSM[s][0])+" -- "+str(matrixSM[s][1]))
        scoreList.append(score(matrixSM,matrixSS))
        nameList.append(i[2][j])
        print("sample ve müziğin peak sayıları")
        print(len(matrixSS))
        print(i[2][j])
        print(scoreList[j])
        dosya.close()

textDB()
print("\n\n\n\n")
print("----------------------------")
print("SONUÇ:")
maxIndex=scoreList.index(max(scoreList))
np.set_printoptions(precision=2)
print("En iyi Eşleşme: "+str(scoreList[maxIndex])+" oranı ile "+str(nameList[maxIndex].split('.')[0])+" dosyasıdır.")
print("----------------------------")
