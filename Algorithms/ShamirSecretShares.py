import numpy as np
import random as rand

N=9 #Number of shares of a secret
K=3 #Minimum number of shares required to view the secret
S=int(input("Enter your secret:")) #The secret


def main():
    coefficientVec=np.zeros(K) #Stores the coefficients of the polynoomial in increasing order of degree of x
    secretSharesVec=np.zeros((N,2)) #Stores the secrets generated
    knownSharesVec=np.zeros((K,2)) #Stores the known secrets
    coefficientVec[0]=S #The constant term of the polynomial contains the secret
    initializeCoefficients(coefficientVec)
    createShares(secretSharesVec,coefficientVec)
    displayShares(secretSharesVec)
    getKnownShares(knownSharesVec)
    print(aggregateShares(knownSharesVec))


#initialize the coefficients to some random values
def initializeCoefficients(coefficientVec):
    for i in range(1,K):
        coefficientVec[i]=rand.randint(1,1000)


#Creates shares using the coefficients
#The shares are the x and y values of the polynomial generated using the coefficient vector
def createShares(secretSharesVec,coefficentVec):
    for i in range(N):
        x=i+1 #The x value ranges from 1 to n
        secretSharesVec[i,0]=x
        temp=1
        y=0
        for j in range(K):
            y=y+temp*coefficentVec[j]
            temp=temp*x
        secretSharesVec[i,1]=y


#displays the shares
def displayShares(secretSharesVec):
    for i in range(N):
        print(secretSharesVec[i,0],secretSharesVec[i,1])


#Input known shares
def getKnownShares(knownSharesVec):
    for i in range(K):
        knownSharesVec[i,0]=input("Enter x{}:".format(i))
        knownSharesVec[i,1]=input("Enter y{}:".format(i))



#Finds the secret using K known shares
#Uses lagrange interpolation to find only the constant term of the polynomial(which is the secret) using K known shares(points/coordinates)
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