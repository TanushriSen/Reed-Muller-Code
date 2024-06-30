'''Given a message, encode using Reed-Muller, impose some errors and decode that errored message using 
walsh Transform'''

#input
n=int(input("Enter length of the message: "))
message=input("Enter the message in binary: ")
if(len(message)!=n):
    print("Invalid Message")
    exit()
#print("Given message: ",message)
p=float(input("Enter error probability: "))
#print("Given error probability: ",p)


#encode the message using Reed-Muller of order 1 (i.e., ;inear function)
def Encode(msg):
    codeword=''
    for i in range(2**(n-1)):
        x=str(format(i, '0{}b'.format(n-1)))
        f=int(msg[n-1])
        for j in range(len(x)):
            f=(int(int(x[j])*int(msg[j]))+f)%2
        #print(x,' ',f)
        codeword+=str(f)
    return codeword

codeword=Encode(message)
print("codeword: ",codeword)

#imposing some errors
import random
flip_num=int(p*(2**n))
def Noise(codeword,flip_num):
   
    flip_indices=random.sample(range(len(codeword)),min(flip_num,len(codeword)))
    #print(flip_indices)
    errored_msg=list(codeword)
    for index in flip_indices:
        errored_msg[index]='1' if codeword[index]=='0' else '0'
    
    return ''.join(errored_msg)


err_codeword=Noise(codeword,flip_num)
print("After some bit flips new codeword: ",err_codeword)


#finding walsh spectrum values using Fast Walsh Transform
def fast_walsh(f):
    n = len(f)
    walsh=[]
    for i in range(n):
        walsh.append((-1)**int(f[i]))
    
    h = 1
    while h < n:
        for i in range(0, n, h*2 ):
            for j in range(i, i + h):
                x = walsh[j]
                y = walsh[j + h]
                walsh[j] = x + y
                walsh[j + h] = x - y
        h *= 2
    print("Walsh spectrum values: ",walsh)
    return walsh



#Decode using Walsh Transform
import math
def decode(codeword):
    walsh=fast_walsh(codeword)
    #take maximum among walsh spectrum values, that will give the corresponding codeword
    maximum=max(abs(x) for x in walsh)
    print("Max walsh spectrum value: ",maximum)
    print("Distance of codeword from a linear codeword is: ",0.5*(len(codeword)-maximum))

#finding the codewordS

    count=walsh.count(maximum)
    if count>1:
        print("Can not decoded the message")
        exit()
    else:
        i=walsh.index(maximum)
        n=int(math.log2((len(walsh))))
        decoded=str(format(i, '0{}b'.format(n)))
        if walsh[i]>0:
            decoded+='0'
        else:
            decoded+='1'
    return decoded

print("\nRequired decoded codeword from errored message: ",decode(err_codeword))
    




  