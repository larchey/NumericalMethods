def subset(a):
    a=list(a);
    k = len(a);
    n=len(a);

    while (k>= 1 and a[k-1]=="1"):
        k-=1;
    
    if(k>=1):
        a[k-1]="1"
        print(*a);
        
        for j in range(k,n):
            a[j]=0;
            print(*a)
        print("The next subset is ",*a)
        
    else:
        print("This string contains all 1's");
    


print("Charley Hoffmann Next Subset Algorithm");
a=str(input("Enter a string of 1's and 0's(ex. '1110011') "));
subset(a);
