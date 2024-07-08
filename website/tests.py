from django.test import TestCase
# Create your tests here.

def bytesto(bytes, to, bsize=1024):
    """convert bytes to megabytes, etc and round to nearest integer.
       sample code:
           print('mb= ' + str(bytesto(314575262000000, 'm')))
       sample output: 
           mb= 300002348
    """

    a = {'k' : 1, 'm': 2, 'g' : 3, 't' : 4, 'p' : 5, 'e' : 6 }
    r = float(bytes)
    for i in range(a[to]):
        r = r / bsize
    
    r = round(r)
    return(r)

x = bytesto(3145752600, 'g')
print(x)