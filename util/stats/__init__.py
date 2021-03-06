import os
from util.math import abs_diff, SMALL
from util.random import pairs

# Import "numpy" by modifying the system path to remove conflicts.
import sys
_ = []
for i in range(len(sys.path)-1,-1,-1):
    if "util/util" in sys.path[i]: _ = [sys.path.pop(i)] + _
import numpy as np
sys.path = _ + sys.path


# Import all of the submodules so that users can access all from "util.stats".
from util.stats.rank          import *
from util.stats.ks            import *
from util.stats.difference    import *
from util.stats.distributions import *
from util.stats.samples       import *
from util.stats.modes         import *
from util.stats.metric_pca    import *
from util.stats.plotting      import *

# Backwards compatibility with warning for deprecation.

def cdf_fit_func(*args, **kwargs):
    print("\nWARNING: 'cdf_fit_func' is a deprecated function. Use 'cdf_fit' instead.\n")
    return cdf_fit(*args, **kwargs)

def pdf_fit_func(*args, **kwargs):
    print("\nWARNING: 'pdf_fit_func' is a deprecated function. Use 'pdf_fit' instead.\n")
    return pdf_fit(*args, **kwargs)


# ../../development/testing/test_stats.py 
if __name__ == "__main__":
    from util.random import cdf
    np.random.seed(1)
    data = cdf()
    
    from util.random import cdf
    np.random.seed(1)
    data = cdf(nodes=3).inverse(np.random.random(100))
    # modes(data)

    # Look for "largest" regions of separation 

