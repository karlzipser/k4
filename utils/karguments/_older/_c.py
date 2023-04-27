
from k4.utils import *





if False:
    
    W = {'value':{},'doc':{},'type':{}}
    D = {
        'm':'a/a',
        ('mm','mmmm!'):[1,2,3],
        'c':('name',),
        'd':('path','a/b')
    }
    for k in D:
        doc = ''
        if type(k) is tuple:
            assert len(k) == 2
            parameter_name = k[0]
            doc = k[1]
            assert doc
        else:
            assert type(k) is str
            parameter_name = k
        assert parameter_name
        print(parameter_name,doc)

        q = D[k]
        if type(q) is tuple:
            assert len(k) <= 2
            parameter_type = q[0]
            assert parameter_type in ['int','float','bool','name','path']
            if len(q) == 1:
                val = '<required>'
            else:
                val = q[1]
        else:
            val = q
            parameter_type = classify_token(q)
        W['value'][parameter_name] = val
        W['type'][parameter_name] = parameter_type
        W['doc' ][parameter_name] = doc
    zprint(W)





def parse_argument_string(argstr,verbose=True):
    import shlex
    ts = shlex.split(argstr)
    tokens = []
    for t in ts:
        if re.findall('\s',t):
            t = qtd(t)
        tokens.append(t)
    zprint(tokens)
    classifications,tokens = classify_tokens_and_expand_implicit_True_args(tokens)
    if 'unknown' in classifications:
        if verbose:
            for c,t in zip(classifications,tokens):
                if c == 'unknown':
                    cE('Error, token',qtd(t,s=1),"is of 'unknown' type")
            raw_enter()
        return None
    current_arg = ''
    A = {'positional_args':[]}
    for c,t in zip(classifications,tokens):
        if not current_arg:
            if 'argname' not in c:
                A['positional_args'] += [(c,t)]
            else:
                current_arg = t
        elif 'argname' in c:
            current_arg = t
        else:
            if current_arg in A:
                if verbose:
                    cE(argstr)
                    cE('Error,',(c,t),'with current_arg',qtds(current_arg),"already used")
                    cE('Check for positional arguments after first keyword argument or repeat of keyword argument.')
                    raw_enter()
                return None
            A[current_arg] = (c,t)
    Args = {'type':{},'value':{}}
    for k in A:
        t = A[k][0]
        v = A[k][1]
        if t == 'list':
            v = v.split(',')
        if len(k) == 2 and k[0] == '-':
            Args['type'][k[1]] = t
            Args['value'][k[1]] = v
        elif len(k) > 3 and k[0:2] == '--':
            Args['type'][k[2:]] = t
            Args['value'][k[2:]] = v
        else:
            assert k == 'positional_args'
            Args['type'][k] = []
            Args['value'][k] = []
            for p in A[k]:
                t = p[0]
                v = p[1]
                if t == 'list':
                    v = v.split(',')
                Args['type'][k].append( t )
                Args['value'][k].append( v )
    return Args





def classify_tokens_and_expand_implicit_True_args(tokens):
    classifications = []
    for t in tokens:
        classifications += [classify_token(t)]

    a,b = [],[]
    for i in range(len(classifications)-1):
        a += [classifications[i]]
        b += [tokens[i]]
        if classifications[i] in ['short_argname','long_argname']:
            if classifications[i+1] in ['short_argname','long_argname']:
                a += ['bool']
                b += ['True']
    i = -1
    if classifications[i] in ['short_argname','long_argname']:
        a += [classifications[i]]
        b += [tokens[i]]
        a += ['bool']
        b += ['True']

    classifications = a
    tokens = b

    return classifications,tokens





def classify_token(s):
    fs = [
        match_int,
        match_float,
        match_bool,
        match_name,
        match_short_argname,
        match_long_argname,
        match_list,
        match_path,
    ]
    for f in fs:
        m = f(s)
        if m:
            return m
    return 'unknown'




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




def main(argstr):
    Arguments = parse_argument_string(argstr)
    zprint(Arguments,t=argstr)


if __name__ == '__main__':
    argstr = """a b1b_l 1,2,3 2.2 3.a /a.3 '/Users/karl zipser/Desktop' ~/Desktop    -a False --bb -c 0 --xx --dogs -d 1,2,a --dog"""
    main(argstr)


#EOF