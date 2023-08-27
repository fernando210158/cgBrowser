import pandas as pd
from audioMos import audioMosCal

pathRep = 'C:/Users/Utente/Documents/Catture/RES'
trcBlob = 'blobTrcE2E.csv'

# Retreive audio records
e2eBlobTrc = pd.read_csv(f'{pathRep}/{trcBlob}', sep=',', delimiter=None, na_values=[''])
audioE2ETrc = e2eBlobTrc[e2eBlobTrc['mediaType'] == 'Audio']

A_LFLpP = 20  # Value is in ms
A_NPpTS = 1

audioE2ETrc['mos'] = audioE2ETrc.apply(lambda x: audioMosCal(
        x['codec'],
        x['redCodec'],
        A_LFLpP,
        A_NPpTS,
        x['RTPAvgBr'] + x['RTPSdvBr'],
        x['pWDuration'],
        x['RTPMissedPack'],
        x['burstPackMissed'],
        x['burstFreq']), axis=1)

audioE2ETrc['e2eMos'] = audioE2ETrc.apply(lambda x: audioMosCal(
        x['codec'],
        x['redCodec'],
        A_LFLpP,
        A_NPpTS,
        x['RTPAvgBr'] + x['RTPSdvBr'],
        x['pWDuration'],
        x['e2eRTPMissedPack'],
        x['e2eBurstPackMissed'],
        x['e2eBurstFreq']), axis=1)

audioE2ETrc.to_csv(f'{pathRep}/AudioBlobE2E.csv')

