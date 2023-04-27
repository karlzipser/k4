from k4 import *
from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer
Arguments = get_Arguments(
    {
        'webpage':'k4.utils.html.webpage',
        'quiet':True,
        'name':"localhost",
        'port':9000,
    }
)
exec(d2s('import',Arguments['webpage'],'as wp'))

Images = {}


class MyServer(BaseHTTPRequestHandler):
    if Arguments['quiet']:
        def log_message(self, format, *args):
            return
    def do_GET(self):

        mimetype=None
        if exname(self.path) in ('jpeg','jpg','JPG','JPEG'):
            mimetype='image/jpg'
        elif exname(self.path) in ('png','PNG'):
            mimetype='image/png'
        elif exname(self.path) in ('gif','GIF'):
            mimetype='image/gif'

        if mimetype is not None:
            from urllib.parse import unquote
            try:   
                path_to_image = unquote(opjh(self.path)[1:])
                #cb(path_to_image)
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
            except:
                pass
                #cr('failed to load',path_to_image)#,r=1)

        elif "favicon.ico" in self.path:
            return

        #elif '.py' not in self.path:
        #   return

        else:
            #cr(self.path)
            SubCode = wp.get_SubCode(self.path)

            html = '---WEBPAGE---'

            ks = kys(SubCode)
            ks.remove(html)
            ks = [html] + ks

            for j in ks:
                sc = SubCode[j]
                """
                sc_is_path = False
                try:
                    #print(sc)
                    if j != '---TITLE---' and j != '---PATH-URL---' and len(sggo(sc)) == 1:
                        sc_is_path = True
                except:
                    pass
                """
                if j[0] == '-':
                    sc_is_path = True
                elif j[0] == 't':
                    sc_is_path = False
                else:
                    assert False
                if sc_is_path:
                    #cg(trun(d2s('treating',j,sc,'as path')))
                    try:
                        r = file_to_text(SubCode[j])
                    except:
                        cr('failure with r = file_to_text(SubCode[j])')
                        r = d2s(9*'\n'+j,": Error, unable to find or load",sc)
                        cr(r)
                else:
                    #cy(trun(d2s('treating',j,'as text')))
                    r = SubCode[j]
                #cy(j,r,r=1)
                html = html.replace(j,r)
            
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(html, "utf-8"))



def main(**A):

    hostName = Arguments['name']
    hostPort = int(Arguments['port'])

    myServer = ThreadingHTTPServer((hostName, hostPort), MyServer)
    print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

    try:
        myServer.serve_forever()
    except KeyboardInterrupt:
        pass

    myServer.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))


if __name__ == '__main__':
    main()



#EOF
