from k4.utils.core.paths import *
from k4.utils.core.times import *
from k4.utils.core.printing import *
import fnmatch

def rb(s):
    return s.replace('\\','')

    
def txt_file_to_list_of_strings(path_and_filename):
    f = open(path_and_filename,"r")
    str_lst = []
    for line in f:
        str_lst.append(line.strip('\n'))
    return str_lst


def list_of_strings_to_txt_file(path_and_filename,str_lst,write_mode="w"):
    f = open(path_and_filename,write_mode)
    for s in str_lst:
        f.write(s+'\n')
    f.close()


def text_to_file(f,t,write_mode="w"):
    list_of_strings_to_txt_file(f,t.split('\n'),write_mode=write_mode)


def file_to_text(f):
    return '\n'.join(txt_file_to_list_of_strings(f))



def assert_disk_locations(locations):
    if type(locations) == str:
        locations = [locations]
    for l in locations:
        if len(gg(l)) < 1:
            raise ValueError(d2s('Could not find',l))



def percent_disk_free(disk='/'):
    statvfs = os.statvfs(disk)
    size_of_filesystem_in_bytes = statvfs.f_frsize * statvfs.f_blocks     # Size of filesystem in bytes
    number_of_free_bytes_that_ordinary_users_have = statvfs.f_frsize * statvfs.f_bavail     # Number of free bytes that ordinary users
    percent_free = dp(100*number_of_free_bytes_that_ordinary_users_have/(1.0*size_of_filesystem_in_bytes))
    return percent_free


def main(**A):
    eg(__file__)
    print("percent_disk_free(disk='/') =", percent_disk_free(disk='/'))

if __name__ == '__main__':
    main()



########################
#
# relic needed for Learn

def args_to_dictionary(*args):
    if not is_even(len(args[0])):
        print("args_to_dictionary(*args)")
        print("args are:")
        print(args)
        #raise ValueError('ERROR because: not is_even(len(args[0]))')
        spd2s('def args_to_dictionary(*args): Warning, not is_even(len(args[0]))')
        return
    ctr = 0
    keys = []
    values = []
    for e in args[0]:
        if is_even(ctr):
            keys.append(e)
        else:
            values.append(e)
        ctr += 1
    d = {}
    if len(keys) != len(values):
        print("args_to_dictionary(*args)")
        print("given keys are:")
        print(keys)
        print("given values are:")
        print(values)
        raise ValueError('ERROR because: len(keys) != len(values)')
    for k,v in zip(keys,values):
        d[k] = v
    return d
def parse_to_Arguments(sys_str):
    a = sys_str.split(' ')
    b = []
    for c in a:
        if c != '':
            b.append(c)
    if len(b) > 1:
        b = b[1:]

    temp = args_to_dictionary(b)
    if type(temp) != dict:
        return {}
    #kprint(temp,'temp')
    if temp != None:
        Args = {}
        for k in temp.keys():
            if '/' in temp[k]:
                print('Treating '+temp[k]+' as filename')
                exec("Args[\'"+k+"\'] = '"+temp[k]+"'")
            elif type(temp[k]) == str:
                exec("Args[\'"+k+"\'] = '"+temp[k]+"'")
            else:
                exec('Args[\''+k+'\'] = '+temp[k])
        del temp
        Arguments_ = {}
        for a in Args.keys():
            ar = Args[a]
            if a[0] == '-':
                assert a[0] == '-'
                assert a[1] == '-'
                a = a[2:]
            else:
                print(Args)
                pd2s('\x1b[1m\x1b[41m\x1b[37m',
                    '*** Warning, argument',
                    "'"+k+"'",
                    'not proceeded by -- on command line ***',
                    '\x1b[0m'
                )
                time.sleep(4)
                #raw_enter()
            if str_is_int(ar):
                Arguments_[a] = int(ar)
            elif str_is_float(ar):
                Arguments_[a] = float(ar)
            elif ',' in ar:
                Arguments_[a] = ar.split(',')
            elif ar == 'True':
                Arguments_[a] = True
            elif ar == 'False':
                Arguments_[a] = False        
            else:
                Arguments_[a] = ar
    return Arguments_


def find_files_recursively(
    src,
    pattern,
    FILES_ONLY=False,
    DIRS_ONLY=False,
    ignore_underscore=True,
    ignore_Trash=True,
    followlinks=True,
    verbose=True,
):
    
    """
    https://stackoverflow.com/questions/2186525/use-a-glob-to-find-files-recursively-in-python
    """
    files = []
    folders = {}
    ctr = 0
    #timer = Timer(5)
    if src[-1] != '/':
        src = src + '/'
    if verbose:
        print('src =' ,src,', pattern = ',"\"",pattern,"\"")
    for root, dirnames, filenames in os.walk(src,followlinks=followlinks):
        assert(not(FILES_ONLY and DIRS_ONLY))
        if FILES_ONLY:
            use_list = filenames
        elif DIRS_ONLY:
            use_list = dirnames
        else:
            use_list = filenames+dirnames
        for filename in fnmatch.filter(use_list, pattern):
            file_ = opj(root,filename)
            folder = pname(file_).replace(src,'')
            if folder not in folders:
                folders[folder] = []
            folders[folder].append(filename)
            ctr += 1
            """
            if timer.check():
                print(d2s(time_str('Pretty'),ctr,'matches'))
                timer.reset()
            """
    if ignore_underscore:
        folders_ = {}
        for f in folders:
            ignore = False
            if ignore_Trash:
                if 'Trash' in f:
                    ignore = True
            g = f.split('/')
            for h in g:
                if len(h) > 0:
                    if h[0] == '_':
                        #cb('ignoring',f)
                        ignore = True
                        break
            if not ignore:
                folders_[f] = folders[f]
        folders = folders_
    data = {}
    data['paths'] = folders
    data['parent_folders'] = [fname(f) for f in folders.keys()]
    data['src'] = src
    data['pattern'] = pattern
    if verbose:
        print(ctr,'matches,',len(data['parent_folders']),'parent folders.')
    return data


#
#
############

def get_temp_filename(path=opjD()):
    t = time.time()
    r = opj(path,d2p('__temp__',t,random_with_N_digits(9),'txt'))
    while t >= time.time():
        print("get_temp_filename sleeping")
        time.sleep(1/10**9)
    return r




#EOF
