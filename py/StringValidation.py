# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 12:28:10 2023

@author: COnnor.gibbs
"""

from time import strptime
import re
def is_valid_date(string):
    """Checks if a string is a valid date"""
    try:
        strptime(string, '%m/%d/%Y')
        return True
    except ValueError:
        return False

def is_ssn(string):
    """Checks if string is a valid social security number"""
    pattern = r'^\d{9}$'  # Regex pattern for exactly nine digits
    return bool(re.match(pattern, string))

def remove_empty_words(lines):
    """Removes empty words from each line in lines."""
    lines = [[elem for elem in inner_list if elem != ''] for inner_list in lines]
    return lines

def remove_string(lines, string):
    """Recursively removes a string from each line in lines."""
    for inner_list in lines:
        for i in range(len(inner_list)):
            inner_list[i] = inner_list[i].replace(string, '')
    return lines

def remove_lines_with_string(lines, strings):
    """Removes line in lines if line contains any string in strings."""
    strings_set = set(strings)
    lines = [line for line in lines if not any(string in ' '.join(line) for string in strings_set)]
    return lines

def line_contains_string(lines, strings):
    """Returns true if any of the strings are in the line for each line or false otherwise."""
    strings_set = set(strings)
    result = []
    for line in lines:
        found = False
        for string in strings_set:
            if string in ' '.join(line):
                found = True
                break
        result.append(found)
    return result