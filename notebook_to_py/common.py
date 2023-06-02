from pathlib import Path
from datetime import datetime
from glob import glob

def save_csv(df, dir, name=''):
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    Path(dir).mkdir(parents=True, exist_ok=True)
    # print(f'{pth}{name}_{time}.csv')
    fullPath = f'{dir}{name}{time}.csv'
    df.to_csv(fullPath, index=False)
    print(f'SAVED CSV : {fullPath}')

def select_csv_path(dir):
    dirFiles = [Path(x).name for x in glob(f'{dir}*.csv')]
    dirFiles.sort(reverse=True)
    filePath = dir+dirFiles[0]
    print(f'CSV File : {filePath}')
    return Path(filePath)