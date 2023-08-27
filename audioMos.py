import math


tableB1M1071 = {'AMR_NB': [1.33483, 6.42499, 3.49066, 0, 723.3661, 1],
          'AMR_WB': [3.19158, 5.7193, 1.63208, 0, 826.7936, 1]}

def audioMosCal(aCod, aRedCod, A_LFLpP, A_NPpTS, aBr, A_MT, aPackLoss, aPackBurst, aBurstFreq):
    # A_LFpP is the audio frame length for audio packet, see 6.11 of P1201.1
    # A_NPpTS Number of RTP packets per 1 audio frame, see 6.121 of P1201.1

    if aCod == 'Satin' and aRedCod != '':
        aCodec = 'AMR_WB'
        aSamp = 48000
    elif aCod == '' and aRedCod == 'Redundancy':
        aCodec = 'AMR_NB'
        aSamp = 48000
    else:
        aCodec = 'AMR_NB'
        aSamp = 48000

    # Formula 6.1 P1201.1
    audioFrameLength = 1024000 / aSamp

    # Number of packet loss event per A_MT (a single packet loss or a burst loss is one event)
    A_PLEF = aPackLoss - aPackBurst + aBurstFreq

    if A_PLEF == 0:
        A_ABPLL = 0
    else:
        A_ABPLL = aPackLoss / A_PLEF

    # Formula 4.4 of M1071
    A_LFL = A_PLEF * max(audioFrameLength, A_LFLpP * (A_ABPLL + A_NPpTS - 1) / A_NPpTS)

    # Formula 4.3 of M1071
    if A_MT != 0:
        MA = (1 - tableB1M1071[aCodec][3]) * math.exp(-(10 * A_LFL) / (tableB1M1071[aCodec][4] * A_MT)) + \
             tableB1M1071[aCodec][3] * math.exp(- (10 * A_LFL) / (tableB1M1071[aCodec][5] * A_MT))
    else:
        MA = 0

    # Formula 4.2 of M1071
    A_MOSC = 1 + (tableB1M1071[aCodec][0] - tableB1M1071[aCodec][0] /
                 (1 + math.pow((aBr / tableB1M1071[aCodec][1]), tableB1M1071[aCodec][2])))

    # Formula 4.1 of M1071
    A_MOS = 1 + (A_MOSC -1) * MA

    return A_MOS

# aCodec = 'AMR_WB'
# aSamp = 48000
# A_LFLpP = 20 # Value is in ms
# A_NPpTS = 1
# aBr = 42 # Value is in Kbps
# A_MT = 10 # Value is in seconds
# aPackLoss = 0
# aPackBurst = 0
# aBurstFreq = 0

# print(round(audioMosCal(aCodec, aSamp, A_LFLpP, A_NPpTS, aBr, A_MT, aPackLoss, aPackBurst, aBurstFreq), 2))