import math 

def base(number, base):
    k=len(number)-1
    
    num=0
    for i in number:
       
        num=num+(int(i)*(base**k))
        k=k-1
        
    return num

y=input("Enter a number to be converted")
z=eval(input("Enter the base"))
x=base(y,z)
print(x)
