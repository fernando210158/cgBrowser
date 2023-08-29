import glob
import pandas as pd


def combine_dat_files(pathIn, pathOut, type):
    """
    Combines all .dat files in the specified folder into a single Pandas DataFrame.

    Args:
        pathIn (str): The path to the folder containing the .{type} files.
        pathOut (str): The path to the folder containing the .{type} aggregated file.
        type (str): The file extension of the files.

    Returns:
        Pandas DataFrame: A DataFrame containing the data from all of the .dat files in the specified folder.
    """

    # Create a new empty DataFrame
    blob = pd.DataFrame()

    # Get a list of all the .dat files in the folder
    allFiles = glob.glob(f'{pathIn}/*.{type}')

    # If there are no files, return the empty DataFrame
    if len(allFiles) == 0:
        return blob

    # Iterate over the files and read them into Pandas DataFrames
    for fName in allFiles:
        with pd.option_context('mode.chained_assignment', None):
            df = pd.read_csv(fName, sep='|', delimiter=None, na_values=[''], dtype=str, skiprows=1)
            blob = pd.concat((blob, df), axis=0)

    prot = {'0': 'N/A', '1': 'ssl/tcp', '2': 'http', '3': 'quic', '4': 'ssl+', '5': 'quic+', '6': 'http+',
            '101': 'udp', '102': 'tcp', '103': 'dtls'}
    provider = {'1001': 'Blacknut', '1002': 'Stadia', '1003': 'GeForceNow', '2001': 'Teams'}
    mType = {'1': 'Audio', '2': 'Video', '3': 'Sharing', '4': 'Data'}

    # Translate fields in human readable format
    protField = ['ctrlProtocol', 'transportMediaProtocol', 'eventProt']
    for field in protField:
        try:
            blob[field] = blob[field].map(prot)
        except:
            pass

    try:
        blob['serviceProvider'] = blob['serviceProvider'].map(provider)
    except:
        pass

    try:
        blob['mediaType'] = blob['mediaType'].map(mType)
    except:
        pass

    timeField = ['startTime', 'endTime', 'gameStartTime', 'streamingStartTime', 'streamingEndTime',
                 'sessionStartTime', 'sessionEndTime']
    for field in timeField:
        try:
            blob[field] = pd.to_datetime(blob[field], unit='ms')
        except:
            pass

    blob.to_csv(f'{pathOut}/blob{type}.csv')

    return blob
