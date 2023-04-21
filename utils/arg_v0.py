
import argparse

d0 = {
	'x':int,
	'y':2,
}

d1 = {}

parser = argparse.ArgumentParser()

for k in d0:
	if len(k) == 1:
		dash = '-'
	else:
		dash = '--'
	print(k,d0[k])
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

#parser.add_argument('--x', type=int, required=True)
#parser.add_argument('--y', type=int, required=True)

args = parser.parse_args()
print('***',args.y)
for k in vars(args):
	d1[k] = vars(args)[k]
print(d1)
product = d1['x'] * d1['y']

print('Product:', product)
