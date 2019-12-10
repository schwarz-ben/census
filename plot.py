from scipy import histogram2d as h2d
import numpy as np
DEFAULT_NB_BINS_FOR_2D_HISTO=(35,35)
DEFAULT_DENSITY_DOT_THRESHOLD=0
DEFAULT_NB_BINS_FOR_HISTO=100
def histo2d( plt_figure, dots,threshold=DEFAULT_DENSITY_DOT_THRESHOLD,**kwargs):
    """ draw a colormap matrix expressing the density of dots in the plane
    :param axes plt_figure: (mandatory)
    :param list dots: (mandatory) a list of points to be plotted
    :param int threshold: (optional) density value under which density is white and dots are plotted
    :keyword tuple or list xyrange: (optional) format ((x_min,x_max),(y_min,y_max)), if empty list use min and max values on each axes, if None use values from plt_figure
    :keyword tuple or list bins: (xbins, ybins) nb bins on the X and Y axis
    :keyword boolean plot_low_densities: (True) shall I plot the points under
    :keyword str low_densities_dot_color: optional) default ('b')
    :keyword str low_densities_dot_marker: (',')
    :keyword boolean plot_color_bar: (False) shall I draw the colorbar associated to the density
    :keyword axes colorbar_axe: allows one to specify a (sub)figure in which to draw the colorbar
    """

    xyrange = kwargs.get("xyrange")
    if xyrange == None :
        xyrange = (plt_figure.get_xlim(),plt_figure.get_ylim())

    bins = kwargs.get("bins")
    if bins == None:
        bins = DEFAULT_NB_BINS_FOR_2D_HISTO

    plot_low_densities = kwargs.get("plot_low_densities")
    if plot_low_densities == None :
        plot_low_densities = True

    low_densities_dot_color = kwargs.get("low_densities_dot_color")
    if low_densities_dot_color == None :
        low_densities_dot_color = "b"

    low_densities_dot_marker = kwargs.get("low_densities_dot_marker")
    if low_densities_dot_marker == None :
        low_densities_dot_marker = ","

    plot_color_bar = kwargs.get("plot_color_bar")
    if plot_color_bar == None :
        plot_color_bar = False
    else :
        del(kwargs["plot_color_bar"])

    colorbar_axe = kwargs.get("colorbar_axe")
    if colorbar_axe != None :
        print("colorbar_axe<<")
        del(kwargs["colorbar_axe"])

    X= np.array([ dot[0] for dot in dots ])
    Y= np.array([ dot[1] for dot in dots ])
    if xyrange == () or xyrange == []:
        xyrange = ( (min(X),max(X)), (min(Y),max(Y)) )

    hh, locx, locy = h2d(X, Y, range=xyrange, bins=bins)
    posx = np.digitize(X, locx)
    posy = np.digitize(Y, locy)
    #select points within the histogram
    ind = (posx > 0) & (posx <= bins[0]) & (posy > 0) & (posy <= bins[1])

    hhsub = hh[posx[ind] - 1, posy[ind] - 1] # values of the histogram where the points are
    xdat1 = X[ind][hhsub < threshold] # low density points
    ydat1 = Y[ind][hhsub < threshold]
    hh[hh < threshold] = np.nan # fill the areas with low density by NaNs
    im=plt_figure.imshow(hh.T[::-1],cmap='jet',extent=np.array(xyrange).flatten(), interpolation='nearest',aspect='auto')
    if plot_low_densities == True :
        plt_figure.plot(xdat1, ydat1, color=low_densities_dot_color, marker = low_densities_dot_marker, linestyle="None")

    if plot_color_bar :
        current_fig = plt.gcf()
        if colorbar_axe == None :
            c_kwarg = {}
        else :
            c_kwarg={"cax":colorbar_axe}
            print("colorbar_axe",colorbar_axe)
        current_fig.colorbar(im,**c_kwarg)

def test_histo2d():
    import matplotlib.pyplot as plt

    points = [ (a,(a+b)**2) for a in range(-10,10,1) for b in [1,2,-.5,.5,6]]
    histo2d(plt.axes(),points,xyrange=[],bins=(5,5))
    plt.show()

if __name__ == "__main__":
    test_histo2d()
