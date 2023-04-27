#,a

from k4.utils.misc.zprint import *


Last_D = {'D':{}}


def o(
    p,
    e=None,
    wD=None,
    sD=None,
    create_missing_paths=True,
    report_path_creation=True,
    zp=False,
    t=None,
    prune=None,
    copy_=None,
    move = None,
):
    def _zprint(zp,p,D,t,k):
        if zp:
            if t is None: t = p
            #if k is not None:
            #    D = D[k]
            zprint(D,t)

    if sD is not None:
        assert_as( wD is None, "wD is None")
        Last_D['D'] = sD
        D = sD
    elif wD is not None:
        assert_as( sD is None, "sD is None" )
        D = wD
    elif sD is None and wD is None:
        D = Last_D['D']

    assert_as(D is not None,"D is not None")

    if p in ['']:
        _zprint(zp,p,D,t,None)
        return D

    assert_as(has_form_of_path(p),d2n('has_form_of_path(',qtd(p),')'))

    key_list = p[:-1].split('/')

    if e == None:
        
        #for k in key_list:
        for i in rlen(key_list):
           # print(i,D)
            k = key_list[i]
            if i == len(key_list)-1:
                if prune:
                    #print('del D[k]',D,k)
                    del D[k]
                    break
            assert_as( k in D, d2s("k in D? No,",qtd(k),"not in",D))
            D = D[k]
        _zprint(zp,p,D,t,k)
        cy(key_list)
        #if prune:
            #del [key_list[-1]]
            #print(D,key_list[-1],'prune')
        return D 
    else:
        assert_as(prune is None,"prune is None")
        for k in key_list[:-1]:
            if k not in D:
                if create_missing_paths:
                    if report_path_creation:
                        print( d2s('creating',qtd(k)) )
                    D[k] = {}
            D = D[k]
        k = key_list[-1]
        D[k] = e
        _zprint(zp,p,D,t,k)
        cg(key_list)
        return e


def has_form_of_path(s):
    if type(s) == str:
        if len(s) > 1:
            if s[0] != '/':
                if s[-1] == '/':
                    return True
    return False 


if __name__ == '__main__':
 
    code = """

clear_screen()

if '__file__' in locals(): eg(__file__)

import copy

o('a/b/c/d/e/',e=1,sD={},zp=1)

Q = {}

o('x/y/z/',e=2,wD=Q,zp=1)

o('',wD=Q,zp=1,)#t='Q')

o('a/b/c/d/f/',e=Q,zp=1)

o('a/b/g/',e=copy.deepcopy(o('x/y/',wD=Q)),zp=1)

o('a/b/c/d/',zp=1)

o('',zp=1,)#t='Last_D[0]')

o('a/b/c/d/e/',prune=1)

o('',zp=1,)#t='Last_D[0]')

o('a/b/c/',prune=1)

o('',zp=1,t='Last_D[0]')
    """

    for c in code.split('\n'):
        if not c.isspace():
            clp(c,'`--u')
            exec(c)
#,b

if False:
    exec(gcsp()) ###############################################



def q(path,Din,u,d):
    D = Din
    key_list = path[:-1].split('/')
    for i in rlen(key_list):
        k = key_list[i]
        D = D[k]




def a(Din,kl):

    Dout = {}
    for key, element in Din.items():
        kk = kl.copy()
        kk.append(key)
        
        if type(key) is str and key[0] == '=':
            return Dout
        if isinstance(element, dict):
            Dout[key] = a(element,kk)
            Dout[key]['<'] = '/'.join(kk)
            print('/'.join(kk))
        else:
            
            Dout[key] = element
            print(d2f('/',*(kk+[element])))
    return Dout


#EOF





