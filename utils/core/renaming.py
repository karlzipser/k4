from k4.utils.core.essentials import *

host_name = socket.gethostname()
home_path = os.path.expanduser("~")
username = getpass.getuser()

sleep = time.sleep
sys = os.sys
gg = glob.glob


_Arguments = args_to_dict('face 1 2 -a a3 -b 4 1 a2 5 -c a12 1')

def main(**A):
    eg(__file__)
    print("cos(pi) =",cos(pi))
    print('home_path =',home_path)
    print('username =',username)
    print('host_name =',host_name)
    print('rndn(3) =',rndn(3))
    print_dic_simple(A)
    
if __name__ == '__main__':
    main(**get_Arguments(_Arguments))

#EOF
