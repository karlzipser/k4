from k4 import *
from htmlpy import *
import tree_
import importlib
from contextlib import redirect_stdout
import html

D = {'files_dir':opjk('utils'),}

Imports = {}


# sort out problem with directory to dic

verbose = False

def get_Output_form(p,A):
    s = """
   <form>
   """
    """
      <input readonly style="font-size:25px;font-weight:bold;" type="text" id="file_output" name="file_output" value=\""""+p+"""\">
      <label for="file">file</label>
      <br>
    """
    #s = ''
    for k in A.keys():
        Ak = str(A[k])
        k = str(k)
        k_ = k + '_output'
        s += """
  <input style="font-size:14px;" type="text" id=\""""+k_+"""\" name=\""""+k_+"""\" value=\""""+Ak+"""\">
  <label for=\""""+k_+"""\">"""+k+"""</label>
  <br>
    """

    """
  <input spellcheck="false" style="font-size:14px;" type="text" id="extra_output" name="extra_output" value="">
  <label for="extra_output">additional cmd line str</label>
  <br>
  """

    s += """
  <input hidden readonly type="text" id="run_output" name="run_output" value=\"Run\">
    """
    s += """
  <input hidden readonly type="text" id="city_tab" name="city_tab" value=\"Output\">
    """    
    s += """
  <input type="submit" value="Run">
  </form>
    """
    return s





#html_warning = "html detected, this page not shown"

from bs4 import BeautifulSoup

def handle_path_and_URL_args(p,URL_args):

    if 'SaveCode' in URL_args:
        #print(qtd(URL_args['SaveCode']))

        if not bool(BeautifulSoup(URL_args['SaveCode'], "html.parser").find()):
            sc = URL_args['SaveCode'].replace('\r','')
            n = opjh('bkps',p.replace(opjh(),''))
            cy('Saving',p)#n.replace(opjh(),''))
            os_system('mkdir -p',pname(n))
            os_system('mv',p,d2p(n,time.time()))
            text_to_file(p,sc)
            if len(URL_args['SaveCode']) > 50:
                URL_args['SaveCode'] = URL_args['SaveCode'][:50]+' . . .'
        else:
            print("Can't save because URL_args['SaveCode'] contains html")
            #print(qtd(URL_args['SaveCode']))
    if exname(p) == 'py':
        try:
            if p not in Imports:
                Imports[p] = importlib.import_module( opj(pname(p),fnamene(p)).replace('/','.') ) 
                Imports[p+':time'] = time.time()
                if verbose:
                    cb('imported',p)

            if os.path.getmtime(p) > Imports[p+':time']:
                importlib.reload( Imports[p] )
                Imports[p+':time'] = time.time()
                if verbose:
                    cb('reloaded',p)

            try:
                Imports[p]._Arguments
                #zprint(Imports[p].Arguments,'Arguments: '+p)
            except:
                pass#cb('p has no Arguments')
            #Imports[p].main(**URL_args)
        except:
            cr('Could not import',p)

H=(('&','&amp;'),('<','&lt;'),('>','&gt;'),('\"','&quot;'))

def get_SubCode(url):

    SubCode = {
        '---ACE-ACE---':    opjk('utils/html/ace/ace.js'),
        '---ACE-MODE---':   opjk('utils/html/ace/mode-python.js'),
        '---ACE-THEME---':  opjk('utils/html/ace/theme-iplastic.js'),#opjk('utils/html/ace/theme-iplastic.js'),#
        '---WEBPAGE---':    opjk('utils/html/webpage.html'),
        't--FIGURES---':    """<img src="/Pictures/Internet_dog.jpg" ;>""",
        't--SAVE-HIDDEN---': "",
        't--HTML-CODE-AREA---': "",

    }

    path, URL_args = urlparse(url)
    #cm(path)
    p = path
    del path
    if p[0] == '/' and len(p) > 1:
        p = p[1:]
    #cy(p)
    if not os.path.isfile(p):
        p_ = p
        p = opjk('utils/__init__.py').replace(opjh(),'')
        #cr(p_,'-->',p,r=0)

    handle_path_and_URL_args(p,URL_args)

    SubCode['t--URL_args---'] = print_dic_simple(
        URL_args,'',html=True,print_=False)

    try:

        if len(sggo(p)) == 1:
            from urllib.parse import quote
            if exname(p) in IMAGE_EXTENSIONS:
                SubCode['t--EDITOR---'] = \
                    "<img src=\"/"+quote(p)+"\"; width=\"350\">"
                SubCode['---ACE-ACE---'] = ''
                SubCode['---ACE-THEME---'] = ''
                SubCode['---ACE-MODE---'] = ''
            elif exname(p) in ['pdf']:
                SubCode['t--EDITOR---'] = \
                    "<embed src=\"/"+quote(p)+"\"; width=\"350\">"
            else:
                raw_code = file_to_text(p)
                SubCode['t--EDITOR---'] = raw_code
                if bool(BeautifulSoup(SubCode['t--EDITOR---'], "html.parser").find()):
                    
                    #SubCode['t--TEXTAREA---'] = "<!-- contains html -->\n"+SubCode['t--EDITOR---']
                    SubCode['t--EDITOR---'] = ""#html_warning
                    SubCode['t--SAVE-HIDDEN---'] = 'hidden'
                    #for k in H:
                    #    SubCode['t--EDITOR---'] = SubCode['t--EDITOR---'].replace(k,H[k])
                    SubCode['---ACE-ACE---'] = opjk('utils/html/ace/mode-python.js')
                    for h in H:
                        k = h[0]
                        Hk = h[1]
                        raw_code = raw_code.replace(k,Hk)
                    text_to_file(opjD('raw.txt'),raw_code)
                    SubCode['t--HTML-CODE-AREA---'] =\
                        """
<pre
    style="
        /*float:left;*/
        cursor: no-drop;
        background-color: #FFDDD0;
        font-family: 'Courier New';
        font-size: 10px;
        height: 100%;
        /*width:300px;*/
        overflow: scroll;
        /*overflow-x: hidden;
        overflow-y: scroll;*/

    "
>\n""" + '\n<br>'.join(raw_code.split('\n')) + "</pre>"
    except:
        pass

    A = {}
    try:
        A = Imports[p]._Arguments
    except:
        pass
    if type(A) is not dict:
        A = {}
    SubCode['t--OUTPUT---'] = get_Output_form(p,A)

    SubCode['t--TITLE---'] = p

    if 'files_dir' in URL_args and len(URL_args['files_dir']) > 0:
        D['files_dir'] = URL_args['files_dir']

    SubCode['t--FILES---'] = tree_.get_tree(D['files_dir'])

    A = {}
    for k in URL_args:
        if k.endswith('_output'):
            k_ = k.replace('_output','')
            A[k_] = URL_args[k]
    #zprint(A,'A')
    out = 'k4/__private__/__private3.temp.txt'
    #print('def main(**' in file_to_text(SubCode['---EDITOR---']))
    #if True:#'def main(**' in SubCode['---EDITOR---']:
        #cr(0,r=1)
    if 'run' in A:
        if True:#try:
        #cr(1,r=1)
            with open(out, 'w') as f:
                with redirect_stdout(f):
                    if False:#os.path.getmtime(p) > Imports[p+':time']:
                        importlib.reload( Imports[p] )
                        Imports[p+':time'] = time.time()
                    Imports[p].main(**A)
            SubCode['t--OUTPUT---'] += '<hr>'+lines_to_html_str(file_to_text(out))
        else:#except:
            SubCode['t--OUTPUT---'] += \
                '<hr>'+lines_to_html_str("\ncould not run Imports[p].main(**A)")
            cr("could not run Imports[p].main(**A)")

    if 'city_tab' in URL_args:
        SubCode['t--CITY_TAB---'] = \
            """onload="openTab('event', '"""+URL_args['city_tab']+"""')" """
        #cr(SubCode['t--CITY_TAB---'])
    else:
        SubCode['t--CITY_TAB---'] = """onload="openTab('event', '-')" """
        #cy(SubCode['t--CITY_TAB---'])
    # onload="setURL()"

    return SubCode

#EOF
