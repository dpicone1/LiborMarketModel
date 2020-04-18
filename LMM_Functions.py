import numpy as np
from scipy.interpolate import splrep, splev

# functions to price 
# 1 . Swaption receiver
# 2 . ZCB and to calculate
# 3 . continously compounded forward and spot rates, from DFs
# 4 . cubic spline 
def ZCB(FwdRates):
    size = len(np.zeros(len(FwdRates)))

    # Prerare the forward discount factors    
    FDFs = 1/(1+FwdRates*0.25)
    
    # Prepare the spot discount factors
    DFs = np.cumprod(FDFs)
    
    # and return the Value of a ZCB
    return DFs[-1]

def CC_Spot_and_Forward(FwdRates):    

    size = len(np.zeros(len(FwdRates)))
    
    # Prerare the forward discount factors    
    FDFs  = 1/(1+FwdRates*0.25)
    ccfwd = -np.log(FDFs)/0.25
    
    # Prepare the spot discount factors
    DFs = np.cumprod(FDFs)
    j   = 0.25
    ccspot = np.zeros(size)
    for i, val in enumerate(DFs): 
        ccspot[i] = -np.log(val)/j
        j +=0.25
        
    return ccspot, ccfwd 

def SwapValue(FwdRates, rate):
    
    # The swap rates are calculated assuming semi-annual payments
    Swap_CFs = np.zeros(len(FwdRates))
    size     = len(Swap_CFs)

    # Prerare the forward discount factors    
    FDFs = 1/(1+FwdRates*0.25)
    
    # Prepare the spot discount factors
    DFs  = np.cumprod(FDFs)
    
    # Calculate the swap value
    for x in range(2, size + 1, 2):
        Swap_CFs[x-1] = rate*0.5*DFs[x-1]     
    
    Total_CFs_PV = np.sum(Swap_CFs) +  DFs[-1] 
    # and return the value
    return (Total_CFs_PV - 1)

def f_cubic(x, x1, y1):
    ret = splrep(x1, y1)
    return splev(x, ret)