from LinkedList import *


BYZANTINE_NODES=5
NON_BYZANTINE_NODES=9


def SquaredDeviation(n):
    k=0
    EX=0
    EXX=0
    while(k<NON_BYZANTINE_NODES):
        EX=EX+n.data
        EXX=EXX+n.data*n.data
        n=n.next
        k=k+1
    return (EX*EX-NON_BYZANTINE_NODES*EXX)
    
def ToleranceRange(l):
    r=0
    i=1
    n=l.head
    SD=SquaredDeviation(n)
    while(i<BYZANTINE_NODES):
        n=n.next
        tempDeviation=SquaredDeviation(n)
        if(SD<tempDeviation):
            SD=tempDeviation
            r=i
        i=i+1
        n=n.next
    return r

l=linkedlist()
l.insert(0)
l.insert(1)
l.insert(10)
l.insert(11)
l.insert(12)
l.insert(13)
l.insert(14)
l.insert(15)
l.insert(16)
l.insert(17)
l.insert(18)
l.insert(19)
l.insert(100)
l.insert(101)
l.insert(110)
l.insert(111)

print(ToleranceRange(l))