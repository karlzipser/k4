#,a

from k4.utils.misc.environment import *


def set_str(path):
    s='Enter str for'
    v = input(d2s(s,qtd(path),'> '))
    o(path,e=v)  
    return d2s(qtd(path),'set to',o(path))


def set_number(dst_path,min_path,max_path):
    #cy(dst_path,min_path,max_path,r=1)
    mn,mx = o(min_path,w='~/'),o(max_path,w='~/')
    assert(is_number(mn))
    assert(is_number(mx))

    target_type = type(o(dst_path))

    v = input(d2s('Enter',target_type.__name__,'for',qtd(dst_path),'in range',(mn,mx),'> '))

    no = False

    if target_type == int:

        if str_is_int(v):
            v = int(v)
        else:
            no = True

    elif target_type == float:
        if str_is_float(v):
            v = float(v)
        else:
            no = True
    else:
        no = True

    if no:
        return d2s('failed to set',qtd(dst_path),'to',v)

    if v < mn or v > mx:
        return d2s(v,'not in range',(mn,mx))

    o(dst_path,e=v)
            
    return d2s(qtd(dst_path),'set to',o(dst_path))


def set_from_list(dst_path,options_path):
    #cy(dst_path,options_path)
    #cm(o(options_path),r=1)

    for i in rlen(o(options_path,w='~/')):
        clp('    ',i,') ',o(options_path,w='~/')[i],s0='')

    i = input_int_in_range(0,len(o(options_path,w='~/'))-1,'>> ')
    if i is None:
        return 'failed'

    o(dst_path,e=(o(options_path,w='~/')[i]))
    return d2s(qtd(dst_path),'set to',o(dst_path))


def set_toggle(path):
    o(path,e=not o(path))
    message = d2s('toggled',qtd(path),'to',o(path))
    return message




def is_functional(path):
    import collections.abc

    ks = kys(o(path))
    if '_function' in ks:
        if isinstance(o(path+'_function/'),collections.abc.Callable):
            f = o(path+'_function/')
        else:
            return False
    else:
        return False
    if '_args' in ks:
        arg_paths = o(path+'_args/')
    else:
        arg_paths = []
    if 'value' in ks:
        value_path = path+'value/'
    else:
        return False
    return [f,arg_paths,value_path]


def run_function(path,z=0):
    r = is_functional(path)
    if not r:
        return None
    f,arg_paths,value_path = r[0],r[1],r[2]
    
    message = f(value_path,*arg_paths)

    if z:
        zprint(Environment,ignore_underscore=Environment['params']['ignore_underscore'])

    return message

def create_shadow(path):
    pass

def select_functional():
    pass

def delete_node(path):
    pass

def move_node(path,new_path):
    pass

def scan_tree(path):
    pass

def myprint(d):
    for k, v in d.items():
        if isinstance(v, dict):
            myprint(v)
        else:
            print("{0} : {1}".format(k, v))



def a(Din,kl):

    Dout = {}
    for key, element in Din.items():
        kk = kl.copy()
        kk.append(key)
        
        if type(key) is str and key[0] == '=':
            return Dout
        if isinstance(element, dict):
            if is_functional(element):
                cy('is_functional',r=1)
            Dout[key] = a(element,kk)
            Dout[key]['<'] = '/'.join(kk)
            print('/'.join(kk))
        else:
            
            Dout[key] = element
            print(d2p(*(kk+[element])))
    return Dout




if __name__ == '__main__':
    if '__file__' in locals(): eg(__file__)
    
    Environment['dictionary']['~shadow'] = {}

    _words = ['cat','dog','bird','horse']
    Environment['top']['_functionals'] = {
            'value':None,
            '_function':set_from_list,
            '_args':['dictionary/_functionals/_paths/'],
            '_paths':['dictionary/~/menu/range/min/','dictionary/~/menu/range/max/'],
    }
    Environment['top']['world']['~'] = {
        'range':{
            'min':{
                'value':0,
                '_function':set_number,
                '_args': ['dictionary/~menu/range/_min/','dictionary/~menu/range/_max/'],
            },
            'max':{
                'value':10,
                '_function':set_number,
                '_args': ['dictionary/~menu/range/_min/','dictionary/~menu/range/_max/'], 
            },
            '_min':0,
            '_max':10,
        },
        'toggle':{
            'value':False,
            '_function':set_toggle,
        },
        'word': {
            'value':_words[-1],
            '_function':set_from_list,
            '_args':['menu/word/_options/'],
            '_options':_words,
        },
        'str': {
            'value':'This is a string.',
            '_function':set_str,
        },
    }
    del _words
 
    if False:
        zprint(Environment)

        run_function('menu/range/min/',1)

        run_function('menu/range/max/',1)

        o(s='~/menu/')

        run_function('toggle/',1)
        run_function('str/',1)
        run_function('word/',1)


    #zprint(a(_menu,[]))
    zprint(a(Environment,[]))

#,b

if False:
    exec(gcsp()) ###############################################


#EOF
