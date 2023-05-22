
from k4 import *
from k4.utils.core.arrays import *

if interactive():
  __file__ = opjk('misc/msg_reader/format.py')



def messages_to_js_map_str(
    Person,
    Messages,
    A,
):
    A = limD(A,[
        'my_first_name','width',
        'img_width','time_gap_between_dates','max_wordlength',
        'msg_count_date_gap','Attachments',
        ],)

    import html

    M = Messages
    jsMessages = {}

    Dates = {}

    Chat_identifiers = {}

    to_name = Person['name']['first']

    from_name = A['my_first_name']
  
    _t_prev = 0
    _msg_count = 0

    ts = []
    message_rowids = []
    for k in M:
        ts.append(M[k]['message.date'])
        message_rowids.append(M[k]['message.rowid'])

    date_sorted = na(ts).argsort()

    loop_range = rlen(date_sorted)    


    for j in loop_range:

        i = date_sorted[j]

        rowid = message_rowids[i]

        me = M[rowid]['message.is_from_me']
        
        if i < len(message_rowids) - 1:
            if me == M[message_rowids[i+1]]['message.is_from_me']:
                _last = False
            else:
                _last = True
        else:
            _last = True

        t = M[rowid]['message.date']

        if len(M[rowid]['Attachments']):
            _attachment_modifier = '_with_attachment'
        else:
            _attachment_modifier = ''


        _message_identifier = rowid
        _message_identifier = d2n(to_name,'_',t)


        message_html = [
            '\n'+8*' '+'<!--==================================================================-->',
            d2n(8*' ','<div class="message_div',_attachment_modifier,'" id="',_message_identifier,'">'),
            d2n(12*' ','<div class="',get_safe_name(M[rowid]['chat.chat_identifier']),'">'),
        ]


        date_html = []
        if (t - _t_prev)/1000000000 > A['time_gap_between_dates'] or _msg_count > A['msg_count_date_gap']:
            date_html = [
                12*' '+'<div class="date'+_attachment_modifier+'">',
                d2n(16*' '+'<a id="a_date_',_message_identifier,'">'),
                16*' '+M[rowid]['date'],
                12*' '+'</div>  <!--date-->',
            ]
            _msg_count = -1

        if True:
            #
            if not _t_prev <= t:
                cE('not _t_prev <= t',_t_prev//1000000000, t//1000000000, (_t_prev - t)//(1*1000000000))
                #time.sleep(4)

        _t_prev = t
        _msg_count += 1
        

        message_html += date_html
        

        message_html.append(
            d2n(12*' '+'<div class="timestamp',
                _attachment_modifier+'" id="timestamp_',
                _message_identifier,'">',
                _message_identifier,' ',M[rowid]['chat.chat_identifier'],' ',
                M[rowid]['date'],'</div>'
            )
        )

        if M[rowid]['chat.chat_identifier'] not in Chat_identifiers:
            Chat_identifiers[ M[rowid]['chat.chat_identifier'] ] = 0
        Chat_identifiers[ M[rowid]['chat.chat_identifier'] ] += 1

        if me:

            if 'sms' in M[rowid]['message.service'].lower():
                message_html.append(12*' '+'<div class="mine_sms messages">')
            else:
                message_html.append(12*' '+'<div class="mine messages">')

        else:
            message_html.append(12*' '+'<div class="yours messages">')

        



        for B in M[rowid]['Attachments']:

            f = B['attachment.filename']

            if exname(f).lower() == 'heic':
                f = f +'.jpg'
            if f:
                if 'Attachments' in f:
                    f_s = f.split('Attachments/')
                    f = opj(A['Attachments'],f_s[1])
                    f = 'file://'+f.replace('~/',opjh())
                else:
                    cE(f)
                fn = fname(f)
                if len(fn) > A['max_wordlength']:
                    fn = fn[:A['max_wordlength']]+'...'

                if str(B['attachment.mime_type']) not in [
                    'video/mp4',
                    #'image/heic',
                    'application/pdf',
                    'image/png',
                    'image/gif',
                    #'text/x-python-script',
                    #'text/x-vlocation',
                    'image/jpeg',
                    #'audio/x-m4a',
                    #'application/zip',
                    'None',
                    'video/quicktime',
                    #'text/vcard',
                    #'text/rtf'
                    ]:
                    message_html.append(str(B['attachment.mime_type'])+'<br>')

                message_html += [
                    16*' '+'<!--****************************************************-->',
                    16*' '+'<a href="' + f + '"> <img src="' + f + '" alt="' + fn \
                        + '" style="max-width:'+str(A['img_width'])+'px"></a><br>',
                    16*' '+'<!--****************************************************-->',
                ]


        if _last:
             message_html.append(16*' '+'<div class="message last">')
        else:
            message_html.append(16*' '+'<div class="message">')


        if M[rowid]['message.text']:
            txt = M[rowid]['message.text'].split(' ')
            for j in rlen(txt):
                if len(txt[j]) > A['max_wordlength']:
                    txt[j] = txt[j][:A['max_wordlength']]+'...'
            tx = ' '.join(txt)
            tx = html.escape(tx).encode('ascii', 'xmlcharrefreplace').decode("utf-8")
            tx = tx.replace('\n','\n<br>')

            message_html.append( 20*' '+tx )

        message_html.append(16*' '+'</div> <!--message (last?)-->')
        message_html.append(12*' '+'</div> <!--mine/yours-->')
        message_html.append(12*' '+'</div> <!--chat_identifier-->')
        message_html.append(8*' '+'</div> <!--message_div-->')

        jsMessages[_message_identifier] = message_html



    ks = sorted(kys(jsMessages))
    js = ['var Messages = {']
    for k in ks:
        js.append( d2s( qtd(k,s=1), ': `\n', '\n'.join(jsMessages[k]),'\n`,\n') )
    js.append('}\n')

    messages_js_str = '\n'.join(js)

    return messages_js_str




#EOF


