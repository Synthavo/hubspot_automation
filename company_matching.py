

import pandas as pd
import os 
import time

INPUT_DIR = "input\company"
OUTPUT_DIR = "output\company"

COMPANY_LABEL = "Company name"

def split_str(string):
    string = string.split(" ")
    string = [h.split("-") for h in string]
    string = [item for sublist in string for item in sublist] # flatten list 
    return string

def list_to_display_String(ls):

    indexes = [x+1 for x in range(len(ls))]
    left = 3
    right = 3
    filler = " "

    upper = ""
    lower = ""

    for string, index in zip(ls, indexes): 
        upper += left * filler
        upper += string
        upper += right * filler 
        upper += "|"

        lower += left * filler
        
        if len(string) % 2 == 0: # if even
            inner_right = int(len(string) / 2)
            inner_left = inner_right -1 
        else: #if uneven
            inner_right = int(len(string) / 2)
            inner_left = inner_right
        lower += inner_left * filler
        lower += str(index)
        lower += inner_right * filler
        lower += right * filler
        lower += "|"
    return lower, upper

def get_company_string(string):
    splitted = split_str(string)
    lower, upper = list_to_display_String(splitted)
    return lower,upper, len(splitted)

def get_index_input(index_len, index):
    print(str(index + 1) + ": Enter indexes of string you want to save, delimitted by a space.'back' -> one back, 'finish' -> end.")
    inp = input().lower()
    
    if inp == "back" or inp == "finish":
        return inp

    numbers = inp.split(" ")
    

    for number in numbers:
        if not number.isdigit(): # if its not an int
            if number != "-":
                print("Please only provide an int number or a '-'.")
                
                return (get_index_input(index_len, index))
        elif int(number) < 1:
            print("Please only provide int numbers > 1")
            return (get_index_input(index_len, index))
     
    numbers = [int(x) if x != "-" else x for x in numbers ]
    for number in numbers:
        if number != "-":
            if number > index_len:
                print("Please provide only valid indexes")
                return (get_index_input(index_len, index))
    
    return numbers

def get_output(input_indexes, splitted):
    output = ""
    last_was_dash = False
    for count,index in enumerate(input_indexes):
        
        if index == "-":
            output += "-"
            last_was_dash = True
        else:
            if count != 0 :
                if last_was_dash:
                    last_was_dash = False
                else:
                    output += " "
            output += splitted[index -1]
    
    return output

def end_script(df: pd.DataFrame, index = None):
    df_filtered = df[df["company_short"] != ""] #only save ones that you changed.
    
    filename = str(time.time()) + ".csv"
    filename = os.path.join(OUTPUT_DIR, filename)

    df_filtered.to_csv(filename, index  = False)

    print(f"File saved to: {filename}")
    if index:
        print(f"When continuing, enter Line: {index+1}")
    exit()


def iteration(index, row,df, back = False):
    company_name = row[COMPANY_LABEL]

    splitted = split_str(company_name)
    if len(splitted) == 1:
        if back:
            return iteration(index -1, df.loc[index-1], df, back = True)
        df.loc[index, "company_short"] = splitted[0].upper()
        return
    lower, upper = list_to_display_String(splitted)

    print(upper)
    print(lower)

    input_indexes = get_index_input(len(splitted), index)
    if input_indexes == "back":
        iteration(index -1, df.loc[index-1], df, back = True)
        iteration(index, row, df)
    else:
        if input_indexes == "finish":
            end_script(df,index = index)
        
        output_string = get_output(input_indexes, splitted)
        output_string = output_string.upper()
        print(output_string)
        df.loc[index, "company_short"] = output_string






def get_start_line():
    inp = input("At which line do you want to start ? ")

    try:
        inp_int = int(inp)

        if inp_int == 0:
            print("Please provide an int number > 0.")
            return get_start_line()
        return inp_int
    except ValueError:
        print("Please only provide an int number.")
        return get_start_line()


if __name__ == "__main__":
    start_line = get_start_line()
    print("TYPE IN finish to end script")


    files = os.listdir(INPUT_DIR)
    csv_files = [x for x in files if x.endswith(".csv")]
    if len(csv_files) == 0:
        print("No CSV File in input folder. Please provide exactly one")
    elif len(csv_files) > 1:
        print("More than one CSV File in input folder. Please provide exactly one")
    else:
        csv_file = csv_files[0]
        df  = pd.read_csv(os.path.join(INPUT_DIR, csv_file),header=0)
        #insert empty row
        df["company_short"] = ""

        #remove empty rows
        df = df[~df[COMPANY_LABEL].isnull()]
        df = df.reset_index()
        
        #filter out startline
        df = df.drop(index= df.index[:start_line-1])

        for index, row in df.iterrows():
            iteration(index, row, df)

        print("All lines in file Done.")
        end_script(df)

    stringy_list = split_str(stringy)
    lower,upper = list_to_display_String(stringy_list)
    print(upper)
    print(lower)


