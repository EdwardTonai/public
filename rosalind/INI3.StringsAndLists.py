# INI3: Strings and Lists
# OS: Windows 7
# python 2.7

import argparse
from Tkinter import Tk # For sending answers to the clipboard

def perform_rosalind_ini3(infile,answer):
    dataset = infile.readline()
    indices = infile.readline()
    int_indices = [int(x) for x in indices.split()]
    answer.clipboard_append(dataset[int_indices[0]:int_indices[1]+1] + ' ' + dataset[int_indices[2]:int_indices[3]+1])
    print dataset[int_indices[0]:int_indices[1]+1] + ' ' + dataset[int_indices[2]:int_indices[3]+1]

parser = argparse.ArgumentParser()
parser.add_argument("fileName")
args = parser.parse_args()

file_name = args.fileName

infile = open(file_name)

answer = Tk()
answer.withdraw()
answer.clipboard_clear()

perform_rosalind_ini3(infile,answer)

