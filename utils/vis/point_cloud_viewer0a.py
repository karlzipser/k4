from k4 import *

class Viewer:
    def __init__(
        _,
        xyzs,
        xmin=-5,
        xmax=5,
        ymin=-5,
        img_width=300,
        img_height=300,
        color=(255,255,0),
        title='Viewer',
    ):
        assert len(shape(xyzs)) == 2
        assert shape(xyzs)[1] == 3
        _.xyzs = zeros((shape(xyzs)[0],4))
        _.color = color
        #cm(_.test)
        #setattr(_,'test',2)
        #cm(_.test,r=1)
        #cm(shape(getattr(_,'xyzs')))
        _.xyzs[:,:3] = xyzs
        _.xyzs[:,3] = 1
        _.xmin = xmin
        _.xmax = xmax
        _.ymin = ymin
        _.transform = get_IdentityMatrix()
        _.zgraph = ZGraph(img_width,img_height,title)
        _.zgraph.add(1.0*_.xyzs[:,:2], _.color)#rndint(255,size=(len(xyzs),3)))#(255,255,255))
        _.zgraph.graph(_.xmin,_.xmax,_.ymin)
        _.zgraph.show()
        _.transformation_list = []
        _.help_str = """'h' : help
        'u' : undo last transformation
         x<float> : rotate along x axis <float> degrees
             e.g., x9.3
         y<float> : rotate along y axis <float> degrees
         z<float> : rotate along z axis <float> degrees
         e<float> : translate along x axis
         r<float> : translate along y axis
         t<float> : translate along z axis
         l : show transformation_list
         # change xymin,xymax
         # allow running from commandline with point cloud file
         # path, cloud index
         # plot size as argument
        """
        box(_.help_str)
        _.Transformations = {
            'x' : get_xRotationMatrix,
            'y' : get_yRotationMatrix,
            'z' : get_zRotationMatrix,
            's' : get_xyzScalingMatrix,
            'e' : get_xTranslationMatrix,
            'r' : get_yTranslationMatrix,
            't' : get_zTranslationMatrix,
        }

    def attributes_to_dict(lst):
        U = {}
        for name in lst:
            U[name] = getattr(_,name)
        return U




    def get_img(_):
        xyzs_ = _.xyzs @ _.transform
        _.zgraph.add(xyzs_[:,:2],_.color)
        _.zgraph.graph(_.xmin,_.xmax,_.ymin)
        return _.zgraph.img

    def interactive_loop(_):
        while True:
            A = None
            undo = False
            s = input('command > ')
            if s == 'q':
                break
            if not s:
                continue
            if s[0] == 'h':
                box(_.help_str)
            elif s[0] in _.Transformations.keys() and len(s) > 1:
                value = s[1:]
                if str_is_float(value):
                    value = float(value)
                    A = _.Transformations[s[0]](value)
                    print(s[0],value,'\n',A)
                else:
                    cE(qtds(value),'not float')
                    continue
            elif s[0] == 'u':
                undo = True
                if len(_.transformation_list):
                    print('undo',_.transformation_list[-1][0])
                else:
                    print('\tTransformation_list is empty.')
            elif s[0] == 'l':
                print('transformation_list:')
                for a in _.transformation_list:
                    print(a[0],'\n',a[1])
            else:
                print('\tHuh?')
                continue
            _.zgraph.clear()
            if not is_None(A):
                _.transformation_list.append( (s,A) )
            if len(_.transformation_list):
                B = _.transformation_list[0][1]
                if undo:
                    _.transformation_list.pop()
                if len(_.transformation_list) > 0:
                    for C in _.transformation_list[1:]:
                        B = B @ C[1]
                _.transform = B
                xyzs_ = _.xyzs @ _.transform
            else:
                xyzs_ = 1.0 * _.xyzs
            _.zgraph.add(xyzs_[:,:2],_.color)
            _.zgraph.graph(_.xmin,_.xmax,_.ymin)
            _.zgraph.show()



if __name__ == '__main__':
    
    xyzs = rndn(1000,3)
    xyzs[:,0] *= 0.1
    xyzs[:,1] *= 0.03
    xmin,xmax,ymin = -1,1,-1

    v = Viewer(xyzs,xmin,xmax,ymin,color=rndint(255,size=(len(xyzs),3)))

    if False:
        mi(v.get_img(),'img')
        spause()

    v.interactive_loop()

#EOF
