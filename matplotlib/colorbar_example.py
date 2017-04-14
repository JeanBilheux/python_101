from pylab import *
close('all') #close all figures in memory

#1. Figures for fig.clf method
fig1 = figure()
fig2 = figure()
cbar1=None
cbar2=None
data = rand(250, 250)

def makefig(fig,cbar):
    fig.clf()
    ax = fig.add_subplot(111)
    im = ax.imshow(data)
    if cbar:
        cbar=None
    else:
        cbar = fig.colorbar(im)
    return cbar


#2. Update method
fig_update = figure()
cbar3=None
data_update = rand(250, 250)
img=None

def makefig_update(fig,im,cbar,data):
    if im:
        data*=2 #change data, so there is change in output (look at colorbar)
        #im.set_data(data) #use this if you use new array
        im.autoscale()
        #cbar.update_normal(im) #cbar is updated automatically
    else:
        ax = fig.add_subplot(111)
        im = ax.imshow(data)
        cbar=fig.colorbar(im)
    return im,cbar,data

#Execute functions a few times
for i in range(3):
    print(i)
    cbar1=makefig(fig1,cbar1)
    cbar2=makefig(fig2,cbar2)
    img,cbar3,data_update=makefig_update(fig_update,img,cbar3,data_update)
cbar2=makefig(fig2,cbar2)

fig1.show()
fig2.show()
fig_update.show()