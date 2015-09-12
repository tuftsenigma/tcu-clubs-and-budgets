
*1* data retrieval

    [TCU website]
			|
	 scrapeTCU() ---club-info-and-resources---> [DB] + [Facebook]
                                                  \________/
						                               |
						                           mineTCU() ---club-social-media-metrics---> [DB]

*2* data mining

	[DB]
	 |
    budget-download.py ---club-budget-xls---> [Local]
												 |
											budget-mine.py ---club-budget-metrics---> [DB]


*3* data summary

	[DB]
	 |
	stats.py ---mathematical-summary---> [Human Brain] ---vis-tools---> [Visualization]
												
							 

