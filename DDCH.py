#Charley Hoffmann
#DividedDifference.py 
#Graphing commands for students.
#Goal: Enter data, graph the data.
#Compute the Lagrange polynomial and graph it.


import string
import math
from tkinter import *
from graphics import *



def getheading():
    print ("Divided Difference Interpolatory Polynomial by Charley Hoffmann")
    print("This program has the user enter data points.")
    print("It computes the Lagrange Polynomial through those points")
    print ("and graphs the points and the polynomial.")
    print()


def enterPoints():
    n=int(input("Enter the number of points: ")) 
    abscissa=[]
    ordinate=[]
    print ("Enter the x,y coordinates, separated by a comma.")
    for i in range(n):
        print ("Point ", i,":",end="  ")
        x,y=eval(input("  "))
        abscissa.append(x)
        ordinate.append(y)
    return n,abscissa, ordinate

def coordsystemSize(abscissa,ordinate):
    xmin=min(abscissa)
    xmax=max(abscissa)
    delx=xmax-xmin
    ymin=min(ordinate)
    ymax=max(ordinate)
    dely=ymax-ymin
    winxmin=xmin-0.025*delx
    winxmax=xmax+0.025*delx
    winymin=ymin-2*dely    #Change if function goes off window
    winymax=ymax+2*dely
    return xmin,xmax,delx,ymin,ymax,dely,winxmin,winxmax,winymin,winymax

def makeWin(width,height,winxmin,winxmax,winymin,winymax):
    win=GraphWin("Lagrange-Charley Hoffmann",width,height)
    win.setCoords(winxmin,winymin,winxmax,winymax)
    win.setBackground("ivory")
    return win


def makeAxes(winxmin,winxmax,winymin,winymax,win):
 
    ptx1=Point(winxmin,0)
    ptx2=Point(winxmax,0)
    shape=Line(ptx1,ptx2)
    shape.draw(win)
    
    pty1=Point(0,winymin)
    pty2=Point(0,winymax)
    shape=Line(pty1,pty2)
    shape.draw(win)

def plotPoints(n,abscissa,ordinate,win):
    for i in range(n):
        pt=Point(abscissa[i],ordinate[i])
        pt.setOutline("red3")
        pt.draw(win)

def getInputs(xmin,xmax):
    print (" " )
    print ("Enter the number of subintervals on which to evaluate the function.  The more subintervals, the more accurate the graph.")
    n=int(input("Enter the number of subintervals: "))   
    print (" ")
    deltax=(xmax-xmin)/n
    return n,deltax

def evalFunction(n,xmin,deltax,f):
    abscissa=[]
    ordinate=[]
    for i in range(n+1):
        x=xmin+i*deltax
        y=eval(f)
        abscissa.append(x)
        ordinate.append(y)
    return abscissa,ordinate

def plotFunction(n,abscissa,ordinate,win):
    for i in range(n):
       pt1=Point(abscissa[i],ordinate[i])
       pt2=Point(abscissa[i+1],ordinate[i+1])
       shape=Line(pt1,pt2)
       shape.draw(win) 
def another(LP):
    a=input("Do you want to evaluate the function at a point? yes/no   ")
    if(a=="yes"or a=="Yes"):
        x=eval(input("Enter the x-value:   "))
        z=eval(LP)
        print("LP(",x,")=",z)
        another(LP)
    else:
        return

def zeroMat(n):
    mat = []
    for i in range(n):
        rowList = []
        for j in range(n+1):            
            rowList.append(0)
        mat.append(rowList)

    return mat

def matInputs(n,ddmat,abscissa,ordinate):
    for i in range(n):
        ddmat[i][0]=abscissa[i]
        ddmat[i][1]=ordinate[i]
    return ddmat





def showMat(n,ddmat):
    for i in range(n):
        print(ddmat[i])

def fillDDmat(n,ddmat):
    for j in range(1, n):
        for i in range(1,n-(j-1)):
            y2=ddmat[i][j]
            y1=ddmat[i-1][j]
            x1=ddmat[i-j+j-1][0]
            x2=ddmat[i+j-1][0]
            
            ddmat[i-1][j+1] = float(y2-y1)/float(x2-x1)
      
    return ddmat

    
def main():
    getheading()
   
    #Enter the points         
    n,abscissa, ordinate = enterPoints()
    #Zero the matrix
    ddmat=zeroMat(n)
    print ("The matrix of zeros is ")
    showMat(n,ddmat)
    print()
    #Put the x and y coordinates in the first 2 columns of the matrix.
    ddmat=matInputs(n,ddmat,abscissa,ordinate)
    print("The matrix with x-y in first columns is ")
    
    showMat(n,ddmat)
    print()
    ddmat=fillDDmat(n,ddmat)
    print("The divided difference matrix is ")
    showMat(n,ddmat)
    print()
    for i in range (n):
        ordinate[i]=ddmat[0][i+1]
    print("Coefficient list is",ordinate)
    print("Abscisssa  list is",abscissa)

    #Compute the size of the graphing window as 1.05*(xmax-xmin) and 3*(ymax-ymin)
    xmin,xmax,delx,ymin,ymax,dely,winxmin,winxmax,winymin,winymax=coordsystemSize(abscissa,ordinate)

    #a will be the pixel size of the python graph window.
    a=1200
    width = a
    height = a

    win=makeWin(width,height,winxmin,winxmax,winymin,winymax)

    #Draw the axes, which won't always appear dependent on points used.
    makeAxes(winxmin,winxmax,winymin,winymax,win)
    
    #Plot the points
    plotPoints(n,abscissa, ordinate,win)
    LP=""
    
    for k in range(n):
        currx=abscissa[k]
        curry=ordinate[k]
        LP=LP+"+"+str(curry)+"*1"
        i=0
        while i<k:
            LP=LP+"*(x-"+str(abscissa[i])+")"
            i=i+1
        print("LP is now", LP)
        
    print()
    print ("The Newton's divided difference interpolating polynomial =", LP)
    x=3
    z=eval(LP)
    print("LP(",3,")=",z)
    x=4
    z=eval(LP)
    print("LP(",4,")=",z)
    x=6
    z=eval(LP)
    print("LP(",6,")=",z)
    x=9
    z=eval(LP)
    print("LP(",9,")=",z)
    x=12
    z=eval(LP)
    print("LP(",12,")=",z)
    x=14
    z=eval(LP)
    print("LP(",14,")=",z)
    x=18
    z=eval(LP)
    print("LP(",18,")=",z)




    print()    
    print ("The Lagrange Polynomial LP(x)=", LP)

    
    #Input number of subintervals.  Compute delta x.
    n,deltax=getInputs(xmin,xmax)
    
    #Compute the abscissas (x-coordinates) and ordinates (function values)
    abscissa,ordinate=evalFunction(n,xmin,deltax,LP)   
    
    #Plot the piecewise linear approximation.
    plotFunction(n,abscissa,ordinate,win)
    
    another(LP)
    print (" ")
 
main()
 
 
