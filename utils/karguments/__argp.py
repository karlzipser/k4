from k4.utils import *
import argparse

my_parser = argparse.ArgumentParser(description='<something>')

my_parser.add_argument('-p',
    metavar='',
    type=str,
    help='the path to list')

my_parser.add_argument('--apple',
    metavar='',
    type=str,
    help='an int')

my_parser.add_argument('-q',
    metavar='',
    #nargs='?',
    #default=6,
    type=int,
    help='an int')


my_parser.add_argument('-b',
    action='store_true',
    help='T/F')

# Execute the parse_args() method
A = vars( my_parser.parse_args() )

zprint(A)
