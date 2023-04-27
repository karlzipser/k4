#,a
from k4.utils.misc.zprint import *

Environment = {
    'params': {
        'create_missing_paths':True,
        'report_implicit_path_creation':True,
        'max_num_messages':20,
        'message_ctr':0,
        'max_depth':10**6,
        'ignore_underscore':False,
    },
    'current_prefix_path': '~/',
    'aliases': {},
    'messages':[],
    

    'dictionary': { '~':{} },
}




def o(
    p=None,
    e=None,
    w=None,
    s=None,
    u=None,
    d=None,
    a=None,
    ):

    r = _up_or_down(u,d)

    if r is not None:
        return r ###################

    assert_as( w is None and s is None, "w is None and s is None" )
    path = _get_path(p,w,s)

    if a is not None:
        assert_as(has_form_of_alias(a),"has_form_of_alias(a)")
        Environment['aliases'][a] = path

    key_list = path[:-1].split('/')
    D = Environment['dictionary']

    if e == None:
        for k in key_list:
            k = str_to_tuple_as_necessary(k)
            assert_as( k in D, d2s("k in D? No,",k,"not in",D))
            D = D[k]
        #_message(d2s("returning value at",path))
        return D ###################
    else:
        for k in key_list[:-1]:
            k = str_to_tuple_as_necessary(k)
            if k not in D:
                if Environment['params']['create_missing_paths']:
                    if Environment['params']['report_implicit_path_creation']:
                        _message( d2s('creating',k) )
                    D[k] = {}
            D = D[k]
        k = str_to_tuple_as_necessary( key_list[-1] )
        D[k] = e
        #_message(d2s("returning value set at",path))
        return e ###################







def _get_path(p,w,s):
    prefix = Environment['current_prefix_path']

    assert_as( at_least_1_None(w,s), "at_least_1_None(w,s)")

    if has_form_of_alias(w):
        w = Environment['aliases'][w]

    if has_form_of_path(w):
        prefix = w

    if has_form_of_alias(s):
        s = Environment['aliases'][s]

    if has_form_of_path(s):
        Environment['current_prefix_path'] = s
        prefix = s

    if has_form_of_alias(p):
        assert_as(s is None, "s is None")
        assert_as(w is None, "w is None")
        path = Environment['aliases'][p]

    elif has_form_of_path(p):
        path = prefix + p

    elif p is None:
        path = prefix

    else:
        cE(p,'is neither path nor alias')

    return path


def _message(message):
    Environment['messages'] = Environment['messages'][-Environment['params']['max_num_messages']:]
    Environment['params']['message_ctr'] += 1
    Environment['messages'].append((Environment['params']['message_ctr'],message))
    


def _up_or_down(u,d):
    
    assert_as( at_least_1_None(u,d), "at_least_1_None(u,d)")

    if u == 1:
        if Environment['current_prefix_path'] == '~/':
            _message("already at top")
            return o() ###################
        Environment['current_prefix_path'] = pname_(
            Environment['current_prefix_path']
        ) + '/'
        _message('went up to '+Environment['current_prefix_path'])
        return o( w=Environment['current_prefix_path'] ) ###################

    if d == 1 or d == True or has_form_of_alias(d):
        key_list = Environment['current_prefix_path'][:-1].split('/')
        D = Environment['dictionary']
        for k in key_list:
            k = str_to_tuple_as_necessary(k)
            D = D[k]
        if type(D) == dict:
            if has_form_of_alias(d):
                if d in kys(D):
                    Environment['current_prefix_path'] += d + '/'
                    _message(d2s('down to',d))
                    return o() ###################
                else:
                    assert False
            if len(kys(D)) > 1:
                k = select_from_list(kys(D))
            else:
                k = kys(D)[0]
            Environment['current_prefix_path'] += k + '/'
            _message(d2s('down to',k))
        else:
            _message("can't go down")
        return o() ###################
    elif d is None:
        pass

    else:
        assert False




def at_least_1_None(*l):
    for q in l:
        if q is None:
            return True
    return False


def has_form_of_path(s):
    if type(s) == str:
        if len(s) > 1:
            if s[0] != '/':
                if s[-1] == '/':
                    return True
    return False


def has_form_of_alias(s):
    if type(s) == str:
        if len(s) > 0:
            if '/' not in s:
                return True
    return False    



def str_to_tuple_as_necessary(s):
    if type(s) == str:
        if len(s) > 1:
            if s[-1] == ',':
                if str_is_int(s[:-1]):
                    return (int(s[:-1]),)
    return s


def pname_(path):
    assert has_form_of_path(path)
    path = path[:-1]
    return pname(path)


def input_int(s='> '):
    c = input(s)
    if str_is_int(c):
        return int(c)
    else:
        return None


def input_int_in_range(a,b,s):
    c = input_int(s)
    if c is None or c < a or c > b:
        return None
    else:
        return c


def select_from_list(lst):
    for i in rlen(lst):
        clp('    ',i,') ',lst[i],s0='')
    i = input_int_in_range(0,len(lst)-1,'>> ')
    return lst[i]







if __name__ == '__main__':

    if '__file__' in locals(): eg(__file__)

    print(o('a/b/c/',e=1))

    print(o('a/b/d/',e=456,a='d'))

    zprint(o(),t='3')
    
    print(o('a/b/e/',e=789,a='e'))

    zprint(o(),t='4')

    print(o('a/f/g/h/',e=3,a='h'))

    zprint(o(),t='5')

    #print(o(s='~/a/f/'))

    
    #print(o('g/h/',e=6))

    #zprint(o(),t='6')
    
    zprint(Environment)


if False:
    exec(gcsp()) ###############################################


#EOF





