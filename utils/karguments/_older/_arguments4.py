
from k4.utils import *


alp = '[A-Za-z]'
alpnum = '[A-Za-z0-9_]'
path_ = '[-~/.A-Za-z0-9_]'
path_s = '[-~/.A-Za-z0-9_\s]'


def match_int(s):
    if type(s) is int:
        return 'int'
    if type(s) is not str:
        return
    if str_is_int(s):
        return 'int'


def match_float(s):
    if type(s) is float:
        return 'float'
    if type(s) is not str:
        return
    if str_is_float(s):
        return 'float'


def match_bool(s):
    if type(s) is bool:
        return 'bool'
    if type(s) is not str:
        return
    if s in ['True','False']:
        return 'bool'


def match_name(s):
    if type(s) is not str:
        return
    if match_whole([alp,alpnum,'*'],s):
        return 'name'


def match_short_argname(s):
    if type(s) is not str:
        return
    if match_whole(['-',alp],s):
        return 'short_argname'


def match_long_argname(s):
    if type(s) is not str:
        return
    if match_whole(['--',alp,alpnum,'+'],s):
        return 'long_argname'


def match_list(s):
    if type(s) is list:
        return 'list'
    if ',' in s:
        return 'list'


def match_path(s):
    if type(s) is not str:
        return
    if len(s) > 2:
        if s[0] == '"' and s[-1] == '"':
            s = s[1:-1]
        if s[0] == "'" and s[-1] == "'":
            s = s[1:-1]
    if match_whole(['[~/.]+'],s):
        return 'path'
    if match_whole(['[~/.]*',alpnum,path_s,'*'],s):
        return 'path'


def match_whole(pattern,s):
    if type(pattern) is list:
        pattern = ''.join(pattern)
    return re.match(d2n('^',pattern,'$'),s)



#EOF