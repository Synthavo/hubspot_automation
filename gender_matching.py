import pandas as pd
import os 
import time

INPUT_DIR = "input"
OUTPUT_DIR = "output"

FIRST_NAME_LABEL = "First Name"
LAST_NAME_LABEL = "Last Name"

def get_start_line():
    inp = input("At which line do you want to start ? ")

    try:
        inp_int = int(inp)
        return inp_int
    except ValueError:
        print("Please only provide an int number.")
        return get_start_line()
    
def get_gender_input(f_name, l_name):
    print("Enter -> Male, Space + Enter -> Female, 'back' -> one back, 'finish' -> end")
    inp = input(f_name + " " + l_name)
    if inp == " ":
        return "f"
    elif inp == "":
        return "m"
    elif inp.lower() == "finish" or inp.lower() == "back":
        return inp
    else:
        print("You did enter something else than exepcted.")
        return get_gender_input(f_name,l_name)
    
def iteration(index, row,df):
    if not(row.isnull()[FIRST_NAME_LABEL] and row.isnull()[LAST_NAME_LABEL]): #skip if both are empty
        if row.isnull()[FIRST_NAME_LABEL]:
            f_name = ""
            l_name = row[LAST_NAME_LABEL]
        elif row.isnull()[LAST_NAME_LABEL]:
            l_name = ""
            f_name = row[FIRST_NAME_LABEL]
        else:
            f_name = row[FIRST_NAME_LABEL]
            l_name = row[LAST_NAME_LABEL]

        gender = get_gender_input(f_name, l_name)
        
        if gender == "back":
            iteration(index -1, df.iloc[index-1], df)
            iteration(index, row, df)
        else:
            if gender== "finish":
                end_script(df)
            #insert gender
            df.loc[index,"gender"] = gender
            

def end_script(df: pd.DataFrame):
    df_filtered = df[df["gender"] != ""] #only save ones that you changed.
    
    filename = str(time.time()) + ".csv"
    filename = os.path.join(OUTPUT_DIR, filename)

    df_filtered.to_csv(filename, index  = False)
    exit()


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
        df  = pd.read_csv(os.path.join(INPUT_DIR, csv_file)) #TODO load from specific line

        #insert empty row
        df["gender"] = ""

        for file_index, index, row in enumerate(df.iterrows()):
            iteration(index, row, df)
            #HIER WEITER, mach das geprintet wird welche line man weiter machen muss next time

            
        print("All lines in file Done.")
        end_script(df)
        


    







            





    



