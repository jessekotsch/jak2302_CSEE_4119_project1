#!/usr/bin/python3.10
#jak2302


import sys
import time




def bitrate_select(Tcurr, availible_bitrates):
    """
    This function calculates the throughput of a single chunk
    Inputs:
        T_curr (int)               : current EWMA Threshold
        availible_bitrates [list]  : availible bitrates found from parsing minifest file
    Outputs:
        bitrate (str)  : chosen bitrate (A connections can support a bitrate if the average throughput is at least 1.5x the bitrate)
        
    """
    
    return bitrate


def bitrate_search(manifest):
    """
    This function parses the manifest (mpd) file requested at the beginning of the stream for available bitrates
    (noted as bandwidths in the file"
    Inputs:
        manifest (str) : .mdp file requested at the beginning of the stream (encoded in XML). Used to extract possible bitrates. 
    Outputs:
        availible_bitrates [list]  : availible bitrates found from parsing minifest file

    """

    availible_bitrates = []

    print("Found!")
	root = ET.fromstring(str(manifest.decode()))
	#for child in root: 
	    #print(child.tag, child.attrib)

    
    return availible_bitrates



