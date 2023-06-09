from k4.utils.core.files.files import *

_Arguments = args_to_dict('--one 1111 --two 2222 --three 3333')

def main(**A):
    eg(__file__)
    print_dic_simple(A)
    soD('temp',A)
    B = loD('temp')
    os.system('rm ' + opjD('temp.pkl'))
    print_dic_simple(B)
    
    
def save_obj(obj, name,noisy=False,show_time=False,use_real_path=False):
    import pickle
    assert_disk_locations([pname(name)])
    name = name.replace('.pkl','')
    if use_real_path:
        name = os.path.realpath(name)
    with open(name + '.pkl', 'wb') as f:
        if use_real_path:
            f = os.path.realpath(f)
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    if noisy:
        timer = Timer()
        a = d2s('. . . saved',name+'.pkl')
        if show_time:
            b = d2s('`','in',dp(timer.time()),'seconds.\r')
        else:
            b=''
        pd2s(a,b)




def load_obj(name,noisy=False,time=False,use_real_path=False):
    import pickle
    assert_disk_locations([pname(name)])
    if noisy:
        timer = Timer()
        #clp('Loading','`',name,'`--rb','. . .\r'),
        pd2s('Loading',name,'. . .\r'),
    name = name.replace('.pkl','')
    name = name + '.pkl'
    if use_real_path:
        name = os.path.realpath(name)
    assert_disk_locations(name)
    with open(name, 'rb') as f:
        #o = pickle.load(f)
        o = pickle.load(f, encoding='latin1') # change for python3 to read python2
        # may fail to load python3
        if noisy:
            pd2s(d2s('. . . loaded in',dp(timer.time()),'seconds.\r')),
        return o
        
lo = load_obj

def loD(name,noisy=False,use_real_path=False):
    if use_real_path:
        name = os.path.realpath(name)
    return load_obj(opjD(name),noisy)

def so(arg1,arg2,noisy=False):
    if True:#try:
        if type(arg1) == str and type(arg2) != str:
            save_obj(arg2,arg1,noisy)
            return
        if type(arg2) == str and type(arg1) != str:
            save_obj(arg1,arg2,noisy)
            return
        if type(arg2) == str and type(arg1) == str:
            pd2s('def so(arg1,arg2): both args cannot be strings')
        assert(False)
    else:#except:
        print("exec(EXCEPT_STR)")

def soD(arg1,arg2,noisy=False):
    if True:#try:
        if type(arg1) == str and type(arg2) != str:
            save_obj(arg2,opjD(arg1),noisy)
            return
        if type(arg2) == str and type(arg1) != str:
            save_obj(arg1,opjD(arg2),noisy)
            return
        if type(arg2) == str and type(arg1) == str:
            pd2s('def so(arg1,arg2): both args cannot be strings')
        assert(False)
    else:#except:
        print("exec(EXCEPT_STR)")


if __name__ == '__main__':
    main(**get_Arguments(_Arguments))

#EOF
