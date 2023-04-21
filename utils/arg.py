import argparse

def ad(d0):

	d1 = {}

	parser = argparse.ArgumentParser()

	for k in d0:
		if len(k) == 1:
			dash = '-'
		else:
			dash = '--'

		if type(d0[k])is type:
			parser.add_argument(
				dash+k,
				type=d0[k],
				required=True,
			)
		else:
			parser.add_argument(
				dash+k,
				nargs='?',
				type=type(d0[k]),
				required=False,
				default=d0[k],
			)

	args = parser.parse_args()

	for k in vars(args):
		d1[k] = vars(args)[k]

	for k in d0:
		if k not in d1 or d1[k] is None:
			print(
				'***',
				k,
				'must have value and cannot be None'
			)
			assert(False)

	return d1

if __name__ == '__main__':

	d0 = {
		'x':5,#int,
		'y':2.,
		'hi':'hello'
	}

	d1 = ad(d0)

	print(d1['hi'],'Product:', d1['x'] * d1['y'])
