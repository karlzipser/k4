from k3 import *
import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F

#CA()


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


if 'classes' not in locals():
    transform = transforms.Compose(
        [transforms.ToTensor(),
         transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    batch_size = 16

    trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                            download=True, transform=transform)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                              shuffle=True, num_workers=2)

    testset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                           download=True, transform=transform)
    testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                             shuffle=False, num_workers=2)

    classes = ('plane', 'car', 'bird', 'cat',
               'deer', 'dog', 'frog', 'horse', 'ship', 'truck')


    dot_files = sggo(opjh('data/dots/*.png'))
    Dots = {}
    for d in dot_files:
        n = int(fname(d).split('.')[0])
        img = z2o(cv2.blur(zimread(d)[:,:,0],(7,7)).astype(np.float))
        #img = z2o(zimread(d)[:,:,0]).astype(np.float)
        Dots[n] = img.flatten()
        





class Fire(nn.Module):
    def __init__(
        self,
        inplanes,
        squeeze_planes,
        expand1x1_planes,
        expand3x3_planes,
        name='',
        A={}
    ):
        super(Fire, self).__init__()
        self.A = A
        self.name = name
        self.inplanes = inplanes
        self.squeeze = nn.Conv2d(inplanes, squeeze_planes, kernel_size=1)
        self.squeeze_activation = nn.ReLU(inplace=True)
        self.expand1x1 = nn.Conv2d(squeeze_planes, expand1x1_planes,
                                   kernel_size=1)
        self.expand1x1_activation = nn.ReLU(inplace=True)
        self.expand3x3 = nn.Conv2d(squeeze_planes, expand3x3_planes,
                                   kernel_size=3, padding=1)
        self.expand3x3_activation = nn.ReLU(inplace=True)

    def forward(self, x):
        x = self.squeeze_activation(self.squeeze(x))
        return torch.cat([
            self.expand1x1_activation(self.expand1x1(x)),
            self.expand3x3_activation(self.expand3x3(x))
        ], 1)



a = 3
b = 64
d = 2*b




class SqueezeNet(nn.Module):
    def __init__(self,net_name):
        super().__init__()
        self.net_name = net_name
        self.a = nn.Conv2d(a, d, kernel_size=3, stride=2)
        self.b = nn.ReLU(inplace=True)
        self.c = nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True)
        self.d = Fire(d, b, d, d)            
        self.e = Fire(d+d, b, d, d)
        #self.f = nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True)
        #self.g = Fire(e, c, e, e)
        #self.i = Fire(e+e, c, e, e)
        #self.j = nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True)
        self.k = nn.Upsample((32,32),mode='nearest')
        self.k2 = nn.Upsample((64,64),mode='nearest')
        self.k3 = nn.Upsample((96,96),mode='nearest')
        self.l = nn.Conv2d(
            in_channels=d+d,
            out_channels=a,
            padding=1,
            kernel_size=3)
        self.m = nn.ConvTranspose2d(
            in_channels=d+d,
            out_channels=d+d,
            kernel_size=3,
            stride=2,
            output_padding=(0,0),
        )
        self.n = nn.ConvTranspose2d(
            in_channels=d+d,
            out_channels=3,
            kernel_size=3,
            stride=2,
            output_padding=(1,1),
        )
        self.o = nn.AvgPool2d(2, stride=2)

    def forward(self,x,print_shape=False,use_deconv=False):
        #use_deconv=True
        x = self.k3(x)

        x = self.a(x)
        
        x = self.b(x)
        
        x = self.c(x)
        
        x = self.d(x)
        
        x = self.e(x)

        if use_deconv:
            x = self.b(self.m(x))
            x = self.n(x)
            x = self.k(x)
        else:
            x = self.k(x)
            x = self.l(x)
            
            

        return x


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.aa = SqueezeNet('aa')
        self.bb = SqueezeNet('bb')
        self.cc = SqueezeNet('cc')
        self.dd = SqueezeNet('dd')
        self.zz = nn.Conv2d(
            in_channels=3,##
            out_channels=1,
            padding=1,
            kernel_size=3)
        self.A = {}
    def forward(self,x,print_shape=False):
        self.A['input'] = torch.clone(x)
        #y = self.dd(x,use_deconv=True)
        x = self.aa(x,use_deconv=False)

        #y = self.dd(x,use_deconv=False)
        self.A[0] = torch.clone(x)
        x = self.bb(x,use_deconv=False)
        #y = self.dd(x,use_deconv=False)
        
        self.A[1] = torch.clone(x)
        x = self.cc(x,use_deconv=False)
        y = self.dd(x,use_deconv=False)
        self.A[3] = torch.clone(y)
        self.A[2] = torch.clone(x)
        x = self.zz(x)
        x = torch.cat((x,y),1)
        return torch.flatten(y, 1)


def from_1024_to_32x32(t):
    a = t.cpu().numpy()
    return a.reshape(32,32)



net = Net()
net.to(device)

N = 200
print_shape = True
save_timer = Timer(300)
show_timer = Timer(7)
ftimer = Timer(10)

import torch.optim as optim
criterion = nn.MSELoss()
#optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.1)
optimizer = optim.Adam(net.parameters(), lr=0.001)
first_time = False
loss_list = []
running_loss = 0.0
ctr = 0

scale_factor = 1/2.

for epoch in range(400):  # loop over the dataset multiple times

    for i, data in enumerate(trainloader, 0):
        ctr += 1
        if ftimer.rcheck():
            print('ftimer',dp(ctr/ftimer.time_s))
            ctr = 0
        inputs, labels = data
        inputs0 = 1.0 * inputs
        for i in range(inputs.size()[0]):
            #cg()
            #print(inputs[i,:].size())
            a = inputs[i,:]
            #print(a.size())
            b = F.interpolate(a.unsqueeze(0), scale_factor=scale_factor, mode='nearest')
            #print(b.size())
            
            inputs[i,1,:] = F.interpolate(b, scale_factor=1/scale_factor, mode='nearest').squeeze(0)[1,:]
            inputs[i,0,:] = inputs[i,1,:]
            inputs[i,2,:] = inputs[i,1,:]
            #print(inputs.size())
        inputs = inputs.to(device)
        labels_ = labels.numpy()
        labels2 = []
        for i_ in range(batch_size):
            labels2.append(Dots[labels_[i_]])
        labels2 = na(labels2)
        labels2 = torch.from_numpy(labels2).float()
        labels2 = labels2.to(device)
        optimizer.zero_grad()


        outputs = net(inputs,print_shape)
        print_shape = True

        loss = criterion(outputs,torch.flatten(inputs0,1))

        
        loss.backward()
        optimizer.step()


        running_loss += loss.item()
        

        if save_timer.rcheck():
            PATH = opjD('net8c-up64.pth')
            torch.save(net.state_dict(), PATH)

        if show_timer.rcheck():

            loss_list.append(running_loss/N)
            first_time = False   
            print('[%d, %5d] loss: %.6f' %
                  (epoch + 1, i + 1, running_loss / N))


            running_loss = 0.0

            images = []
            for k in [0,1,2,3]:
                #figure(k,figsize=(2,2));clf()
                img = z55(net.A[k].detach().cpu().numpy()[0,:].transpose(1,2,0))
                #mi(img,k);spause()
                images.append(img)

            #images.append(from_1024_to_32x32(outputs[0,:(32*32)].detach()))
            
            figure('loss',figsize=(2,2));clf()
            plot(loss_list);spause()

            #spause()
            #figure(100,figsize=(2,2));clf()
            images.append(z55(inputs[0,:].cpu().numpy().transpose(1,2,0)))
            images.append(z55(inputs0[0,:].cpu().numpy().transpose(1,2,0)))
            #cm(0,r=1)
            mi(np.concatenate(images,axis=1),'images')
            spause()

        #raw_enter()
print('Finished Training')

raw_enter()




#EOF
