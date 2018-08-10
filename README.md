# Isi Analysis

## Note about running Jupyter notebooks
The notebooks assume the existance of a `data` directory at the root level of the repository. However, the `data` directory was too large to include in the repository.
Here is the link to the main dataset: [completed-w-holes-7-26-2018.pkl](https://drive.google.com/open?id=1FFY_hlvYbcmBvi2UzLk4N8CdDF9A4Ptq).
You can either remake the `data` directory or change where the Jupyter notebook reads data from.

## Explanation for what images are in different directory
These are all generated in `PMLB reproduction.ipynb`
 - `bal_accuracy_heatmaps`
 Heat maps for every dataset using the method 'AdaBoostClassifier'. The pictures in `even` have the same scale for every image. 
 The titles for `even` are the `kldiv` between the heatmap and a flat distribution.
 (Probably ignore this metric, I was playing around with different ways to characterize the "clumpiness" of these graphs)
 The pictures in `uneven` have different scales for every image.
 - `best-grid/0.0`
 These are heatmaps where white squares are parameter settings that result in the best balanced accuracy for that dataset using 'AdaBoostClassifier'.
 Notice that some images have more than 1 white square. This happens when multiple parameter settings produce the same balanced accuracy score and this score is the best score.
 - `graphs`
 This is for miscellanenous graphs. Right now there is only one graph here. This is just the reproduction of the PMLB graph that looks similar.
 - `pho-probability-dists`
 These are graphs that are the result of averaging heatmaps like those found in `best-grid`. The name of the file is the tolerance.
 The tolerance is the how close to the best score a parameter setting score can be in order to count as the best.
 
 
