#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os


# In[2]:


import warnings
warnings.filterwarnings('ignore')


# In[3]:


#Part 1
#LETTING DATE         (done)
#LETTING TYPE         (done)
#CONTRACT NUMBER      (done)
#LETTING ITEM NUMBER  (done)
#RESPONSIBLE DISTRICT  (done)
#BIDS LOCKED          (done)
#SECTION              (done)
#COUNTY               (done)
#ESTIMATE             (done)
#State Job Number     (done)
#Municipality         (done)
# Part 2
# Bidder Number (done)
# Bidder Name   (done)
# "AS Read" Bidder Total Price  
# Summation of Bidders Extension
# Summation of calculated Extensions
# Low Bid       (done)
# Item Number  (done)
# Item Description (done)
# Quantity  (done)
# Unit of Measure (done)
# Bidder Number   (done)
# Bidder Name     (done)
# Unit Price      (done)
# Bidder Extension  (done)
# Calculated extension  (done)


# In[4]:


Total_dataframes=[]
for file in os.listdir():
    if file.endswith(".txt"):
        print(file)
        content = open(file,"r")
        ##################Dataframe
        column_name=["LETTING_DATE","LETTING TYPE","CONTRACT NUMBER","LETTING ITEM NUMBER",
             "RESPONSIBLE DISTRICT","BIDS LOCKED","SECTION","COUNTY","ESTIMATE",
             "STATE JOB NUMBER","MUNICIPALITY","PROJECT NUMBER","BIDR NBR","BIDDER NAME","AS Read Bidder Total Price","SUMMATION OF BIDDER EXTENSIONS","SUMMATION OF CALCULATED EXTENSIONS","LOW BID",
             "ITEM NBR","ITEM DESCRIPTION","UNIT OF MEASURE","QUANTITY"]
        Output_dataframe = pd.DataFrame()
        for name in column_name:
            Output_dataframe[name]=" "
        ###################Part 1
        counter=1
        for line in content:
            result = " ".join(line.split()).strip()
            #Line 3
            if(counter==3):
                list_line_3=[temp.strip() for temp in result.split(":")]
                #Letting Item Number
                letting_item_number=str(list_line_3[-1])
                #Letting Date
                letting_date = list_line_3[1].strip().split(" ")[0]
                #Letting Type
                letting_type = list_line_3[2].strip().split(" ")[0].title()
                #Contract Number
                contract_number = "#"+list_line_3[3].strip().split(" ")[0]
            #Line 4
            if(counter==4):
                list_line_4=[temp.strip() for temp in result.split(":")]
                #Responsible District
                responsible_district=list_line_4[1].split(" ")[0]
                #Bids Locked
                bids_locked=list_line_4[-1]
            #line 5
            if(counter==5):
                list_line_5=[temp.strip() for temp in result.split(":")]
                #Section
                section=list_line_5[1].split(" ")
                section=" ".join(section[:-1])
                #County
                county=list_line_5[2].split(" ")[0:-1]
                county=" ".join(county)
                #Estimate
                estimate=list_line_5[-1]
            if(counter==6):
                if("------" in result):
                    #print("Done Part 1")
                    #part_1_start=9
                    State_Job_Number=" "
                    Municipality=" "
                    Project_Number=" "
                    break
            if(counter==6):
                list_line_6=[temp.strip() for temp in result.split(":")]
                #STATE Job  Number 
                State_Job_Number=list_line_6[1].split(" ")[0]
                #Municipality
                Municipality=list_line_6[-1]
            if(counter==7):
                list_line_7=[temp.strip() for temp in result.split(":")]
                #Project Number
                Project_Number=list_line_7[-1]
            if(counter==9):
                if("SUMMARY OF CONTRACTOR BIDS" in result):
                    #print("Done Part 1")
                    #part_1_start=11
                    break
            counter=counter+1  
        ###################Part 2
        Number_of_bidders=0
        for line in content:
            result = " ".join(line.split()).strip()
            #
            result=result.split(" ")
            try:
                #Bidder Number
                Bidder_Number=int(result[0][-1])
                Bidder_Number=result[0]
                Bidder_Name=" ".join(result[1:]).strip()
                Number_of_bidders=Number_of_bidders+1
            except:
                pass
            #Remove Last Row
            if("TOTAL GROUP NO ALT PAY ITEMS FOR THIS CONTRACT" in line):
                total_group_alt_pay=line.split("=")[1].strip()
                break
            
            if("NO ALT" in line):
                if("*" in line):
                    Low_Bid = "*"
                else:
                    Low_Bid = ""
                line=line.strip()
                result=line.split(" ")
                line=line.replace("NO ALT","")
                line=line.strip()
                line=line.split(" ")
                line=[temp for temp in line if temp!='*']
                line=[temp for temp in line if temp!='']
                as_read_bidder_total_price=float(line[0].replace(",",""))
                summation_of_bidder_extension=float(line[1].replace(",",""))
                summation_of_calculated_extension=float(line[2].replace(",",""))
                Output_dataframe = Output_dataframe.append({
                    'LETTING_DATE':letting_date,'LETTING TYPE': letting_type,'CONTRACT NUMBER':contract_number,
                    'LETTING ITEM NUMBER':letting_item_number,"RESPONSIBLE DISTRICT":responsible_district,
                    "BIDS LOCKED":bids_locked,"SECTION":section,"COUNTY":county,"ESTIMATE":estimate,
                    "STATE JOB NUMBER":State_Job_Number,"MUNICIPALITY":Municipality,"PROJECT NUMBER":Project_Number,
                    "BIDR NBR":Bidder_Number,"BIDDER NAME":Bidder_Name,"AS Read Bidder Total Price":as_read_bidder_total_price,
                    "SUMMATION OF BIDDER EXTENSIONS":summation_of_bidder_extension,"SUMMATION OF CALCULATED EXTENSIONS":summation_of_calculated_extension,
                    "LOW BID":Low_Bid},ignore_index=True)
        Output_dataframe["Total Group AlT pay"]=total_group_alt_pay
        ###################Part 3
        #print("Part 3")
        list_of_bidder_numbers=list(Output_dataframe["BIDR NBR"].unique())
        item_number_list=[]
        quantity_list=[]
        unit_of_measure_list=[]
        quantity_list=[]
        item_Description_list=[]
        rest_of_lines=[]
        for line in content:
            line_analysis="     ".join(line.split()).strip().split("    ")
            try:
                temp_number=int(line_analysis[0][-1])
                temp_number=line_analysis[0]
            except:
                continue
            if(temp_number in list_of_bidder_numbers):
                rest_of_lines.append(line)
                for bidder in range(0,Number_of_bidders):
                    rest_of_lines.append(content.readline())
            else:
                #Item Number
                item_number=line_analysis[0]
                item_number_list.append(item_number)
                line=line.replace(item_number,"")
                line=line.strip().split("   ")
                line=[temp for temp in line if temp!='']
                #Unit of Measure
                unit_of_measure=line[-1].strip()
                unit_of_measure_list.append(unit_of_measure)
                #Quantity
                quantity=float(line[-2].strip().replace(",",""))
                quantity_list.append(quantity)
                #Item Description
                item_Description=line[0:-2]
                item_Description=" ".join(item_Description).strip()
                item_Description_list.append(item_Description) 
        ###################Second Part
        Output_dataframe=pd.concat([Output_dataframe]*len(item_number_list), ignore_index=True)
        for temp in range(0,len(item_number_list)):
            indexes_to_adjust=list(Output_dataframe.iloc[temp*Number_of_bidders:temp*Number_of_bidders+Number_of_bidders].index)
            Output_dataframe.loc[indexes_to_adjust,"ITEM NBR"]=item_number_list[temp]
            Output_dataframe.loc[indexes_to_adjust,"ITEM DESCRIPTION"]=item_Description_list[temp]
            Output_dataframe.loc[indexes_to_adjust,"UNIT OF MEASURE"]=unit_of_measure_list[temp]
            Output_dataframe.loc[indexes_to_adjust,"QUANTITY"]=quantity_list[temp]
        rest_of_lines=[temp.strip() for temp in rest_of_lines]
        rest_of_lines=[temp for temp in rest_of_lines if len(temp)>1]
        column_name=["BIDR NBR","BIDDER NAME","UNIT PRICE","BIDDER EXTENSION","CALCULATED EXTENSION"]
        Output_dataframe_2 = pd.DataFrame()
        for name in column_name:
            Output_dataframe_2[name]=" "
            
        ##
        rest_of_lines_total=[]
        move_on=-1
        for x in range(0,len(rest_of_lines)):
            if(move_on==x):
                continue
            try:
                temp_check=rest_of_lines[x].strip().split("   ")
                temp_check=[temp for temp in temp_check if temp!='']
                unit_price=float(temp_check[-1].strip().replace(",",""))
                rest_of_lines_total.append(rest_of_lines[x])
            except:
                temp=" ".join(rest_of_lines[x:x+2])
                rest_of_lines_total.append(temp)
                move_on=x+1
        rest_of_lines=rest_of_lines_total
        #
        for line in rest_of_lines:
            line=line.strip().split("   ")
            line=[temp for temp in line if temp!='']
            unit_price=float(line[-3].strip().replace(",",""))
            bidder_extension=float(line[-2].strip().replace(",",""))
            calculated_extension=float(line[-1].strip().replace(",",""))
            #Bidder Number
            Bidder_Number=line[0]
            Bidder_Name=line[1].strip()
            for temp_name in list(Output_dataframe['BIDDER NAME'].unique()):
                if temp_name in Bidder_Name:
                    Bidder_Name=temp_name
            Output_dataframe_2 = Output_dataframe_2.append(
                {
                    'BIDR NBR':Bidder_Number,'BIDDER NAME': Bidder_Name,'UNIT PRICE':unit_price,
                    'BIDDER EXTENSION':bidder_extension,'CALCULATED EXTENSION': calculated_extension
                },ignore_index=True)
        ##
        #Sor Values by Bidder Name
        #Output_dataframe_2=Output_dataframe_2.sort_values(by="BIDDER NAME")
        #Output_dataframe=Output_dataframe.sort_values(by="BIDDER NAME")
        #Output_dataframe_2=Output_dataframe_2.reset_index()
        #Output_dataframe=Output_dataframe.reset_index()
        #total=pd.merge(Output_dataframe,Output_dataframe_2,on=["index","BIDR NBR","BIDDER NAME"])
        #total.drop(columns=["index"],inplace=True)
        #Total_dataframes.append(total)
        final_dataframe=[]
        for i in range(0,int(Output_dataframe.shape[0]/Number_of_bidders)):
            start_idx = i * Number_of_bidders
            end_idx = start_idx + Number_of_bidders
            
            # Get the chunk of rows
            chunk_1 = Output_dataframe.iloc[start_idx:end_idx]
            chunk_2 = Output_dataframe_2.iloc[start_idx:end_idx]
            merged=pd.merge(chunk_1,chunk_2,on=["BIDR NBR","BIDDER NAME"])
            final_dataframe.append(merged)
        concatenated_df = pd.concat(final_dataframe, ignore_index=True)
        Total_dataframes.append(concatenated_df)


# In[5]:


concatenated_df = pd.concat(Total_dataframes, ignore_index=True)


# In[7]:


concatenated_df.to_excel(r'Output_File.xlsx', index=False)

