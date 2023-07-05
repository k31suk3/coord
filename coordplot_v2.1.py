
import sys
import csv
import simplekml
import pandas as pd
import json
import os
import color_select
import time
import datetime 
import shutil


today = datetime.date.today().strftime('%Y%m%d')
path_configjson = "./configfile/config.json"
save_dir = "./outputs/" + today + "/"


#check_configfile
if os.path.exists(path_configjson) == False:
    print("'config.json' not found! <./configfile> to store 'config.json'")
    time.sleep(5)
    print("Canceled.")
    time.sleep(3)
    exit()


with open(path_configjson) as f:
    jf = json.load(f) 


flight_time = jf["alias"][0]["flight_time"]
#init_coord_col_from_config.json
latitude = jf["alias"][0]["latitude"]
longitude = jf["alias"][0]["longitude"]
altitude = jf["alias"][0]["altitude"]

#init_columns_list
columns_list = list(jf["alias"][0].items())

#init_visualization_methods_list
visualization_methods_list =["gradation","range","close"]

#init_columns_ind_list
columns_ind_list = []
for i, _ in enumerate(columns_list):
    columns_ind_list.append(str(i))
columns_ind_list.append("-c")    

#init_range_list
range_list = jf["ranges"]

#check_arg
try:
    source_file = None
    source_file = sys.argv[1]
except IndexError:
    source_file = input("Enter the source file as a string(Ex. test.csv)\n")
#check_source_fmt
while os.path.exists(source_file) == False or source_file[-4:] != ".csv":
    if os.path.exists(source_file) == False:
        print("\nIncorrect file name! Please enter the correct file name again.")
        source_file = input("Enter the source file as a string(Ex. test.csv)\n")
    elif source_file[-4:] != ".csv":
        print("\nNot a CSV file! The file must be in CSV format.")
        source_file = input("Enter the source file as a string(Ex. test.csv)\n")
#check_source_coord_col
coord_col = [latitude, longitude, altitude]
df = pd.read_csv(source_file) 
flg_coord_col = ""
time.sleep(1)
print("Checking columns for coordinates.....")
time.sleep(2)
for i in coord_col:
    if i not in df.columns:
        print(i, "...NG")
        flg_coord_col = False
        time.sleep(2)
    elif i in df.columns:
        print(i, "..OK")
        time.sleep(2)        
if flg_coord_col == False:
    print("\nColumns Value Error! The above column specified in config.json does not seem to exist.\
        \nCheck config.json and specify the correct columns.")
    time.sleep(15) 
    print("Canceled.")
    time.sleep(3)
    exit()

for i in range(100):
    #select_target_column
    print("\nPlease select the columns you wish to visualize from the following\
        \nTo specify column names directly, use Enter '-c'.")
    print("--------------------------------------")
    for index,item in enumerate(columns_list):
        print(index,item)
    print("--------------------------------------")
    target_column = ""
    value = ""
    while value not in columns_ind_list:
        value = input()
        if value in columns_ind_list:
            if value != "-c":
                
                while target_column not in df.columns:
                    value_int = int(value)
                    target_column = columns_list[value_int][1]
                    print("\nSpecified column: ", target_column)
                    time.sleep(1)
                    print("Checking specified column exists in the source file....")
                    time.sleep(2)
                    if target_column in df.columns:
                        print("OK\n")
                    elif target_column not in df.columns:
                        print("NG\n")
                        print("The specified column does not seem to exist in the source file.\
                            \nCheck the source file or 'config.json' and try again.")
                        time.sleep(15) 
                        print("Canceled.")
                        time.sleep(3)
                        exit()
            else:
                while target_column not in df.columns:
                    target_column = input("\nEnter the Arbitrary column name as a string(Ex. client_id)\n")
                    print("\nSpecified column: ", target_column)
                    time.sleep(1)
                    print("Checking specified column exists in the source file....")
                    time.sleep(2)
                    if target_column in df.columns:
                        print("OK\n")                
                    elif target_column not in df.columns:
                        print("NG\n")
                        print("The column name entered does not exist. Please enter the column name again.")
                        continue
        else:
            print("\nIncorrect input!! Please try again.")


    #init_sourcefile_check_NaN
    wow_replacement = ""
    print("Checking for the specified column do not contain missing values.....")
    time.sleep(2)
    missing_values = df[target_column].isnull().sum()
    if  missing_values > 0:
        while wow_replacement not in ["y", "n", "yes", "no"]:
            wow_replacement = input("\n" + str( missing_values) + " Missing values detected!　Fill in missing values with the immediately preceding value?[y/n]\
                \n*If more than 4 missing values are in a row, the fourth and subsequent ones are not adapted.\n")
            if wow_replacement ==  "y" or wow_replacement ==  "yes":
                df[target_column].fillna(method='ffill', limit=3, inplace=True)
                print("Filled")
            elif wow_replacement ==  "n" or wow_replacement ==  "no":
                pass
            else:
                print("\nIncorrect input !!\n")
                continue  
    else:
        print("No missing values were detected.")

    #select_visualization_methods
    print("\nSet the color of the data for easy visualization of its distribution and variability. Please choose how you would like to visualization_methods.")
    print("--------------------------------------")
    for index,item in enumerate(visualization_methods_list):
        print(index,item)
    print("--------------------------------------")
    string = ""
    while string not in ["0", "1", "range", "gradation"]:
        string = input()
        if string=="2" or string=="close":
            print("Canceled.")
            time.sleep(3)
            exit()
        elif string=="0" or string=="gradation":
            set_method = "gradation"
        elif string=="1" or string=="range":
            set_method = "range"
        else:
            print("Incorrect input !! Please enter the correct value again.")
            continue      

    #visualization_gradation
    if set_method == "gradation":
        df_target_column = df[target_column]
        class_list = df_target_column[~df_target_column.duplicated()]
        if len(class_list) > 1275:#check under 1275
            print(class_list)
            print("The range of representable colors has been exceeded.")
            print("Canceled.")
            time.sleep(5)
            exit()
        #sort
        data_list = ["ascending","descending","pass","close"]   
        print("\nSorts the data to be displayed. Select ascending or descending order.")
        print("Please select the following data")
        print("--------------------------------------")
        for index,item in enumerate(data_list):
            print(index,item)
        print("--------------------------------------")
        string = ""
        while string not in ["0", "1", "2", "ascending", "descending", "pass"]:
            string = input()
            if string=="3" or string=="close":
                print("Canceled.")
                time.sleep(3)
                exit()
            elif string=="0" or string=="ascending":
                sorted_class_list = class_list.sort_values(ascending=True)
            elif string=="1" or string=="descending":
                sorted_class_list = class_list.sort_values(ascending=False)
            elif string=="2" or string=="pass":
                sorted_class_list = class_list
            else:
                print("Incorrect input !! Please enter the correct value again.")
                continue 
        color_list = color_select.gradation(len(class_list))
        kml = simplekml.Kml()
        class_json = {}
        for ind, item in enumerate(sorted_class_list):
            class_json[item]={
            "multi_point":kml.newmultigeometry(name=item),
            "color":simplekml.Color.hex(color_list[ind])
            }    
        for _, row in df.iterrows():
            point = None
            clm = row[target_column]
            if clm == None:
                pass
            else:
                point = class_json[clm]["multi_point"].newpoint()
                point.style.iconstyle.color = class_json[clm]["color"]
                point.coords = [(row[longitude], row[latitude], row[altitude])]
                point.altitudemode = simplekml.AltitudeMode.absolute
                point.style.iconstyle.icon.href = "./configfile/icon.png"
                point.style.iconstyle.scale = 0.3
                point.style.labelstyle.scale = 0
        #results_gradation
        time.sleep(1)
        print("processing...........")
        time.sleep(2)
        print("\n--------------results-----------------")
        print("target_column = " + target_column)
        print(sorted_class_list)
        if wow_replacement ==  "y" or wow_replacement ==  "yes":
            print("Warning!! Missing values in row " + str(missing_values) + " were replaced with the previous value")
        elif wow_replacement ==  "n" or wow_replacement ==  "no":
            print("Warning!!　Exclude " + str(missing_values) + " rows of missing values")
        else:
            pass        
        print("--------------------------------------\n")

    #visualization_gradation
    #select_range
    elif set_method == "range":
        print("\nSelect the range template you wish to use.\
            \nThe range template can be changed to any value and color from 'config.json'.")
        print("--------------------------------------")
        for index,item in enumerate(range_list):
            print(index,item)
        print("--------------------------------------")
        string = ""
        while string not in ["0", "1", "2"]:
            string = input()
            if string=="0":
                range_num = "range1"
                color_num = "color1"
                range_int = int(string)
            elif string=="1":
                range_num = "range2"
                color_num = "color2"
                range_int = int(string)
            elif string=="2":
                range_num = "range3"
                color_num = "color3"
                range_int = int(string)
            else:
                print("Incorrect input !! Please enter the correct value again.")
                continue
        
        #initi_range
        r1 = jf["ranges"][range_int][range_num][0] # under r1 
        r2 = jf["ranges"][range_int][range_num][1] #r1 <= value < r2
        r3 = jf["ranges"][range_int][range_num][2] #r2 <= value < r3
        r4 = jf["ranges"][range_int][range_num][3] #r3 <= value < r4
        r5 = jf["ranges"][range_int][range_num][4] #r4 <= value < r5
        #init_df
        range_1 = df[df[target_column] < r1]
        range_2 = df[(df[target_column]  >= r1) & (df[target_column]  < r2)]
        range_3 = df[(df[target_column]  >= r2) & (df[target_column]  < r3)]
        range_4 = df[(df[target_column]  >= r3) & (df[target_column]  < r4)]
        range_5 = df[(df[target_column]  >= r4) & (df[target_column]  < r5)]
        range_6 = df[df[target_column]  >= r5]

        #qty_range
        qty_range_1 = len(range_1)
        qty_range_2 = len(range_2)
        qty_range_3 = len(range_3)
        qty_range_4 = len(range_4)
        qty_range_5 = len(range_5)
        qty_range_6 = len(range_6)
        #qty_rate
        rate_range_1 = round(qty_range_1/len(df)*100,2)
        rate_range_2 = round(qty_range_2/len(df)*100,2)
        rate_range_3 = round(qty_range_3/len(df)*100,2)
        rate_range_4 = round(qty_range_4/len(df)*100,2)
        rate_range_5 = round(qty_range_5/len(df)*100,2)
        rate_range_6 = round(qty_range_6/len(df)*100,2)
        #name_landmarks
        place_mark_1 = "under "+ str(r1) + " (" + str(rate_range_1) + "%, " +  str(qty_range_1) + ")"
        place_mark_2 = str(r1) +" to " + str(r2) + " (" + str(rate_range_2) + "%, " +  str(qty_range_2) + ")"
        place_mark_3 = str(r2) +" to " + str(r3) + " (" + str(rate_range_3) + "%, " +  str(qty_range_3) + ")"
        place_mark_4 = str(r3) +" to " + str(r4) + " (" + str(rate_range_4) + "%, " +  str(qty_range_4) + ")"
        place_mark_5 = str(r4) +" to " + str(r5) + " (" + str(rate_range_5) + "%, " +  str(qty_range_5) + ")"
        place_mark_6 = str(r5) + " and above " + "(" + str(rate_range_6) + "%, " +  str(qty_range_6) + ")"
        #add_landmarks
        kml = simplekml.Kml()
        place_marks = [place_mark_1,place_mark_2,place_mark_3,place_mark_4,place_mark_5,place_mark_6]
        multi_geometry_list = []
        for place_mark in place_marks:
            multi_geometry = kml.newmultigeometry(name=place_mark)
            multi_geometry_list.append(multi_geometry)    
        colors = jf["ranges"][range_int][color_num]
        for index,row in df.iterrows():         
            point = None
            clm = float(row[target_column])
            if clm < r1:
                point = multi_geometry_list[0].newpoint()
                point.style.iconstyle.color = simplekml.Color.hex(colors[0])
                
            elif r1 <= clm < r2:
                point = multi_geometry_list[1].newpoint()
                point.style.iconstyle.color = simplekml.Color.hex(colors[1])
            elif r2 <= clm < r3:
                point = multi_geometry_list[2].newpoint()
                point.style.iconstyle.color = simplekml.Color.hex(colors[2])
            elif r3 <= clm < r4:
                point = multi_geometry_list[3].newpoint()
                point.style.iconstyle.color = simplekml.Color.hex(colors[3])
            elif r4 <= clm < r5:
                point = multi_geometry_list[4].newpoint()
                point.style.iconstyle.color = simplekml.Color.hex(colors[4])
            else:
                point = multi_geometry_list[5].newpoint()
                point.style.iconstyle.color = simplekml.Color.hex(colors[5])
            point.coords = [(row[longitude], row[latitude], row[altitude])]
            point.altitudemode = simplekml.AltitudeMode.absolute
            point.style.iconstyle.icon.href = "./configfile/icon.png"
            point.style.iconstyle.scale = 0.3               
            point.name = row[target_column]
            point.style.labelstyle.scale = 0

        #range_results
        time.sleep(1)
        print("processing.........\n")
        time.sleep(2)        
        print("--------------results-----------------")
        print("target_column = " + target_column)
        print("valid raw count " + str(len(df)))
        print(place_mark_1)
        print(place_mark_2)
        print(place_mark_3)
        print(place_mark_4)
        print(place_mark_5)
        print(place_mark_6)
        if wow_replacement ==  "y" or wow_replacement ==  "yes":
            print("Warning!! Missing values in row " + str(missing_values) + " were replaced with the previous value")
        elif wow_replacement ==  "n" or wow_replacement ==  "no":
            print("Warning!!　Exclude " + str(missing_values) + " rows of missing values")
        else:
            pass
        print("--------------------------------------\n")
    #select_savefmt
    time.sleep(2)      
    save_format_list = ["kml","kmz","close"]
    print("\nPlease select the following save format")
    print("--------------------------------------")
    for index,item in enumerate(save_format_list):
        print(index,item)
    print("--------------------------------------")  
    string = ""
    while string not in ["kml","kmz","0","1"]:
        string = input()
        if string == "2" or string == "close":
            print("Canceled.")
            time.sleep(3)
            exit()            
        elif string=="0" or string == "kml":
            string = "0"
        elif string=="1" or string == "kmz":
            string = "1"
        else:
            print("Incorrect input !! Please enter the correct value again.")
            continue

    #save
    rp_target_column = target_column.replace("/","_")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    savename = "(" + rp_target_column + ")_" + set_method + "_" + source_file[:-4]
    if string=="0" or string=="kml":
        if not os.path.exists(save_dir+ "configfile"):
            os.makedirs(save_dir + "configfile")
        if not os.path.exists(save_dir + "configfile/icon.png"):
            shutil.copy("./configfile/icon.png", save_dir + "configfile/icon.png")        
        kml.save(save_dir + savename + ".kml")
        print("saved file name > " + savename + ".kml")
    elif string=="1" or string =="kmz":
        kml.savekmz(save_dir + savename + ".kmz")
        print("saved file name > " + savename + ".kmz")

    v = input("""
    続行するには何かキーを押してください > 
    """)



# except Exception as e:
#     print("\nエラーが発生しました。解決しない場合はサポートへ発生タイミングと以下のエラー内容を伝えてください。")
#     print(e)
#     time.sleep(60)    