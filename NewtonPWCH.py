import string
from math import*
import cmath

def newton(f, df, x, tol):
    i=0
    while True:
        
        fx=eval(f)
        dfx=eval(df)
        print(fx,dfx)
        x1 = x - (fx/dfx)

        t = abs(x1-x)

        if t < tol:
            break
        print("Estimate to the root",i,"is",x)
        x = x1
        fx1=eval(f)
        print("f(p)=f(",x1,")=",fx1,"\n") 
        i+=1
    print("The approximation to the root is f(",x,")=",fx,"")
    




print("Charley Hoffmann NewtonsMethod");
f=input("Input a function of x where x<=a: ")
df=input("Input the derivative a function of x where x<=a: ")
g=input("Input a function of x where x>a: ")
dg=input("Input the derivative a function of x where x>a: ")
o=eval(input("Input the original estimate to the root of the function: "))
tol=float(input("Tolerance: "))
newton(f, df, o, tol)
newton(g, dg, o, tol)


