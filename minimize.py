#!/usr/bin/env python
import sys
import re
import qm

def print_usage():
    '''Prints usage of program
    '''
    print('Enter one or more logic functions with the given format:')
    print('m(minterms)[optional +d(don\'t care conditions)]')
    print('Ex. m(0,1,2,3)+d(5,6,7)')
    print('Ex. m(5,7,10)\n')


def read_input(fp):
    '''Reads input by line
    returns list of input
    '''
    lines = []
    for line in fp:
        if line == '\n':
            break
        lines.append(line)
    return lines


def split_input(lines):
    '''Splits input into numeric elements
    returns nested list of numbers
    '''
    term_list = []
    for string in lines:
        term_list.append(split_line(string))
    return term_list


def split_line(line):
    '''Splits the input line into numeric elements
    returns list of numbers, empty if non-numeric input
    '''
    matches = []
    # split line by '+' character to facilitate regex matching
    split_line = line.split('+')
    patterns = [re.compile('m\(.+\)'), re.compile('d\(.+\)')]
    for pattern, string in zip(patterns, split_line):
        match = pattern.search(string)
        if match is not None:
            # isolate the internal arguments and split by comma
            str_terms = match.group(0)[2:-1].split(',')
            try:
                int_terms = list(map(int, str_terms))
            except ValueError:
                continue
            except Exception:
                continue
            else:
                matches.append(int_terms)
    return matches


if __name__ == '__main__':
    print_usage()
    fp = sys.stdin if len(sys.argv) < 2 else open(sys.argv[1])
    lines = read_input(fp)
    minterms = split_input(lines)
    for terms, line in zip(minterms, lines):
        function = qm.minimize(terms)
        #print(line[:-1])
        #print(function[0])
        #print(function[1])

