
from k4.utils.arg import *

dict_in = {
	'x':int,#5,
	'y':2.,
	'hi':str,#'hello'
}

print('dict_in:',dict_in)

dict_out = parse_args_to_dict(dict_in)

print('dict_out',dict_out)

print(dict_out['hi'],'Product:', dict_out['x'] * dict_out['y'])
