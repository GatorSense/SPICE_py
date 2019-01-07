import pickle
from SPICE import *
import matplotlib.pyplot as plt
from loadmat import loadmat

def main():

    # load the data 
    hsi_image = loadmat('danforth_plant_ds551.mat')['plant']

    # trim the noisy bands
    img_shape = hsi_image.shape
    n_r, n_c, n_b = hsi_image.shape

    # reshape the data because SPICE takes an MxN array, not a full HSI cube
    hsi_image = np.reshape(hsi_image, (img_shape[0]*img_shape[1], img_shape[2]))
    # take the hsi data at the "valid" points

    M = hsi_image

    # down sample the data for the sake of time in this demo
    input_data = M.T.astype(float)
    ds_data = input_data[:, ::20]

    # get the default parameters from the SPICE.py file
    params = SPICEParameters()

    # run the spice algorithm on the down sampled data
    [endmembers, ds_proportions] = SPICE(ds_data, params)

    # prompt the user to see if they would like to graph the output
    if input('Would you like to plot the output? (Y/n): ') == 'n':
        return

    # plot the wavelength versus the reflectance
    n_em = endmembers.shape[1]
    plt.plot(endmembers)
    plt.legend([str(i + 1) for i in range(n_em)])
    plt.title('SPICE Endmembers')

    # unmix the data using the non-downsampled array and the endmembers that SPICE discovered
    s = input_data.max()
    P = unmix_qpp(input_data/s, endmembers/s)

    # re-ravel abundance maps
    P_imgs = []
    for i in range(n_em):
        map_lin = P[:, i]
        P_imgs.append(np.reshape(map_lin, (n_r, n_c)))

    # display abundance maps in the form of a subplot
    fig, axes = plt.subplots(2, int(n_em/2) + 1, squeeze=True)
    for i in range(n_em):
        im = axes.flat[i].imshow(P_imgs[i], vmin=0, vmax=1)
        axes.flat[i].set_title('SPICE Abundance Map %d' % (i + 1))

    # add the original RGB image to the subplot
    # im = axes.flat[n_em].imshow(hsi['RGB'])
    # axes.flat[n_em].set_title('RGB Image')
    # fig.colorbar(im, ax=axes.ravel().tolist())

    # # delete any empty subplots
    # if (n_em % 2 == 0):
    #     fig.delaxes(axes.flatten()[(2*(int(n_em/2)+1)) -1])
    plt.show()
    

# run the main method
if __name__ == '__main__':
    main()