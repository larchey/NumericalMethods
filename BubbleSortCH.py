def Bubble(a):

    for j in range(len(a)-1):
        for k in range(len(a)-1,j,-1):
            print("j=",j,"k=",k);
            if(a[k]<a[k-1]):
                temp=a[k];
                a[k]=a[k-1];
                a[k-1]=temp;
                print(*a);
            else:
                print("a*");
            
    
    print("Final sorted string", *a, "  n =",len(a));

print("Charlie Hoffmann BubbleSort");
a=eval(input("Enter a list of numbers(ex. '[1,5,3,7,4]') "));
Bubble(a);
