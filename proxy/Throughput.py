#!/usr/bin/python3.10
#jak2302


import sys
import time



def throughput_calc(beta, ftime, stime):
    """
    This function calculates the throughput of a single chunk
    Inputs:
        beta  : size of chunk (bits)
        ftime : time when full chunk has been recieved 
        stime : time of chunk request 
    Outputs:
        throughput : how much data is processed in a given time window
    """
    throughput = beta/(ftime - stime)
    return throughput



def ewma_calc(T_curr, alpha, T_new):
    """
    This functions calcualtes the exponentially-weighted moving average (EWMA)
    Inputs:
        T_curr : current EWMA Threshold
        alpha  : constant 0 ≤ α ≤ 1 controls the tradeoff between a smooth throughput estimate (α closer to 0) and one that reacts quickly to changes (α closer to 1)
        T_new  : latest threshold calculation

    Output :
        newT_curr : new current EWMA Threshold
    """

    newT_curr = alpha*T_new + (1-alpha)*Tcurr

    return newT_curr
