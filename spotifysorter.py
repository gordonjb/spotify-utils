import pandas
import re
import progressbar
from tqdm import tqdm
import numpy as np
import csv

def prompt_selection(results):
    global ordered
    global skipped
    global exported
    global dupes
    print("More than one match. Type the number of the correct result, 's' to enter a Spotify ID manually, 'd' for a duplicate, or 'x' to skip.")
    print("Control row was:")
    print(ctrl_row)
    print("Search results were:")
    print(results)
    response = input("Selection: ")
    if response == 's':
        sid = input("Enter the Spotify ID (must be in the exported list still): ")
        prompt_selection(exported[exported['spotid'].str.strip().str.match(sid, na=False)])
        # Append new record
    elif response == 'x':
        print("Skipped")
        skipped.append(ctrl_row)
    elif response == 'd':
        print("Dupe")
        dupes.append(ctrl_row)
    else:
        ordered = ordered.append(results.loc[int(response)], ignore_index = True)
        exported.loc[results.loc[int(response)].name, :] = np.nan


def clean_up(input):
    s1 = str(input).lower().replace('remastered', '').replace('remaster', '').replace('album version explicit', '').replace('radio edit', '').replace(' ', '')
    return re.sub('\W+','', s1)


def clean_up_df(input):
    return input.str.lower().str.replace('remastered', '').str.replace('remaster', '').str.replace('album version explicit', '').str.replace('radio edit', '').str.replace(' ', '').str.replace('[^\w]','')

control = pandas.read_csv('/mnt/c/Users/Gordon/Desktop/gpm/fullthumbs.csv')
exported = pandas.read_csv('/mnt/c/Users/Gordon/Desktop/gpm/movedexport.csv', sep="|")

ordered = pandas.DataFrame(columns=['artist', 'title', 'spotid'])
skipped = []

for ctrl_row in tqdm(control.itertuples()):

     # access data using column names
    ctrl_artist = clean_up(ctrl_row.artist)
    ctrl_title = clean_up(ctrl_row.title)
    print(exported)
    result = exported[clean_up_df(exported['title']).str.contains(ctrl_title, regex = False, na=False)]
    count = result.title.count()
    #print(count)
    if count == 1:
        ordered = ordered.append(result, ignore_index = True)
        exported.loc[result.iloc[0].name, :] = np.nan
    elif count > 1:
        result2 = result[clean_up_df(result['artist']).str.contains(ctrl_artist, regex = False, na=False)]
        count2 = result2.title.count()
        if count2 == 1:
            ordered = ordered.append(result2, ignore_index = True)
            exported.loc[result.iloc[0].name, :] = np.nan
        elif count2 > 1:
            prompt_selection(result2)
        elif count2 == 0:
                prompt_selection(result)
    elif count == 0:
        result3 = exported[clean_up_df(exported['artist']).str.contains(ctrl_artist, regex = False, na=False)]
        prompt_selection(result3)

ordered.to_csv('/mnt/c/Users/Gordon/Desktop/gpm/sorted.csv', sep="|", index=False)
pandas.DataFrame(skipped).to_csv('/mnt/c/Users/Gordon/Desktop/gpm/skipped.csv', index=False, quoting=csv.QUOTE_ALL)
pandas.DataFrame(dupes).to_csv('/mnt/c/Users/Gordon/Desktop/gpm/dupes.csv', index=False, quoting=csv.QUOTE_ALL)
#load control file (original csv) into array (of objects?)

#load exported csv into array (of objects?)

#foreach line in control file
#    search exported csv for a match
#    when we find one, remove from exported array, and add to a new array of objects (i.e. the new order), this could just be spotify ids
#    if we don't find one, prompt to check the exported csv file and ask the user to enter the ID, can then be removed

#we should then have a list of spotify ids that we can make a call to the api to ❤
