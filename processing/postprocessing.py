import os
import numpy as np
from processing.resmaps import ResmapCalculator
from processing.utils import printProgressBar, is_rgb
import matplotlib.pyplot as plt
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResmapPlotter:
    def __init__(
        self, imgs_input, imgs_pred, filenames, color="grayscale", vmin=0.0, vmax=1.0,
    ):
        self.imgs_input = imgs_input
        self.imgs_pred = imgs_pred
        self.filenames = filenames
        self.vmin = vmin
        self.vmax = vmax

        if color == "grayscale":
            self.RC_ssim = ResmapCalculator(
                imgs_input=imgs_input,
                imgs_pred=imgs_pred,
                color="grayscale",
                method="ssim",
                filenames=filenames,
                vmin=vmin,
                vmax=vmax,
                dtype="float64",
            )
        else:
            self.RC_ssim = ResmapCalculator(
                imgs_input=imgs_input,
                imgs_pred=imgs_pred,
                color="rgb",
                method="mssim",
                filenames=filenames,
                vmin=vmin,
                vmax=vmax,
                dtype="float64",
            )

        self.RC_l1 = ResmapCalculator(
            imgs_input=imgs_input,
            imgs_pred=imgs_pred,
            color=color,
            method="l1",
            filenames=filenames,
            vmin=vmin,
            vmax=vmax,
            dtype="float64",
        )

        self.RC_l2 = ResmapCalculator(
            imgs_input=imgs_input,
            imgs_pred=imgs_pred,
            color=color,
            method="l2",
            filenames=filenames,
            vmin=vmin,
            vmax=vmax,
            dtype="float64",
        )

    # Method for generating and plotting Resmaps for inspection

    def generate_inspection_figure(self):
        # if filenames_plot != []:
        #     indicies = [self.filenames.index(filename) for filename in filenames_plot]
        # else:
        indicies = list(range(len(self.imgs_input)))

        nrows = len(indicies)
        ncols = 5

        printProgressBar(0, nrows, prefix="Progress:", suffix="Complete", length=80)

        fig, axarr = plt.subplots(nrows=nrows, ncols=ncols, figsize=(25, 5 * nrows))
        for i, j in enumerate(indicies):
            axarr[i, 0].imshow(
                self.imgs_input[j], vmin=self.vmin, vmax=self.vmax, cmap=None
            )
            axarr[i, 0].set_title("Input\n{}".format(self.filenames[j]))
            axarr[i, 0].set_axis_off()

            axarr[i, 1].imshow(
                self.imgs_pred[j], vmin=self.vmin, vmax=self.vmax, cmap=None
            )
            axarr[i, 1].set_title("Reconstruction\n{}".format(self.filenames[j]))
            axarr[i, 1].set_axis_off()

            # resmap ssim gray
            res_ssim = axarr[i, 2].imshow(
                X=self.RC_ssim.resmaps[j],
                vmin=self.RC_ssim.vmin_resmap,
                vmax=self.RC_ssim.vmax_resmap,
                cmap=self.RC_ssim.cmap_resmap,
            )
            axarr[i, 2].set_title(
                "Resmap SSIM\n" + f"score = {self.RC_ssim.scores[j]:.2E}"
            )
            axarr[i, 2].set_axis_off()
            if self.RC_ssim.color == "grayscale":
                fig.colorbar(res_ssim, ax=axarr[i, 2])

            # resmap l1 gray
            res_l1 = axarr[i, 3].imshow(
                X=self.RC_l1.resmaps[j],
                vmin=self.RC_l1.vmin_resmap,
                vmax=self.RC_l1.vmax_resmap,
                cmap=self.RC_l1.cmap_resmap,
            )
            axarr[i, 3].set_title("Resmap_L1\n" + f"score = {self.RC_l1.scores[j]:.2E}")
            axarr[i, 3].set_axis_off()
            if self.RC_l1.color == "grayscale":
                fig.colorbar(res_l1, ax=axarr[i, 3])

            # resmap l2 gray
            res_l2 = axarr[i, 4].imshow(
                X=self.RC_l2.resmaps[j],
                vmin=self.RC_l2.vmin_resmap,
                vmax=self.RC_l2.vmax_resmap,
                cmap=self.RC_l2.cmap_resmap,
            )
            axarr[i, 4].set_title("Resmap_L2\n" + f"score = {self.RC_l2.scores[j]:.2E}")
            axarr[i, 4].set_axis_off()
            if self.RC_l2.color == "grayscale":
                fig.colorbar(res_l2, ax=axarr[i, 4])

            plt.tight_layout()

            printProgressBar(
                i + 1, nrows, prefix="Progress:", suffix="Complete", length=80
            )
        return fig

    # Method for plotting Resmaps' scores for inspection

    # def generate_score_scatter_plot(
    #     self, generator_test, model_path=None, filenames_plot=[]
    # ):
    #     if filenames_plot != []:
    #         indicies_to_plot = [
    #             self.filenames.index(filename) for filename in filenames_plot
    #         ]
    #     else:
    #         indicies_to_plot = list(range(len(self.imgs_input)))

    #     R_list = [self.RC_ssim, self.RC_l1, self.RC_l2]
    #     method_list = ["ssim", "l1", "l2"]
    #     with plt.style.context("dark_background"):
    #         fig, axarr = plt.subplots(nrows=3, ncols=1, figsize=(15, 24))
    #         if model_path:
    #             fig.suptitle(model_path, fontsize=16)
    #         for i, (R, method) in enumerate(list(zip(R_list, method_list))):
    #             for category in list(generator_test.class_indices.keys()):
    #                 indicies_cat = np.nonzero(
    #                     generator_test.classes == generator_test.class_indices[category]
    #                 )[0]
    #                 # if filenames_plot != []:
    #                 #     indicies_cat = list(
    #                 #         set.intersection(set(indicies_cat), set(indicies_to_plot))
    #                 #     )
    #                 scores = R.scores[indicies_cat]
    #                 marker = "s" if category == "good" else "."
    #                 # markersize = 6 if category == "good" else 4
    #                 axarr[i].scatter(
    #                     indicies_cat, scores, alpha=0.5, marker=marker, label=category
    #                 )
    #             axarr[i].set_xlabel("image index")
    #             axarr[i].set_ylabel(method.upper() + "_score")
    #             axarr[i].legend()
    #     return fig


## functions for processing resmaps


def label_images(images_th):
    images_labeled = np.zeros(shape=images_th.shape)
    areas_all = []
    for i, image_th in enumerate(images_th):
        # close small holes with binary closing
        # bw = closing(image_th, square(3))

        # remove artifacts connected to image border
        cleared = clear_border(image_th)

        # label image regions
        image_labeled = label(cleared)

        # image_labeled = label(image_th)

        # append image
        images_labeled[i] = image_labeled

        # compute areas of anomalous regions in the current image
        regions = regionprops(image_labeled)

        if regions:
            areas = [region.area for region in regions]
            areas_all.append(areas)
        else:
            areas_all.append([0])

    return images_labeled, areas_all
