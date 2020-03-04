Readme

Kato, S., Kaplan, H. S., Schrödel, T., Skora, S., Lindsay, T. H., Yemini, E., et al. (2015). Global Brain Dynamics Embed the Motor Command Sequence of Caenorhabditis elegans. Cell, 163(3), 656–669. http://doi.org/10.1016/j.cell.2015.09.034


traces_raw= neural activity traces uncorrected
traces = neural activity traces corrected for bleaching
tracesDif = derivative of traces
IDs = identified neuron IDs
timeVectorSeconds = time vector in seconds
fps = frames per second
dataset = name of dataset
stimulus
	-identity = what was changed e.g. O2 (oxygen)
	-type = stimulus type e.g. binary steps
	-switchtimes =  time in seconds when stimulus changed from initial state to the other state
	-initialstate = the state that the stimulus starts with, refers to "conc"
	-conc = the concentrations of the stimulus
	-concunits - units of the "conc"


States = vector of different state types (8 states for WT_NoStim, 4 states for WT_Stim and AVA_HisCl

8 states for WT_NoStim:
	‘FWD’ forward crawling 
	‘SLOW’ forward slowing
	‘DT’ dorsal post reversal turn
	‘VT’ ventral post reversal turn
	‘REV1’ reverse crawling
	‘REV2’ reverse crawling
	‘REVSUS’ sustained reverse crawling
	‘NOSTATE’ - ambiguous

4 states for WT_Stim and AVA_HisCl:
	‘FWD’ forward crawling 
	‘REV’ reverse crawling
	‘REVSUS’ sustained reverse crawling
	‘TURN’ post reversal turn
	
