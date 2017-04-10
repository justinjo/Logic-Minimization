#!/usr/bin/env python
import sys
import re
import implicant as imp

def read_input(fp):
    """Reads input by line
    returns list of input
    """
    lines = []
    for line in fp:
        if line == '\n':
            break
        lines.append(line)
    return lines

def split_input(lines):
    """Splits input into numeric elements
    returns nested list of numbers
    """
    terms = []
    for string in lines:
        terms.append(split_line(string))
    return terms

def split_line(line):
    split_line = line.split('+')
    patterns = [re.compile('m\(.+\)'), re.compile('d\(.+\)')]
    matches = []
    for pattern, string in zip(patterns, split_line):
        match = pattern.search(string)
        if match is not None:
            string = match.group(0)[2:-1]
            matches.append(string.split(','))
        else:
            return []
    return matches

if __name__ == '__main__':
    fp = sys.stdin if len(sys.argv) < 2 else open(sys.argv[1])
    lines = read_input(fp)
    minterms = split_input(lines)
    for item in minterms:
        print(item)
