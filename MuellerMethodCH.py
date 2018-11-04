import string
from math import*
import cmath

def bis(f,x0,x1,x2,t,i,k):
    x=x0
    fx0=eval(f);
    x=x1
    fx1=eval(f);
    x=x2
    fx2=eval(f);
    h1 =x1-x0
    h2=x2-x1
    p1=(fx1-fx0)/h1
    p2=(fx2-fx1)/h2
    d=(p2-p1)/(h2+h1)

    while i<k:
        b=p2+h2*d
        D=((b**2)-4*fx2*d)**.5
        if abs(b-D)<abs(b+d):
            E=b+D
        else:
            E=b-D
        h=(-2*fx2)/E
        p=x2+h
        if abs(h)<t:
            x=p
            fp=eval(f)
            print("Approximation to the root is f(",p,")=",fp)
            return
        x0=x1
        x1=x2
        x2=p
        h1=x1-x0
        h2=x2-x1
        x=x0
        fx0=eval(f);
        x=x1
        fx1=eval(f);
        x=x2
        fx2=eval(f);
        p1=(fx1-fx0)/h1
        p2=(fx2-fx1)/h2
        d=(p2-p1)/(h2+h1)
        x=p
        fp=eval(f)
        print(i,": estimate to the root is f(",p,")=",fp)
        i=i+1
        
    
         


i=0;
k=1000
print("Charlie Hoffmann MuellerMethod");
f=input("Input a function of x: ")
a=eval(input("First Estimate: "))
b=eval(input("Second Estimate: "))
c=eval(input("Third Estimate: "))
t=float(input("Tolerance: "))
print("The initial estimates to the root are:\n")
x=a
fa=eval(f);
print("f(",a,")=",fa,"\n")
x=b
fb=eval(f);
print("f(",b,")=",fb,"\n")
x=c
fc=eval(f);
print("f(",c,")=",fc,"\n")
bis(f,a,b,c,t,i,k)
