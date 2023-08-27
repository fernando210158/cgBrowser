from mergeFilesP import recordBlob

# pathTrc = 'C:/Users/fernando/Documents/NTH/Products/CollaborationTools/Teams/HS4CT/Teams-2022-02-03-PTP-FernAV-PierA-Impairments/trc'
# pathDat = 'C:/Users/fernando/Documents/NTH/Products/CollaborationTools/Teams/HS4CT/Teams-2022-02-03-PTP-FernAV-PierA-Impairments'
# pathRep = 'C:/Users/fernando/Documents/NTH/Products/CollaborationTools/Teams/HS4CT/Teams-2022-02-03-PTP-FernAV-PierA-Impairments'

def aggreg(pathDat, pathTrc, pathRes):

    # Session Aggregation
    blobDat = recordBlob(pathDat, pathRes, 'dat')
    if blobDat == False:
        return False
    if pathTrc == False:
        return
    else:
        blobTrc = recordBlob(pathTrc, pathRes, 'trc')
        if blobTrc == False:
            return False

    return len(blobDat["sessionId"].unique()), len(blobTrc["sessionId"].unique())

# aggreg(pathDat, pathTrc, pathRep)