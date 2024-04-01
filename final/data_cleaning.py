## Changing file names to same format
import os
import pandas as pd
import shutil
import glob
from tqdm import tqdm_notebook, tqdm
import warnings
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')
# %config Completer.use_jedi=False

cleaned_data_dir = "./cleaned_data"
if not os.path.exists(cleaned_data_dir):
    os.mkdir(cleaned_data_dir)
    
for idxx,file in enumerate(glob.glob("./stations_data/*/*")):
#     print(file)
    state = file.split('/')[2]
    file_name = file.split('/')[-1]
    
    df = pd.read_csv(file)
    
    print(f"{idxx}. {state} :: {file_name} :: old_shpae :: {df.shape} :: new_shape :: ", end='')
    
    try:
        # Drop column TOT-RF (mm)
        df.drop(columns=['TOT-RF (mm)'],inplace=True)
    except:
        pass
    
    ### Remove duplicate rows
    df = df.drop_duplicates(subset=['From Date'], keep='first')

    # Remove empty columns
    # calculate percentage of NaN values in each column
    nan_pct = df.isna().sum() / df.shape[0]

    # set threshold for NaN values to remove
    threshold = 0.5

    # filter DataFrame to remove columns with NaN percentages above threshold
    df = df.loc[:, nan_pct <= threshold]
#     df.info()

    # Remove columns which have unique values count less than 10
    df = df.loc[:, df.nunique() > len(df) * 0.005]
#     df.info()

    ### Removing first rows which don't contain any values as station was not established at that point of time
    # find index of first non-NaN value in columns C through F
    index = df.iloc[:, 2:].notna().any(axis=1).idxmax()
    
    if index !=0:
        # drop rows above index
        df = df.dropna(subset=df.columns[2:index], how='all')

#     pbar = tqdm(total=100)
    ## filling missing values with rolling mean
    if len(df.columns) > 12:
        while df.isna().sum().sum() > 0:

            # define rolling window size
            window_size = 9  # 4 rows above and 4 rows below, plus the current row

            # calculate rolling mean
            rolling_mean = df.rolling(window_size, min_periods=1, center=True).mean()

            # fill missing values with rolling mean
            df = df.fillna(rolling_mean)
    #         pbar.update(1)

        # close progress bar
    #     pbar.close()

        # print original DataFrame and filled DataFrame
        # print("Original DataFrame:\n", df)
        # print("\nFilled DataFrame:\n", df.info())
        df.reset_index(drop=True, inplace=True)

        new_loc = os.path.join(cleaned_data_dir,state)
        if not os.path.exists(new_loc):
            os.makedirs(new_loc)

        df.to_csv(os.path.join(new_loc, file_name), header=True, index=False)
        print(df.shape)
    else:
        print("DISCARDED")
