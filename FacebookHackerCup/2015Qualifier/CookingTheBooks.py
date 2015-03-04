# Facebook Hacker Cup 2015 Qualification Round
# Problem 15: Cooking the Books

import argparse
from Tkinter import Tk

def get_file_name():
    parser = argparse.ArgumentParser()
    parser.add_argument("fileName")
    args = parser.parse_args()
    
    file_name = args.fileName
    return file_name

# easy algorithm for this problem:
# One way would be to just generate all swaps, and take the largest/smallest (smallest nonzero first number)
# A perhaps more complicated way, generate swaps from the front until you can't swap anymore.
# The algorithm I'm going with?  For small, find the smallest nonzero digit, and swap element 1 with that

def get_smallest_transposed_fail(original_number):
    #print "Looking for smallest for original: ", original_number
    digits = map(str, str(original_number))
    smallest_position = 0;
    for i in range(1,len(digits)):
        if digits[i] != '0':
            if digits[i] < digits[smallest_position]:
                #print "found smaller -",digits[i]
                smallest_position = i

    digits[0],digits[smallest_position] = digits[smallest_position],digits[0]
    #print digits
    
    return ''.join(digits)

def get_smallest_transposed(original_number):
    #print "Looking for smallest for original: ", original_number
    digits = map(str, str(original_number))
    tobeswapped = 0
    smaller = 0
    for i in range(0,len(digits)):
        #print "base examining",i,"digit = ",digits[i]
        tobeswapped = i
        smaller = i
        found = False
        for j in range(i+1,len(digits)):
            #print "swap candidate",j," digit = ",digits[j]
            if digits[j] != '0':
                if digits[j] < digits[smaller]:
                    #print "found smaller -",digits[j]
                    smaller = j
                    found = True
                    #break
        if found:
            break
    if found:
        digits[tobeswapped],digits[smaller] = digits[smaller],digits[tobeswapped]
    #print digits
    
    return ''.join(digits)

def get_largest_transposed_fail(original_number):
    #print "Looking for largest for original: ", original_number
    digits = map(str, str(original_number))
    largest_position = 0;
    for i in range(1,len(digits)):
        if digits[i] > digits[largest_position]:
            #print "found larger -",digits[i]
            largest_position = i

    digits[0],digits[largest_position] = digits[largest_position],digits[0]
    #print digits
    
    return ''.join(digits)

def get_largest_transposed(original_number):
    #print "Looking for largest for original: ", original_number
    digits = map(str, str(original_number))
    tobeswapped = 0
    larger = 0
    for i in range(0,len(digits)):
        #print "base examining",i,"digit = ",digits[i]
        tobeswapped = i
        larger = i
        found = False
        for j in range(i+1,len(digits)):
            #print "swap candidate",j," digit = ",digits[j]
            if digits[j] > digits[larger]:
                #print "found larger -",digits[j]
                larger = j
                found = True
                #break
        if found:
            break
    if found:
        digits[tobeswapped],digits[larger] = digits[larger],digits[tobeswapped]
    #print digits
    
    return ''.join(digits)

file_name = get_file_name()
infile = open(file_name)

answer = Tk()
answer.withdraw()
answer.clipboard_clear()

# the first line contains just the value "T"
# which is the number of integers that need tweaking
line = infile.readline().rstrip()
T = int(line)

#print "The T is ", T

for N in range(0,T):
    line = infile.readline().rstrip()
    originalNumber = int(line)
    case = str(N+1)
    smallest = get_smallest_transposed(originalNumber)
    largest = get_largest_transposed(originalNumber)
    print "Case #"+case+":",smallest,largest

