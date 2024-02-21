import numpy as np
import random as rand

N=9
K=3
S=int(input("Enter your secret:"))




def main():
    coefficientVec=np.zeros(K)
    secretSharesVec=np.zeros((N,2))
    knownSharesVec=np.zeros((K,2))
    coefficientVec[0]=S
    initializeCoefficients(coefficientVec)
    createShares(secretSharesVec,coefficientVec)
    displayShares(secretSharesVec)
    getKnownShares(knownSharesVec)
    print(aggregateShares(knownSharesVec))


def initializeCoefficients(coefficientVec):
    for i in range(1,K):
        coefficientVec[i]=rand.randint(1,1000)


def createShares(secretSharesVec,coefficentVec):
    for i in range(N):
        x=i+1
        secretSharesVec[i,0]=x
        temp=1
        y=0
        for j in range(K):
            y=y+temp*coefficentVec[j]
            temp=temp*x
        secretSharesVec[i,1]=y

def displayShares(secretSharesVec):
    for i in range(N):
        print(secretSharesVec[i,0],secretSharesVec[i,1])

def getKnownShares(knownSharesVec):
    for i in range(K):
        knownSharesVec[i,0]=input("Enter x{}:".format(i))
        knownSharesVec[i,1]=input("Enter y{}:".format(i))

def aggregateShares(knownSharesVec):
    secret=0
    for i in range(K):
        prod=1
        for j in range(K):
            if(i!=j):
                prod=prod*(-knownSharesVec[j,0])/(knownSharesVec[i,0]-knownSharesVec[j,0])
        secret=secret+knownSharesVec[i,1]*prod
    return secret


main()