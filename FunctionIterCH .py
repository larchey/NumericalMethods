import string
from math import*
import cmath

def main():
    f=input("Input a function of x")
    n=int(input("Enter an integer n, the number of iterates you wish to compute:"))
    x=eval(input("Input a real number x, the function input:"))
    print("The first",n,"iterates of","f(x)=",f,"at x=", x,"are:")
    for i in range(n):

        print("f^",i+1,"(",x,")=",eval(f))
        x=eval(f)
        print()     

main()
