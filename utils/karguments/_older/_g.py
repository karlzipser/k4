
from k4.utils import *





def main(argstr):
    Arguments = parse_argument_string(argstr)
    zprint(Arguments,t=argstr)


if __name__ == '__main__':
    argstr = """a b1b_l 1,2,3 2.2 3.a /a.3 '/Users/karl zipser/Desktop' ~/Desktop    -a False --bb -c 0 --xx --dogs -d 1,2,a --dog"""
    main(argstr)


#EOF