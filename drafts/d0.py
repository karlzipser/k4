
from k4.utils.arg import *

dict_in = {
	'n':int,
	's':str,
}

print('dict_in:',dict_in)

dict_out = parse_args_to_dict(dict_in)

print('dict_out',dict_out)

print(dict_out['n'] * dict_out['s'])
