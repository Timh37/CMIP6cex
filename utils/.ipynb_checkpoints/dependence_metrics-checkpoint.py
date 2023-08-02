from scipy.stats import kendalltau
from statsmodels.distributions.empirical_distribution import ECDF
import numpy as np

#to-do: annotate
def kendallstau(x,y):
    overlap = np.isfinite(x) * np.isfinite(y)
    
    tau = kendalltau(x[overlap],y[overlap])
    
    return np.array([tau[0],tau[1]])

def empirical_copula(x,y,x_thr,y_thr):
    #based on and validated against pycop
    
    overlap = np.isfinite(x) * np.isfinite(y)
    x = x[overlap]
    y = y[overlap]
    
    n = len(x) #number of obs
    
    x_sorted = sorted(x) #ranked x & y
    y_sorted = sorted(y)
    
    i = int(round(n*x_thr))-1 #translate threshold percentile to index
    j = int(round(n*y_thr))-1
    
    #count number of x,y pairs below ranked x[i],y[j]
    return np.sum((x<=x_sorted[i]) & (y<=y_sorted[j])) / n 

def utdc_at_threshold(x,y,thr=.95):
    #based on and validated against pycop
    
    #See also: https://stats.stackexchange.com/questions/72999/understanding-tail-dependence-coefficients
    
    #For u,v continuous random variables with margins f,g, then in the limit of 
    #treshold->1, utdc = P{u>g-1(threshold)|v>f-1(threshold)}. This function evaluates that at a given threshold.
    if (thr<0) or (thr>=1):
        raise Exception('Threshold must be between 0 and 1.')
    
    overlap = np.isfinite(x) * np.isfinite(y)
    x = x[overlap]
    y = y[overlap]
    
    n = len(x) #number of obs
    
    if n==0:
        return np.array([ np.nan,np.nan ])
    
    i = int(round(n * thr))
    if i == 0:
        return 0
    
    return np.array([ (1-2*(i/n) + empirical_copula(x,y,thr,thr) ) / (1-(i/n)),
                     np.nan ]) #np.nan is place holder for p-value that needs to be implemented


def pseudo_obs(x,y):
    overlap = np.isfinite(x) * np.isfinite(y)
    x = x[overlap]
    y = y[overlap]
    
    n = len(x)
    
    if n==0:
        return np.nan*x,np.nan*y
    
    ecdf_x = ECDF(x)
    ecdf_y = ECDF(y)

    scaled_ranks_x = np.array([n * l / (n + 1) for l in ecdf_x(x)])
    scaled_ranks_y = np.array([n * l / (n + 1) for l in ecdf_y(y)])

    return scaled_ranks_x, scaled_ranks_y

def utdc_cfg(x,y):
    #estimate upper tail dependence coefficient using the Capéraá–Fougéres–Genest estimator.
    
    #(https://www.sciencedirect.com/science/article/pii/S016766870500065X, see also Paprotny et al. (2020))
     
    #bivariates
    overlap = np.isfinite(x) * np.isfinite(y)
    x = x[overlap]
    y = y[overlap]
 
    n = len(x)
    
    if n==0:
        return np.array([ np.nan,np.nan ])
    
    #compute pseudo-obs (rescaled ECDFs)
    scaled_ranks_x,scaled_ranks_y = pseudo_obs(x,y)
    max_ecdf = np.max(np.vstack([scaled_ranks_x,scaled_ranks_y]),axis=0)
     
    return np.array([ 2-2*np.exp( 1/n * np.sum(np.log(np.sqrt(np.log(1/scaled_ranks_x)*np.log(1/scaled_ranks_y))/np.log(1/(max_ecdf**2)) ) )),
                     np.nan ]) #np.nan is place holder for p-value that needs to be implemented
