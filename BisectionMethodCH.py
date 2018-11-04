import string
from math import*
import cmath

def bis(f,a,b,t,i):
    print("Search interval",i,"is[",a,",",b,"]");
    m=(a+b)/2;
    x=m;
    fm=eval(f);
    print("f(midpoint)=f(",m,")=",fm);
    x=a;
    fa=eval(f);
    x=b;
    fb=eval(f);
    if(fa==0):
        print("Interval is 0 at ",fa);
    if(fb==0):
        print("Interval is 0 at ",fb);
    if(fm==0):
        print("The approximation to the root is f(",m,")=",fm);
    elif(abs(fm)<t):
        print("Tolerance reached, interval is [",a,",",b,"]");
    elif(fa*fm<0):
        i+=1;
        bis(f,a,m,t,i);
        
    elif(fb*fm<0):
        i+=1;
        bis(f,m,b,t,i);
        
         



i=1;
print("Charlie Hoffmann BisectionMethod");
f=input("Input a function of x: ")
a=eval(input("Left Endpoint: "))
b=eval(input("Right Endpoint: "))
t=float(input("Tolerance: "))
bis(f,a,b,t,i)
