#,a
from k4.utils.misc.environment import *


def menu():
    clear_screen()
    zprint(o(),t='o()',max_depth=Environment['params']['max_depth'])
    print('')
    if len(Environment['messages']) > 0:
        m = Environment['messages'][-1] 
        s = cf(str(m[0])+')',m[1],'`g')
    else:
        s = ''
    c = input(s + ' >> ')
    if c == 'u':
        o(u=1)
    elif c == 'd':
        o(d=1)
    elif c == 'q':
        return False

    elif c == 'm':
        m = input_int('enter max_depth ('+str(Environment['params']['max_depth'])+') >>> ')
        if type(m) is int and m > 0:
            Environment['params']['max_depth'] = m
    else:
        if c == '':
            c = '<enter>'
        cr(qtd(c),'is unknown option')

    return True


def set_str(path):
    s='Enter str for'
    v = input(d2s(s,qtd(path),'> '))
    o(path,e=v)  
    return d2s(qtd(path),'set to',o(path))


def set_number(dst_path,mn,mx):

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

    for i in rlen(di(options_path)):
        clp('    ',i,') ',di(options_path)[i],s0='')

    i = input_int_in_range(0,len(di(options_path))-1,'>> ')
    if i is None:
        return 'failed'

    o(dst_path,e=(o(options_path)[i]))
    return d2s(qtd(dst_path),'set to',di(dst_path))


def set_toggle(path):
    o(path,e=not o(path))
    message = d2s('toggled',qtd(path),'to',di(path))
    return message





if __name__ == '__main__':
    if '__file__' in locals(): eg(__file__)
        
    _words = ['cat','dog','bird','horse']
    Environment['dictionary']['~']['menu'] = {
        'range':{
            'min':{
                'value':0,
                '_function':set_number,
                '_args': ['menu/range/_min/','menu/range/_max/'],
            },
            'max':{
                'value':10,
                '_function':set_number,
                '_args': ['menu/range/_min/','menu/range/_max/'], 
            },
            '_min':0,
            '_max':10,
        },
        'set_toggle':{
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
 

    while menu():
        pass





#,b

#EOF
