import pandas
import re


def prompt_selection(results, ):
    print("More than one match. Type the number of the correct result, 's' to enter a Spotify ID manually, or 'x' to skip.")
    print("Control row was:")
    print(ctrl_row)
    print("Search results were:")
    print(results)
    response = input("Selection: ")
    if response == 's':
        sid = input("Enter the Spotify ID: ")
        # Append new record
    elif response == 'x':
        print("Skipped")
    else:
        ordered = ordered.append(result.loc[response], ignore_index = True)


control = pandas.read_csv('/mnt/c/Users/Gordon/Desktop/gpm/fullthumbs.csv')
exported = pandas.read_csv('/mnt/c/Users/Gordon/Desktop/gpm/movedexport.csv', sep="|")

ordered = pandas.DataFrame(columns=['artist', 'title', 'spotid'])
skipped = []
#print(control.head)
#print(exported.head)

for ctrl_row in control.itertuples():
     # access data using column names
    ctrl_artist = ctrl_row.artist
    ctrl_title = ctrl_row.title

    #exp_row = exported[ctrl_row.Index]
    #result = exported.loc[(exported['artist'] == ctrl_artist) & (exported['title'] == ctrl_title)]
    result = exported[exported['title'].str.contains(ctrl_title, flags=re.IGNORECASE, regex = False)]
    count = result.title.count()
    #print(count)
    if count == 1:
        ordered = ordered.append(result, ignore_index = True)
        #print(result.iloc[0])
        exported.drop(result.iloc[0].name)
    elif count > 1:
        result2 = result[result['artist'].str.contains(ctrl_artist, flags=re.IGNORECASE, regex = False)]
        count2 = result2.title.count()
        if count2 == 1:
            ordered = ordered.append(result2, ignore_index = True)
            exported.drop(result2.iloc[0].name)
        elif count2 > 1:
            #user entry
            print("More than one match. Type the number of the correct result, 's' to enter a Spotify ID manually, or 'x' to skip.")
            print("Control row was:")
            print(ctrl_row)
            print("Search results were:")
            print(result2)
            response = input("Selection: ")
        elif count2 == 0:
                #user entry
                prompt_selection(results, ctrl_row, ordered, exported)
    elif count == 0:
        print("No match. Type the number of the correct result, 's' to enter a Spotify ID manually, or 'x' to skip.")
        print("Control row was:")
        print(ctrl_row)
        response = input("Selection: ")
        if response == 's':
            sid = input("Enter the Spotify ID: ")
        elif response == 'x':
            print("Skipped")
        else:

print(ordered)
#load control file (original csv) into array (of objects?)

#load exported csv into array (of objects?)

#foreach line in control file
#    search exported csv for a match
#    when we find one, remove from exported array, and add to a new array of objects (i.e. the new order), this could just be spotify ids
#    if we don't find one, prompt to check the exported csv file and ask the user to enter the ID, can then be removed

#we should then have a list of spotify ids that we can make a call to the api to ❤
