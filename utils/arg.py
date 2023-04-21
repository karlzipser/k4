import argparse

def parse_args_to_dict(dict_in):

	dict_out = {}

	parser = argparse.ArgumentParser()

	for k in dict_in:

		if len(k) == 1:
			dash = '-'
		else:
			dash = '--'

		if type(dict_in[k])is type:
			parser.add_argument(
				dash+k,
				type=dict_in[k],
				required=True,
			)
		else:
			parser.add_argument(
				dash+k,
				nargs='?',
				type=type(dict_in[k]),
				required=False,
				default=dict_in[k],
			)

	args = parser.parse_args()

	for k in vars(args):
		dict_out[k] = vars(args)[k]

	for k in dict_in:
		if k not in dict_out or dict_out[k] is None:
			print(
				'***',
				k,
				'must have value and cannot be None'
			)
			assert(False)

	return dict_out


if __name__ == '__main__':

	dict_in = {
		'x':int,#5,
		'y':2.,
		'hi':str,#'hello'
	}

	print('dict_in:',dict_in)

	dict_out = parse_args_to_dict(dict_in)

	print('dict_out',dict_out)

	print(dict_out['hi'],'Product:', dict_out['x'] * dict_out['y'])


	#EOF
