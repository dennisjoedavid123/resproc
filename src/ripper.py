import csv
import sys
import pandas as pd
import os
from icecream import ic
import time
import concurrent.futures
import json

# OUTPUT_PATH = '../output/output.csv'
CLEAR_RESPONSE = "Clicked on 'Clear Response' button."
csv_columns = ['EED', 'REGNO', 'CID', 'QSN', 'QA', 'AP']


def main():
    dir = os.listdir()
    try:
        process()
    except:
        ic(" Exception")


def process(INPUT_PATH, reg_no, eed, OUTPUT_PATH):
    input_data = open(INPUT_PATH, 'r')
    result = {}
    for line in input_data:
        columns = line.split('|')  # or w/e you're delimiter/separator is
        i = 0
        data = {}
        data['EED'] = eed
        data['REGNO'] = reg_no
        for c in columns:
            if(i == 2):
                data["CID"] = c
            elif(i == 3):
                data["QSN"] = c
            elif(i == 4):
                data["QA"] = c

            elif(i == 5):
                data["AP"] = c
            elif(i == 9):
                # ic(c.lower)
                if c == 'RS' or c == CLEAR_RESPONSE:
                    if(data["CID"] not in result.keys()):
                        if (data["QSN"] != ""):
                            result[data["CID"]] = data

                    else:
                        if (data["QSN"] != ""):
                            result[data["CID"]] = data
            i += 1

    # ic(result.keys())
    # df = pd.DataFrame(result).T
    # ic(OUTPUT_PATH)
    with open(OUTPUT_PATH, 'a') as csvfile:
        # Writes Header only once for the entire file.
        # df.to_csv(f, mode='a', header=f.tell() == 0, index=False)
        # df.to_csv(f, mode='a', header=None, index=False)
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)

        if csvfile.tell() == 0:
            writer.writeheader()

        for key in result.keys():
            # ic(data)
            writer.writerow(result[key])

    return 'Success'


# Using the special variable
# __name__
if __name__ == "__main__":

    INPUT_FOLDER = "/home/dennis/Downloads/SEQ_CHECK/DIAMOND/CRL/rack1/logs"
    fileCount = 0
    starttime = time.perf_counter()
    out_dir = ''
    OUTPUT_PATH = ''
    PROJ_NAME = 'DIA'
    prev_dir = ''

    for (root, dirs, files) in os.walk(INPUT_FOLDER, topdown=True):
        ic(fileCount)
        try:
            # ic(root)
            out_dir = root.split('/')[9]

            if prev_dir is None:
                prev_dir = out_dir

            if prev_dir != out_dir:
                # ic(out_dir)
                OUTPUT_PATH = '../output/diamond/rack1/output'
                OUTPUT_PATH = OUTPUT_PATH+'_'+PROJ_NAME + \
                    '_'+out_dir.split('_')[3]+'.csv'
                prev_dir = out_dir

            # ic(OUTPUT_PATH)
        except IndexError:
            # ic(root)
            ic('Do Nothing')

        # ic(OUTPUT_PATH)
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = [executor.submit(process, os.path.join(root, file),
                                       file.split('-')[0],
                                       file.split('-')[1],
                                       OUTPUT_PATH
                                       ) for file in files]

            for f in concurrent.futures.as_completed(results):
                try:
                    if (f.result() == "Success"):
                        fileCount = fileCount+1

                except Exception as exc:
                    ic(exc)

    finishtime = time.perf_counter() - starttime

    ic(str(round(finishtime, 2)) + 'seconds')
