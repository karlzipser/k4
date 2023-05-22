from k4.utils.karguments.parse_utils.classifying import *

def input__( desired_type, prompt='> ', convert_unknown_to_str=False, verbose=True):
    s = input(prompt)
    classified_type = classify_token(s)
    if not convert_unknown_to_str and classified_type == 'unknown':
        if verbose:
            cE("Warning, classified_type == 'unknown'")
        return
    if desired_type not in ['path','str']:
        if desired_type == classified_type:
            if desired_type == 'int':
                return int(s)
            elif desired_type == 'float':
                return float(s)
            elif desired_type == 'bool':
                if s == 'False':
                    return False
                else:
                    return True
            elif desired_type == 'name':
                return s
            else:
                if verbose:
                    cE('Warning,',s,'not understood')
                return
        else:
            if verbose:
                cE('Warning, desired_type ('+desired_type+') != classified_type ('+classified_type+')')
            return
    else:
        return s



def select_from_dict(
    D,
    ignore_underscore=False,
    prefix='',
    print_one_element_lst=True,
    title='',
    max_val_string_len=get_terminal_size()[1]//2,
    return_key=False,
):
    ks = sorted(list(D.keys()))
    print_lst = []
    longest = 0
    for k in ks:
        if len(k) > longest:
            longest = len(k)
    for k in ks:
        s = D[k]
        if type(s) is str:
            s = qtds(s)
        else:
            s = str(s)
        s = s.replace('\t',' ').replace('\n',' ')
        if len(s) > max_val_string_len:
            s = s[:max_val_string_len] + '...'

        print_lst += [ k + (longest-len(k))*' ' + ': ' + s ]
    
    k = select_from_list(
        ks,
        ignore_underscore=False,
        prefix=prefix,
        print_lst=print_lst,
        print_one_element_lst=True,
        title=title,
    )
    if k:
        if return_key:
            return k
        else:
            return D[k]
    

def input_to_dict(
    D,
    ignore_underscore=False,
    prefix='',
    print_one_element_lst=True,
    title='',
    max_val_string_len=get_terminal_size()[1]//2,
    prompt='Enter new value for key XXX: ',
    verbose=True,
):
    Atomic = {}

    for k in D:
        if type(D[k]) in [str,int,float,bool,str]:
            Atomic[k] = D[k]

    k = select_from_dict(
        Atomic,
        title=title,
        return_key=True,
        max_val_string_len=get_terminal_size()[1]//2
    )
    if k:
        v = input__( 
            type(D[k]).__name__,
            prompt=prompt.replace('XXX',qtds(k)),
            convert_unknown_to_str=True,
        )
        if type(v) is not None:
            D[k] = v
            return True

    if verbose:
        if k:
            cE('No change for key',qtds(k))
        else:
            cE('No change')

    return False



if __name__ == '__main__':

    D = {
    'one' : 1,
    '2': '2',
    'three':(1,2,3,4,5,6,7,8,9,10,),
    'a txt' : """Four score and seven years ago
our fathers brought forth upon this continent,
a new nation, conceived in Liberty,
and dedicated to the proposition that all
men are created equal.
""",
    'xxx' : {1:2,3:{4:5}},
    }

    a = select_from_dict(D,title='\nselect_from_dict:')

    print('You selected:\n'+boxed(a))

    input_to_dict(D,title='\ninput_to_dict:')

    zprint(D,t='D')
    



#EOF

