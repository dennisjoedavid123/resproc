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
csv_columns = ['EED', 'REGNO', 'CID', 'QSN', 'QA',
               'NQA_CQ', 'NQA_AS', 'NQA_NXT', 'AP', 'TS']
e_csv_columns = ['EED', 'REGNO', 'CID', 'QSN',
                 'QA', 'NQA_CQ', 'NQA_AS', 'NQA_NXT', 'AP', 'TS']


def main():
    dir = os.listdir()
    try:
        process()
    except:
        ic(" Exception")


# def ff_process(INPUT_PATH, reg_no, eed, OUTPUT_PATH):
#     result = {}
#     cs_result = {}
#     # ic("hasdfasdfasdfasdfads")

#     for line in input_data:
#         columns = line.split('|')
#         i = 0
#         data = {}
#         data['EED'] = eed
#         data['REGNO'] = reg_no
#         for c in columns:
#             if(i == 2):
#                 data["CID"] = c
#             elif(i == 3):
#                 data["QSN"] = c
#             elif(i == 4):
#                 data["QA"] = c

#             elif(i == 5):
#                 data["AP"] = c

#             elif(i == 9):
#                 ic("inside")
#                 if c == 'RS' or c == CLEAR_RESPONSE:
#                     if(data["CID"] not in result.keys()):
#                         if (data["QSN"] != ""):
#                             result[data["CID"]] = data

#                     else:
#                         if (data["QSN"] != ""):
#                             result[data["CID"]] = data
#                 # ic(c)
#                 # if 'C.Q.' in c:
#                 # ic(c)

#             elif(i == 12):
#                 # ic(c)
#                 if(data["CID"] in result.keys()):
#                     data = result[data["CID"]]
#                     data.update({"TS": c})
#                     # ic(data)
#                     result[data["CID"]] = data
#             i += 1

#     return "Success"


def process(INPUT_PATH, reg_no, eed, OUTPUT_PATH, CS_OUTPUT_PATH):
    input_data = open(INPUT_PATH, 'r')
    result = {}
    cs_result = {}
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

                if 'C.Q.No' in c:
                    if(data["CID"] in result.keys()):
                        if(data["QSN"] == result[data["CID"]]["QSN"]):
                            if(data["QA"] != result[data["CID"]]["QA"]):
                                n_data = result[data["CID"]]
                                n_data.update({'NQA_CQ': data["QA"]})
                                if cs_result:
                                    ic("C Q Issue")
                                    if (data["CID"] in cs_result.keys()):
                                        cs_result[data["CID"]].update(n_data)
                                    else:
                                        cs_result[data["CID"]] = n_data
                                else:
                                    cs_result[data["CID"]] = n_data

                                # ic(cs_result)
                if 'Auto Submitted' in c:
                    if(data["CID"] in result.keys()):
                        if(data["QSN"] == result[data["CID"]]["QSN"]):
                            if(data["QA"] != result[data["CID"]]["QA"]):
                                ic("Auto Submitted Issue")
                                n_data = result[data["CID"]]
                                n_data.update({'NQA_AS': data["QA"]})
                                if cs_result:
                                    if (data["CID"] in cs_result.keys()):
                                        cs_result[data["CID"]].update(
                                            n_data)
                                    else:
                                        cs_result[data["CID"]] = n_data
                                else:
                                    cs_result[data["CID"]] = n_data

                if 'Next' in c:
                    if(data["CID"] in result.keys()):
                        if(data["QSN"] == result[data["CID"]]["QSN"]):
                            if(data["QA"] != result[data["CID"]]["QA"]):
                                ic("Next Issue")
                                n_data = result[data["CID"]]
                                n_data.update({'NQA_NXT': data["QA"]})
                                if cs_result:
                                    if (data["CID"] in cs_result.keys()):
                                        cs_result[data["CID"]].update(
                                            n_data)
                                    else:
                                        cs_result[data["CID"]] = n_data
                                else:
                                    cs_result[data["CID"]] = n_data

            elif(i == 12):
                # ic(c)
                if(data["CID"] in result.keys()):
                    data = result[data["CID"]]
                    data.update({"TS": c})
                    # ic(data)
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

    with open(CS_OUTPUT_PATH, 'a') as e_csvfile:
        # Writes Header only once for the entire file.
        # df.to_csv(f, mode='a', header=f.tell() == 0, index=False)
        # df.to_csv(f, mode='a', header=None, index=False)
        e_writer = csv.DictWriter(e_csvfile, fieldnames=e_csv_columns)

        if e_csvfile.tell() == 0:
            e_writer.writeheader()
        for cs_key in cs_result.keys():
            # ic(cs_key)
            e_writer.writerow(cs_result[cs_key])

    return 'Success'


# Using the special variable
# __name__
if __name__ == "__main__":

    INPUT_FOLDER = "/home/dennis/Downloads/SEQ_CHECK/DIAMOND/CRL/rack1/logs"
    # INPUT_FOLDER = "/home/dennis/work/dev/OES/projects/ripper/code/input/Rack1_Candidate_Logs_26MAR2021"
    # INPUT_FOLDER = "/home/dennis/work/dev/OES/projects/ripper/code/input/allnew/old"

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
            ic(out_dir)

            if prev_dir is None:
                prev_dir = out_dir

            if prev_dir != out_dir:

                OUTPUT_PATH = '../output/diamond/rack1/output'
                CS_OUTPUT_PATH = '../output/diamond/rack1/cs_output'

                # OUTPUT_PATH = '../output/mahadev/output'
                # CS_OUTPUT_PATH = '../output/mahadev/cs_output'

                ic(out_dir.split('_'))

                file_name_fix = "EMPTY" if out_dir.split(
                    '_')[0] == 'input' else out_dir.split('_')[3]

                ic(file_name_fix)

                OUTPUT_PATH = OUTPUT_PATH+'_'+PROJ_NAME + \
                    '_'+file_name_fix+'.csv'

                CS_OUTPUT_PATH = CS_OUTPUT_PATH+'_'+PROJ_NAME + \
                    '_'+file_name_fix+'.csv'

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
                                       OUTPUT_PATH, CS_OUTPUT_PATH
                                       ) for file in files]

            for f in concurrent.futures.as_completed(results):
                try:
                    if (f.result() == "Success"):
                        fileCount = fileCount+1

                except Exception as exc:
                    ic(exc)

    finishtime = time.perf_counter() - starttime

    ic(str(round(finishtime, 2)) + 'seconds')
