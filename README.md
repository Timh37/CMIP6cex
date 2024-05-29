# CMIP6cex
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10817904.svg)](https://doi.org/10.5281/zenodo.10817904)

This repository provides several functionalities to analyze changes in the joint probability of extreme wind speed, storm surges and precipitation in the simulations of CMIP6 models stored on Google Cloud. `CMIP6cex` can efficiently open, manipulate and combine large numbers of CMIP6 simulations using packages like `intake-esm`, `xarray`, `dask` and `xmip`. Scripts for regridding and nearest-neighbour interpolation to tide gauges of these datasets using `xesmf` are provided. Another functionality allows the user to derive storm sturges at tide gauges from simulations of daily mean, gridded wind speed and sea-level pressure from CMIP6 models using the statistical storm surge model of Tadesse et al. (2020) and Tadesse & Wahl (2021). More information about this model and its application to CMIP6 models can be found in Hermans et al. (under review), Projecting Changes in the Drivers of Compound Flooding in Europe Using CMIP6 Models. Users are asked to cite this publication where appropriate.

Additionally, scripts are provided to analyze (future changes in) the number of joint wind speed and precipitation extremes and joint storm surge and precipitation extremes based on the CMIP6 simulations and their storm surge derivatives and to reproduce the figures in Hermans et al. (under review). The analysis of changes in the number of joint extremes includes the decomposition of future changes into changes due to changes in the marginal distributions of the variables and changes in their dependence and various other steps.

To run the scripts in this repository, users need access to the [LEAP-Pangeo cloud-based computing platform](https://leap-stc.github.io/leap-pangeo/architecture.html) or a similar cloud-computing platform. 

## Publications

[Projecting Changes in the Drivers of Compound Flooding in Europe Using CMIP6 Models (Earth's Future, 2024)](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2023EF004188?af=R)
