

def print(*args, stdout=False, **kwargs):
    import sys
    import builtins as __builtins__
    if stdout:
        f = sys.stdout
    else:
        f = sys.stderr
    return __builtins__.print(*args, file=f, **kwargs)

#print('test of stdout',stdout=True)



imports = (
    'os',
    'os.path',
    #'shutil',
    #'scipy',
    #'scipy.io',
    #'copy',
    #'string',
    'glob',
    'time',
    'sys',
    #'datetime',
    #'random',
    're',
    #'subprocess',
    #'threading',
    #'serial',
    #'inspect',
    #'fnmatch',
    #'h5py',
    'socket',
    'getpass',
    #'numbers',
    #'math',
    #'pickle',
    'time',
    #'importlib',
    #('FROM','pprint','pprint'),
    #('FROM','termcolor','cprint'),
    #('FROM','collections','namedtuple'),
    #('AS','numpy','np'),
    ('FROM','copy','deepcopy'),
)

for im in imports:
    if type(im) == str:
        try:
            exec('import '+im)
        except:
            pass
            print('Failed to import '+im)
    else:
        assert type(im) == list or type(im) == tuple
        if im[0] == 'FROM':
            try:
                exec('from '+im[1]+' import '+im[2])
            except:
                pass
                print('Failed to from '+im[1]+' import '+im[2])
        else:
            assert(im[0] == 'AS')
            try:
                exec('import '+im[1]+' as '+im[2])
            except:
                pass
                print('Failed to import '+im[1]+' as '+im[2]) 





def main(**A):
    print(np.pi)
    print(time.time())
    pprint([[1,2,3],4])
    
if __name__ == '__main__':
    main()
#EOF
