# 1000-Genome
python scripts to analyze VCF data from NCBI 1000 Genome Browser

i have written several python scripts which i am using to extract Allele Frequencies (AFs) from data downloaded from
the NCBI 1000 Genome Browser. Bascically, the scripts ask input from the keyboard for file name, and start and stop 
positions on the genome. Then the file is converted to a Pandas DataFrame. Then a loop is setup to iterate over all of the 
rows, each of which is a variant position in the database compared to the reference genome. For each row, the information line, column 7, is chosen because it contains the AFs of interest.First, the row position is checked to be sure it is in the correct gene position, that is between the start and end positions.  This slice of information is converted to a dictionary after removing the "_" character and replacing with "=". From the dictionary the AF value is chosen, any stray commas eliminated, converted from string to float and than placed into the proper bin for the frequency.Finally, a histogram is made from the results.

HERE IS THE PRIMARY PROGRAM "snp_group.py"



import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

start = int(input("Enter start position: "))
end = int(input("Enter end position: "))

file = input("Enter the data file name: ")

title = input("Enter Title of the Plot  ")
print("file = ",file)



#now a pandas data frame is made from the downloaded data file
data_raw= pd.read_csv(file, sep='\t', header=None,comment='#')


row_num= data_raw.shape[0]
print('the number of rows = ',row_num)



#the variant frequency data is in column index # 7, so below is that slice of the 'data' DataFrame, named 'freq'
freq = data_raw.iloc[ : ,7]
#print(freq.iloc[8])
print('type= ',type(freq))



#now iterate over all rows of the slice 'freq' and select the data from a dictionary at each iteration, and called 'l', which is a string.
#since there are "row_num" rows to iterate over and the first row has index=0...
rare = 0
uncommon = 0
common5 = 0
common10 = 0
common20 = 0

for i in range(0,row_num):
    if data_raw.iloc[i,1] >= start and data_raw.iloc[i,1] <= end:  #column 1 contains the location on the chromosome
        #print('here is the position; ',data_raw.iloc[i,1])
        l = freq[i]
        #print(l)
        #print(type(l))
        q = l.replace('I_A','I=A') #replacing element #9 'MULTI_ALLELIC' corruption. If the data has multi allelic SNP, then you must check to be sure a common variant has not been missed.

#next the string 'l' cleaned up to remove a '_' and replace it with an '=' so all elements contain '=' separating key from value
        r=q.replace('X_T','X=T')
        #print(r)

#now the cleaned up string 'r' will be made into a dictionary of key:value pairs, called 'column7'
        column7={}


#there are 14 results in column index=7 of the 'data' DataFrame, the INFO column, so j is set to range (0,13)
#need to make this string l into a dictionary or 14 key:value pairs

        column7= dict(e.split('=') for e in r.split(';'))

        #print(column7['EUR_AF'])
# the above dictionary 'column7' has only string values, so these must be converted to floats for calculations.
#the particular datum I am interested in is the key 'AF' in the dictionary 'column7', the value is a string.
        AF_val=column7['AF']
        
        #print(AF_val)
        #print(type(AF_val))
        #need to eliminate commas from AF_val
        AF_val_no_comma = AF_val.replace(',0.','')

#now the string value is converted to a float, 'AF_num', which can be used in calculations.
        AF_num=float(AF_val_no_comma)        
                
        if AF_num > 0.5:
            AF_num = 1 - AF_num 
                
        if AF_num < 0.005:
            rare = rare +1
            
        if AF_num >= 0.005 and AF_num < 0.05:
            uncommon = uncommon +1
        
        if AF_num >= 0.05 and AF_num < 0.1:
            common5 = common5 +1
            
        if AF_num >= 0.1 and AF_num < 0.2:
            common10 = common10 + 1
            
        if AF_num >= 0.2 and AF_num < 0.5:
            common20 = common20 +1
            

        
    
print('rare = ',rare, ' .005-.05 =', uncommon, ' 0.05-0.1 =',common5, ' 0.1-0.2 =',common10, ' 0.2-0.5 =', common20 )

list = []
list.append(rare) 
list.append(uncommon)
list.append(common5)
list.append(common10)
list.append(common20)
print('frequency list = ',list)

objects = ('<0.005', '0.005-0.05', '0.05-0.1','0.1-0.2', '0.2-0.5')

y_pos = np.arange(len(objects))


plt.bar(y_pos, list, align = 'center', alpha = 0.5, color='blue')
plt.xticks(y_pos, objects)
plt.ylabel('Number')
plt.title(title)

plt.show()


