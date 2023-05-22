

def html_tag(tag,Meta={},tabs=0,tabsize=4,content=''):
    if content:
        if type(content) is str:
            content = content.split('\n')
        else:
            content = ('\n'.join(content)).split('\n')
    else: content = []
    assert type(content) is list
    tabbed_content = []
    for c in content:
        cg(c)
        tabbed_content.append( tabsize*(tabs+1)*' '+c )

    cm(tabbed_content)
    s = d2n(tabsize*tabs*' ','<',tag)
    if Meta:
        s += '\n'
        ks = sorted(kys(Meta))
        for i in rlen(ks):
            k = ks[i]
            s += d2n(tabsize*(tabs+1)*' ',k,'=',qtd(Meta[k]))
            if i < len(ks)-1:
                s += '\n'
            else:
                s += ' >'
    else:
        s += '>\n'
    if True:
        s += '\n'.join(tabbed_content) + '\n'
        cm(len(tabsize*tabs*' '))
        s += d2n(tabsize*tabs*' ','</',tag,'>')
    return s


to_name='Jone'
__file__ = 'here/thisfile'



head_html = html_tag(
    'head',
    content=[
        html_tag(
            'link',
            {
                'rel' : 'stylesheet',
                'href' : 'file://'+opj(pname(__file__),'style.css'),
            }
        ),
        html_tag(
            'script',
            content=d2n('to_name = ',qtd(to_name),';')
        ),
        html_tag(
            'script',
            {
                'src' : 'file://'+opj(pname(__file__),'script.js'),
            }
        ),
        html_tag(
            'script',
            {
                'src' : 'file:///Users/karlzipser/Desktop/kMessages/Mymap.js',
            }
        ),
        html_tag(
            'script',
            {
                'src' : 'file:///Users/karlzipser/Desktop/kMessages/setup_people.js',
            }
        ),
        html_tag(
            'title',
            content = to_name
        ),
        html_tag(
            'link',
            {
                'href' : 'file:///Users/karlzipser/favicon.ico',
                'rel' : 'icon',
                'type' : 'image/x-icon',
            },
        ),
    ]
)


print(html_tag('html',content=head_html))

