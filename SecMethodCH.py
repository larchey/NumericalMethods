import string
from math import*
import cmath

def bis(f,a,b,t,i):
    print("Search interval",i,"is[",a,",",b,"]");
    t=t;
    x0=a
    x1=b
    x=x0
    fx0=eval(f);
    x=x1
    fx1=eval(f);
    x2 = x1-((fx1*(x1-x0)*1.0)/(fx1-fx0))
    x=x2;
    bi=eval(f);
    print("f(p)=f(",x2,")=",bi);
    i=i+1;
    if(abs(x2-b)<=t):
        print("The approximation to the root is f(",x2,")=",bi);
    elif(abs(x2-b)>t):
        bis(f,x1,x2,t,i);
    
         



i=0;
print("Charley Hoffmann SecantMethod");
f=input("Input a function of x: ")
a=eval(input("Left Endpoint: "))
b=eval(input("Right Endpoint: "))
t=float(input("Tolerance: "))
bis(f,a,b,t,i)
