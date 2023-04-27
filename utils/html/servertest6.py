from k4 import *
from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer
from contextlib import redirect_stdout
import importlib
from k4.drafts.htmltemp import *

hostName = "localhost"
hostPort = 9000
Images = {}

import re

# 7-bit C1 ANSI sequences
ansi_escape = re.compile(r"""
    \x1B  # ESC
    (?:   # 7-bit C1 Fe (except CSI)
        [@-Z\\-_]
    |     # or [ for CSI, followed by a control sequence]
        \[
        [0-?]*  # Parameter bytes
        [ -/]*  # Intermediate bytes
        [@-~]   # Final byte
    )
""", re.VERBOSE)
#result = ansi_escape.sub('', sometext)


def trim_paths(paths):
    paths = sorted(paths)
    q = []
    for p in paths:
        q.append(p.replace(opjk(),'').split('/'))

    for i in range(len(q)-1,1,-1):
        for j in rlen(q[i]):
            print(i,j)
            try:
                if q[i][j] == q[i-1][j]:
                    q[i][j] = ' '*len(q[i][j])
            except:
                pass
    r = []
    for u in q:
        r.append('/'.join(u).replace('/ ','  ').replace(opjk(),'').replace(' /','  '))
    return r


a = get_list_of_files_recursively(opjk('utils'),'*.py')
b = []
for c in a:
    #if fname(a)[0] == '_':
    #    continue
    b.append('/'+c.replace(opjh(),''))
paths = sorted(b)

Imports = {}
print('Sart Imports...')
for p in paths:
    try:
        if p[0] == '/':
            p = p[1:]
        m = opj(pname(p),fnamene(p)).replace('/','.')
        Imports[p] = importlib.import_module( opj(pname(p),fnamene(p)).replace('/','.') ) 
        Imports[p+':time'] = time.time()
    except:
        print(p,'failed')
print('Imports done.')
class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):

        mimetype=None
        if exname(self.path) in ('jpeg','jpg','JPG','JPEG'):
            mimetype='image/jpg'
        elif exname(self.path) in ('png','PNG'):
            mimetype='image/png'
        elif exname(self.path) in ('gif','GIF'):
            mimetype='image/gif'

        if mimetype is not None:      
            path_to_image = opjh(self.path)[1:]
            statinfo = os.stat(path_to_image)
            img_size = statinfo.st_size
            self.send_response(200)
            self.send_header("Content-type", mimetype)
            self.send_header("Content-length", img_size)
            self.end_headers()
            if path_to_image not in Images:
                f = open(path_to_image, 'rb')
                cg('loading',path_to_image)
                Images[path_to_image] = f.read()
                f.close()
            self.wfile.write(Images[path_to_image])

        elif "favicon.ico" in self.path:
            return





        else:

            path, URL_args = urlparse(self.path)
            p = path
            out = 'k4/__private__/__private2.temp.txt'
            code = ''
            raw_code = ''
            if p[0] == '/':
                p = p[1:]
            if 'save_code' in URL_args:
                sc = URL_args['save_code'].replace('\r','')
                #p2 = opjD(p)
                #os_system('mkdir -p',pname(p2))
                os_system('mv',p,d2p(p,time.time()))
                text_to_file(p,sc)  

            if False:#path not in paths:
                path = paths[0]
                redirect = """<meta http-equiv="Refresh" content="0; url='"""+\
                    path+"""'" />"""
            else:
                redirect = ''

            
                #cb(p,r=1)
                raw_code = file_to_text(p)
                code = highlight(raw_code, PythonLexer(), HtmlFormatter())
                

                if 'def main(**' in raw_code:

                    with open(out, 'w') as f:
                        with redirect_stdout(f):
                            if os.path.getmtime(p) > Imports[p+':time']:
                                importlib.reload( Imports[p] )
                                Imports[p+':time'] = time.time()
                            Imports[p].main(**URL_args)
                else:
                    cm('python3',p,'--url',self.path,'>',out,r=0)
                    os_system('python3',p,'--url',qtd(self.path),'>',out)






            s = head_('this is the title')
            s += style
            s += form_('arguments')
            s += '<h3>'+p+'</h3>'

            s += """
<div style="
    margin:0;
    width:280px;
    height:790;
    float: right !important;
    margin-right:20px;
    margin-left:20px;
    position:relative;
    padding: 0;
    text-align: left;
    font-family:'Courier New';
    font-size:14px"
    overflow-y: scroll;

    "
"""

            s += div(60)
            ctr = 0
            q = 40
            for pp,pr in zip(trim_paths(paths),paths):
                if 'has' in URL_args:
                    if URL_args['has'] not in pp:
                        continue
                # +"?a=b&c=d"
                url = pp+'?has=utils/core'
                s += href_(pr,pp[1:].replace(' ','&nbsp'),False)#min(q,len(p))])# + max(0,(q-len(p)))*sp
                ctr += 1
                if True:#ctr%3 ==0:
                    s += br
            s += "</div><hr>"

            s += div(150)
            s += '<h2>'+'input/output'+'</h2>'
            
            s_ = 'path: '+path +'\n'
            for u in URL_args:
                if u == 'save_code':
                    s_ += d2n(
                        'save_code: <holds ',
                        len(URL_args['save_code'].split('\n')),
                        ' lines>'
                    )
                else:
                    s_ += d2n(u,': ',URL_args[u]) +'\n'
            s += highlight(s_, PythonLexer(), HtmlFormatter())

            s += highlight(
                ansi_escape.sub('', file_to_text(out)),
                PythonLexer(),
                HtmlFormatter())
            s += "</div><hr>"
            #s += div()
            
            #s += '<h4>'+'URL_args'+'</h4>'
            

            
            s += div(150*4)
            s += '<h2>'+'code'+'</h2>'
            s += code
            s += "</div><hr>"

            #s += form_('raw_code',v=raw_code.replace('\n','<br>\n'))
            rows = len(raw_code.split('\n'))
            cols = 80
            s += """

<form action="" method="GET">
<textarea id="save_code" name="save_code" rows="30" cols="80" style="font-family:'Courier New';font-size:14px">
""" + raw_code +"""
  </textarea>
  <br><br>
  <input type="save_code" value="Save">
</form>

"""
#.replace('ROWS',str(rows)).replace('COLS',str(cols))


            s += redirect

            s += "</div>"
            #s += 'end.'

            s += end_()

            print(s)


            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(s, "utf-8"))



    def do_POST(self):
        '''Reads post request body'''
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        self.wfile.write("received post request:<br>{}".format(post_body))


myServer = ThreadingHTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))





#EOF
