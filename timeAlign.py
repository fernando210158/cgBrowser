import pandas as pd
import numpy as np

pathRep = 'C:/Users/Utente/Documents/Catture/RES'
trcBlob = 'blob-trc.csv'

blobTrc = pd.read_csv(f'{pathRep}/{trcBlob}', sep=',', delimiter=None, na_values=[''])

# Get unique sessionId values
uniqueSess = blobTrc['sessionId'].unique()
print(uniqueSess)

blobTrcE2e = pd.DataFrame()
for sessItem in uniqueSess:

    # Extract all flows of a sessionId
    trc = blobTrc[blobTrc['sessionId'] == sessItem]

    # Get unique IP src and dst addresses from used by the flows
    uniqueIp1 = trc['ip1Loc'].unique()
    uniqueIp2 = trc['ip2Loc'].unique()

    # Extract unique list of addresses and calculate IP couples that will be set in the ouList list
    listNum = np.union1d(uniqueIp1, uniqueIp2)
    outList = []
    for i in range(len(listNum)):
            item = listNum[i]
            inList = listNum[i + 1:]
            for j in inList:
                outList.append((item, j))

    # Sum counters of each ip-couple of both directions (IP1-IP2 and IP2-IP1) for each Partial Window
    # For each Partial Window and each direction there will be the total packets and losses occurred in both directions
    # Assumption: they will represent the E2E estimation of packet loss if the channel was symmetrical
    #
    # [IP1] ->>>>>x>>>x>>>>-> [MonPoint] (no visibility) [IP2]
    # [IP1] (no visibility)   [MonPoint] <-xxx<<<xx<<<- [IP2]
    #
    # Result (symmetrical channel)
    # [IP1] ->>>>>x>>>x>>>>-> [Mon Point] <-xxx<<<xx<<<- [IP2]
    #
    # x represents packet loss, whereas > or < represent received packets
    for item in outList:
        flow = trc[((trc['ip1Loc'] == item[0]) & (trc['ip2Loc'] == item[1])) |
                   ((trc['ip2Loc'] == item[0]) & (trc['ip1Loc'] == item[1]))]
        aggregation_counters = {'RTPSeenPack': 'sum', 'RTPMissedPack': 'sum', 'burstPackMissed': 'first',
                                'burstFreq': 'sum', 'packReorder': 'sum'}
        aggFlow = flow.groupby(flow['pWStartTime']).aggregate(aggregation_counters)
        mapNames = {'RTPSeenPack': 'e2eRTPSeenPack', 'RTPMissedPack': 'e2eRTPMissedPack',
                    'burstPackMissed': 'e2eBurstPackMissed', 'burstFreq': 'e2eBurstFreq',
                    'packReorder': 'e2ePackReorder'}
        aggFlow.rename(columns=mapNames, inplace=True)

        # Merge of new calculated columns with the original flow columns
        flowResult = pd.merge(flow, aggFlow, on='pWStartTime', how='outer')

        # Add each E2E flow (flowResult) to build the E2E TRC blob
        blobTrcE2e = pd.concat([blobTrcE2e, flowResult], ignore_index=True, sort=False)

blobTrcE2e.to_csv(f'{pathRep}/blobTrcE2E.csv')

