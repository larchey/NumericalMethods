import string
from math import*
import cmath

def right(f,a,b,n):
    h=(max(a,b)-min(a,b))/n
    total=0
    for n in range(1,n+1):
        x=a+n*h
        total=total+eval(f)
    return total*h


    
def left(f,a,b,n):
    h=(max(a,b)-min(a,b))/n
    total=0
    for n in range(0,n):
        x=a+n*h
        total=total+eval(f)
        
    return total*h



def trap(f,a,b,n):
    h=(max(a,b)-min(a,b))/n
    total=0
    for n in range(0,n):
        x=a+n*h
        y0=eval(f)
        x=a+(n+1)*h
        y1=eval(f)
        total=total+((h/2)*(y0+y1))
        
    return total



def simpsons(f,a,b,n):
    if n%2==0:
        h=(max(a,b)-min(a,b))/n
        total=0
        for i in range(0,n+1):
            if i== 0 or i ==n:
                x=a+i*h
                total=total+eval(f)
                
            elif i%2==0:
                x=a+i*h
                total=total+2*eval(f)
                
            else:
                x=a+i*h
                total=total+4*eval(f)
               

        return total*(h/3)
    else:
        return(simpsons(f,a,b,n*2))
    

    




print("Charley Hoffmann Numerical Integration");
f=input("Input a function: ")
a=eval(input("Input the Endpoint A: "))
b=eval(input("Input the Endpoint B: "))
n=eval(input("Input the number of subintervals: "))


print("Right:",right(f,a,b,n))
print("Left:",left(f,a,b,n))
print("Trapezoid:",trap(f,a,b,n))
print("Simpsons:",simpsons(f,a,b,n))


