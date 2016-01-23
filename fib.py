# Implementations done in Python since it natively supports unbounded integer
#   arithmetic and fractional math

#Compiled with Python 2.7.3 (default, Apr 10 2012, 23:31:26) [MSC v.1500 32 bit (Intel)] on win32
#in IDLE version 2.7.3

#For profiling (written in C to avoid overhead)
import cProfile
# to deal with fractions
from fractions import Fraction

global called
global countAdd
global countSub
global countMult
called = 0
countAdd = 0
countSub = 0
countMult = 0

#Recursive implementation based on text
def fibonacci(n, count = False):
    global called
    global countAdd
    global countSub
    global countMult
    if count == True:
        called += 1

    if n<=2:
        return 1
    else:
        if count == True:
            countAdd += 1
            countSub += 2 

        return fibonacci(n-1, count)+fibonacci(n-2, count)
'''
For n = 10:
Counts 54 additions vs 52 predicted (not sure why?)
Counts 108 Subtractions vs 104 predicted (not sure why?)
109 Calls implying 55 calls of cost zero
Implementation is Robust (no possibility of rounding error)
    & unbounded integer arithmetic in python
Implementation is very slow for n > 60 (because of the
    many duplicated recursive calls, as shown in the trie
    from Q4); with count = True it is slow for n > 40)
It will also fail completely because of the limit
    on recursion (of course, any implementation will
    eventually unless storage can grow faster than required
    memory)
'''

#Loop implementation (differs slightly from design to be more storage efficient)
def fibLoop(n, count = False):
    global called
    global countAdd
    global countSub
    global countMult
    fib1 = 1
    fib2 = 1
    for i in range(2,n):
        if count == True:
            countAdd += 1
        
        newfib = fib1 + fib2
        fib1 = fib2
        fib2 = newfib
    return fib2
'''
For n = 10:
Counts 8 additions, as predicted
Counts 0 Subtractions vs 16 predicted, since we didn't use
    a list, but it performs additional 16 assignments instead
Implementation is Robust (no possibility of rounding error)
    & unbounded integer arithmetic in python
n = 100,000 --> 0.166 seconds
n = 1,000,000 --> 14.028 seconds

'''

#Direct implementation subject to rounding errors for n > 71
def fibDirect(n, count = False):
    global called
    global countAdd
    global countSub
    global countMult
    rFive = (5**0.5)

    if count == True:
        countMult += 2*(n-1) + 2 #uses Naive assumption for how
        countSub += 2               # power function works
        countAdd += 1
    
    c = 1/rFive
    a = ((1+rFive)/2)**n
    b = ((1-rFive)/2)**n
    return int(c*(a-b))
'''
For n = 10:
Counts 1 addition, as predicted
Counts 2 Subtractions as predicted
Counts 20 Multiplications as predicted (but this is based on a
    Naive assumption of how exponentiation is implemented
Implementation is NOT Robust; we start getting rounding error
    at n = 72
Since it is not robust, and the results we are interested in are
    exact integers, it isn't really relevent when it fails (i.e
    it is unreliable for n > 71)
Maybe if we were interested in ratios, we could still use it
    (but why bother since there are better methods?)
Fails for n > 1475 --> Overflow
    Python only supports unbounded *integer* arithmetic :)
'''

# Robust Direct implementation (uses helper functions below)
def betterFibDirect(n, count = False):
    global called
    global countAdd
    global countSub
    global countMult
    if count == True:
        countSub += 1
    
    a = rFivePow((Fraction(1,2),Fraction(1,2)),n, count)
    b = rFivePow((Fraction(1,2),Fraction(-1,2)),n, count)
    return int(a[1]-b[1])
'''
For n = 10:
Counts 36 additions (no prediction)
Counts 1 Subtraction (no prediction)
Counts 90 Multiplications (no prediction) - based on Naive expmentiation
    but these are fractional multiplications 
Implementation is Robust! Since there no possibility of rounding error
    because we are dealing with only integers (and fractions)
n = 100,000 --> 69.411 seconds
n = 1,000,000 --> > 20 minutes
    This is as far as I'm willing to go with this one, but I don't think
    it will actually fail until we run out of memory, but it does get slower
    and slower because of the multiplication of large numbers
Also: see NOTE after the next function
'''

# Robust Direct implementation (uses helper functions below)
# cuts our multiplications and additions in two
# I forgot to do this in the first implementation: D'Oh!
def muchBetterFibDirect(n, count = False):  
    global called
    global countAdd
    global countSub
    global countMult
    if count == True:
        countSub += 1
    
    a = rFivePow((Fraction(1,2),Fraction(1,2)),n, count)
    b = a[0],-a[1]   ## Altered Line
    return int(a[1]-b[1])
'''
For n = 10:
Counts 18 additions as predicted
Counts 1 Subtraction as before
Counts 45 Multiplications as predicted
    but these are fractional multiplications 
Implementation is Robust! Since there is no possibility of rounding
    error because we are dealing with only integers (and fractions)
n = 100,000 --> 37.039 seconds
NOTE: We should be able to make this implementation much better
by implementing exponentiation in a smarter way, but it will
probably only compete with fibLoop if we implement a table
to look up our exponents, in which case we might as well store
the fibonacci numbers themselves... unless we want to compute
other fibonacci-like sequences easily... 
'''


# A better recursive implementation that avoids duplication of labour
def betterFibonacci(n, count = False):
    global called
    global countAdd
    global countSub
    global countMult
    if count == True:
        called += 1
    if n<=2:
        return (1,1)
    else:
        if count == True:
            countAdd += 1
            countSub += 1
            
        
        pair = betterFibonacci(n-1, count)
        return (pair[1],pair[0]+pair[1])
'''
For n = 10:
Counts 8 additions, as expected (see the graph in Q4)
Counts 8 Subtractions, as expected
9 calls as expected (vs 109 for the Naive implementation)
Implementation is Robust, since there no possibility of rounding error
Fails for n > 991 --> Maximum Recursion depth exceeded
    This is a python consideration to protect from catasrophic
    failure (likely our Naive implementation would also fail here
    if not a little earlier, but I don't have time to wait for that)
'''
    
###########################################################
#                   HELPER FUNCTIONS                      #
###########################################################
# Exact multiplication for numbers of the form x+y*sqrt(5)
def rFiveMult(n,m, count = False):
    global called
    global countAdd
    global countSub
    global countMult
    if count == True:
        countMult += 5
        countAdd += 2
    return (m[0]*n[0]+m[1]*n[1]*5,m[0]*n[1]+m[1]*n[0])

# Naive power function for numbers of the form x+y*sqrt(5)
def rFivePow(x,n, count = False):
    global called
    global countAdd
    global countSub
    global countMult
    result = x
    for i in range(1,n):
        result = rFiveMult(x,result, count)
    return result

# Reset the global counters
def resetCount():
    global called
    global countAdd
    global countSub
    global countMult
    called = 0
    countAdd = 0
    countSub = 0
    countMult = 0

def printResults(n):
    global called
    global countAdd
    global countSub
    global countMult
    print(n)
    print ("\n")
    print("Additions:  " + str(countAdd))
    print("Subtractions:  " + str(countSub))
    print ("Multiplications:  " + str(countMult))
    print ("Calls:  " + str(called))
    resetCount()
           

if __name__ == "__main__":
    done = False
    while not done:
        resetCount()
        n = input("Enter a non-negative integer: ")
        print ("\n")
        
        #'''    Remove # before and after blocks to comment out
        print("fibonacci("+str(n) + ") = ")
        printResults(fibonacci(n, True))
        cProfile.run('fibonacci(n)')
        #'''

        #'''
        print("fibLoop("+str(n) + ") = ")
        printResults(fibLoop(n, True))
        cProfile.run('fibLoop(n)')
        #'''
        
        #'''
        print("fibDirect("+str(n) + ") = ")
        printResults(fibDirect(n, True))
        cProfile.run('fibDirect(n)')
        #'''
        
        ''' # replaced with muchBetterFibDirect
        print("betterFibDirect("+str(n) + ") = ")
        printResults(betterFibDirect(n, True))
        cProfile.run('betterFibDirect(n)')
        '''

        #'''
        print("muchBetterFibDirect("+str(n) + ") = ")
        printResults(muchBetterFibDirect(n, True))
        cProfile.run('muchBetterFibDirect(n)')
        #'''

        #'''
        print("betterFibonacci("+str(n) + ") = ")
        printResults(betterFibonacci(n, True)[1])
        cProfile.run('betterFibonacci(n)')
        #'''
     

        print ("\n")
        s = raw_input("Exit? Y/N ").lower()
        if s == 'y':
            done = True








     
        
