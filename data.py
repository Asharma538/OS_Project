import pandas as pd
import numpy as np
import sys
import os
import re

# 1. Get all the details of the processes present in system at the moment to an excel file


# 1.1 To get the home directory in your lapy directory
s = '../'
files = os.listdir(s)
while ('home' not in files):
    # print(files)
    s+='../'
    files = os.listdir(s)
s += '/proc'
files = os.listdir(s)

# 1.2 Preparing the dataframe which will hold data

column_names = [
    'pid', 'comm', 'state', 'ppid', 'pgid', 'sid', 'tty_nr', 'tpgid',
    'flags', 'minflt', 'cminflt', 'majflt', 'cmajflt', 'utime', 'stime',
    'cutime', 'cstime', 'priority', 'nice', 'num_threads', 'itrealvalue',
    'starttime', 'vsize', 'rss', 'rsslim', 'startcode', 'endcode', 'startstack',
    'kstkesp', 'kstkeip', 'signal', 'blocked', 'sigignore', 'sigcatch', 'wchan',
    'nswap', 'cnswap', 'exit_signal', 'processor', 'rt_priority', 'policy',
    'delayacct_blkio_ticks', 'guest_time', 'cguest_time'
]


# pattern = r'(\(.*?\))'
pattern = r'\((.*?)\)'



dicty = {}
for i in column_names:
    dicty[i]=[]


for i in files:
    try:
        a = int(i)
        with open(s+'/'+i+'/stat') as process_file:
            # process_details = process_file.read().split()
            process_details = process_file.read()
            # Use re.split to split the string based on the regex pattern
            result = re.split(pattern, process_details)
            result[0] = result[0].strip()
            result_extra = result[2].strip().split()
            result.pop()
            result.extend(result_extra)
            print(result)
            itr = 0
            for i in dicty:
                dicty[i].append(result[itr])
                itr+=1
    except:
        continue

# print(df)
pd.DataFrame(dicty).to_excel('process_details.xlsx', index=False)