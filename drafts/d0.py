#os.environ['GLOG_minloglevel'] = '2'

from k4.utils.arg import *

command_line_args = {
    'paths':'Desktop',
    'file_types':'jpg,jpeg,JPG,JPEG,png,PNG',
    'extent':256,
    'extent2': 350,
    'padval':0,
    'padsize':5,
    'rcratio':1.1,#1.618,
}

def process_args( command_line_args):
    gd = parse_args_to_dict( command_line_args )

    gd['paths'] = gd['paths'].split(',')

    gd['file_types'] = gd['file_types'].split(',')

    if 'print':
        print( 'gd', gd )
        print( gd['paths'], gd['file_types'] )
        print( gd['paths'] )
    return gd





def get_list_of_img_data( gd ):
    img_paths = []

    for p in gd['paths']:
        for f in gd['file_types']:
            img_paths += sggo(p,'*.'+f)

    blank = zeros((gd['extent'],gd['extent'],3),np.uint8)

    list_of_img_data = []

    for p in img_paths:
        print('Loading',p)
        q = Path(p).resolve().as_posix()
        img = zimread(q)
        img = resize_to_extent( img, gd['extent'] )
        img_data = {
            'file':q,
            'extent':gd['extent'],
            #'resized_img':None,
            'square_embeding':None,
            'corner_x':0,
            'corner_y':0,
            #'resized_img':img,
            }

        h,w,d = shape(img)#img_data['resized_img'])
        blank = 0 * blank + gd['padval']
        e2 = gd['extent']//2
        blank[
            e2-h//2 : e2-h//2+h,
            e2-w//2 : e2-w//2+w,
            :d,
        ] = img#img_data['resized_img']
        img_data['square_embeding'] = blank

        list_of_img_data.append( img_data )
        #mi(img_data['square_embeding'])
        #input('enter')

    gd['list_of_img_data'] = list_of_img_data



def make_bkg_image( gd ):
    gd['cols'] = int(gd['rcratio']*sqrt(len(gd['list_of_img_data'])))
    padsize = gd['padsize']
    min_x = 10**9
    min_y = 10**9
    max_x = 0
    max_y = 0
    rows,cols = 0,0
    for I in gd['list_of_img_data']:
        I['corner_x'] = cols * (gd['extent'] + padsize)
        I['corner_y'] = rows * (gd['extent'] + padsize)
        min_x = min(I['corner_x'],min_x)
        min_y = min(I['corner_y'],min_y)
        max_x = max(I['corner_x']+gd['extent'],max_x)
        max_y = max(I['corner_y']+gd['extent'],max_y)
        if cols < gd['cols']-1:
            cols += 1
        else:
            rows += 1
            cols = 0

    bkg = zeros((max_y+2*padsize,max_x+2*padsize,3),np.uint8) + gd['padval']
    for I in gd['list_of_img_data']:
        bkg[
            I['corner_y']+padsize:I['corner_y']+padsize+gd['extent'],
            I['corner_x']+padsize:I['corner_x']+padsize+gd['extent'],:] =\
            I['square_embeding']

    gd['bkg_image'] = bkg
    #_mi()  
    mi( gd['bkg_image'] )
    input()



if __name__ == '__main__':
    gd = process_args( command_line_args )
    get_list_of_img_data( gd )
    make_bkg_image( gd )

#EOF
