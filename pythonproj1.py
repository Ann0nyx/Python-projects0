'''
CITS1401, semester 1 ,PROJECT - 2

Student Id - 24529993
Student Name: Ann Maria Saji
Date: 19 May 2025

AIM: To write a Python 3 program that will read two CSV file and analyse the data in the files and return 3 different outputs.

Note:
1)No modules have been imported in this program
2)print statement has only been used in the case of a graceful termination
'''
#opening file through this function,which takes both the files as arguments
#and using a try except block to catch file related error
def header_filter(file):
    header = file.readline() #just reads the first row, which is the column header
    header = header.lower().strip().split(',')#converts header row into a list of lower case column names
    return header

def openfile(csvfile_1, csvfile_2):
    check = 0 #This is to identify which file is open,to close it if an error occurs
    try:
        file1 = open(csvfile_1,'r')
        check = 1
        file2 = open(csvfile_2,'r')
    except IOError:
        if check == 1:
            file1.close()#closing the area file,doesnt close the other file since its not open

        print("IOError: File not found")
        return None,None,None,None
    
    header1 = header_filter(file1)#calling finction 
    header2 = header_filter(file2)
    
    for num in range(len(header1)):
        header1[num] = header1[num].strip().lower()#converts rest of rows into a list of lower case strings
            
    rows = file1.readlines()#reads the entire file except the header of area file
    rows1 = []
    
    for i in rows:
        rows1.append(i.lower().strip().split(','))
    
    for i in range(len(header2)):
        if '-' in header2[i]:
            header2[i] = header2[i][4:].lower()
        elif 'and' in header2[i].lower():
            header2[i] = header2[i].replace(' and over','-None')
            header2[i] = header2[i][4:]
        else:
            header2[i] = header2[i].lower()
            
    rows = file2.readlines()#reads the entire file except the header of population file
    rows2 = []
    for i in rows:
        rows2.append(i.strip().lower().split(','))
    file1.close()#closing the area file
    file2.close()#closing the population file
    return header1,rows1,header2,rows2
#This function creates a dictionary with each key/column name mapped to its index value
def build_header_index(header):
    index_map = {}
    for i in range(len(header)):
        column_name = header[i].strip()#removes any excess white spaces
        index_map[column_name] = i
    return index_map

#This function is for removing all occurences of duplicate values from either of the files
def rem_duplicate(items1,index_area,items2, index_pop):
    dup_list = []
    uniq_list = []
    
    #going through population file to find and remove any duplicate rows
    for i in items2:
        if i[index_pop['area_code_level2']] in uniq_list and i[index_pop['area_code_level2']] not in dup_list:
            dup_list.append(i[index_pop['area_code_level2']])
        elif i[index_pop['area_code_level2']] in uniq_list and i[index_pop['area_code_level2']] in dup_list:
            pass
        else:
            uniq_list.append(i[index_pop['area_code_level2']])
            
    copy2 = items2.copy()
    for i in copy2:
        if i[index_pop['area_code_level2']] in dup_list:
            items2.remove(i)
    
    #removing the corresponding duplicate row from area file
    copy1 = items1.copy()
    for j in copy1:
        if j[index_area['sa2 code']] in dup_list:
            items1.remove(j)
       
    dup_list = []
    uniq_list = []
    
    #going  through area file to find and remove duplicate rows
    for k in items1:
        if k[index_area['sa2 code']] in uniq_list and k[index_area['sa2 code']] not in dup_list:
            dup_list.append(k[index_area['sa2 code']])
        elif k[index_area['sa2 code']] in uniq_list and k[index_area['sa2 code']] in dup_list:
            pass
        else:
            uniq_list.append(k[index_area['sa2 code']])
            
    copy2 = items2.copy()
    for i in copy2:
        if i[index_pop['area_code_level2']] in dup_list:
            items2.remove(i)
    
    #removing corresponding rows from population file
    copy1 = items1.copy()
    for j in copy1:
        if j[index_area['sa2 code']] in dup_list:
            items1.remove(j)                
    return items1,items2
#This function filters the header, removing any invalid column name.
def sort_header(header1,items1,header2,items2):
    
    index_area = build_header_index(header1)
    index_pop = build_header_index(header2)
    
    dict1={}
    dict2={}
    age_grp_index={}
    
    #This is for filtering out any invalid columns and to also make sure all the columns are in place
    try:
        dict1['sa2 code'] = index_area['sa2 code']
        dict1['sa2 name'] = index_area['sa2 name']
        dict1['sa3 code'] = index_area['sa3 code']
        dict1['sa3 name'] = index_area['sa3 name']
        dict1['s_t code'] = index_area['s_t code']
        dict1['s_t name'] = index_area['s_t name']
        
        dict2['area_code_level2']= index_pop['area_code_level2']
        dict2['area_name_level2']= index_pop['area_name_level2']
    except KeyError :
        print("Error:Cant find column")
        return [],[],{},{},{}
    #creates a seperate index dictionary for just age groups
    for column in index_pop:
        if '-' in column:
            age_grp_index[column] = index_pop[column] #this puts the age group and index in a seperate dictionary 
    #to ignore any invalid columns keys within age_grp_index
    ag_copy = age_grp_index.copy()
    for ag in ag_copy:
        for i in ag:
            if i in '()*^%$#@!~`=_+][{}|/".,<>?:;':
                del age_grp_index[ag]
                break
     
    index_pop = dict2 #this dictionary has the other column names and index of population file other than age-group columns
    index_area = dict1 #This dictionary has all the colum names and index of area file
    
    items1,items2 = rem_duplicate(items1,index_area,items2, index_pop)#returns the rows of both the files after removing duplicates
    
    return items1,items2,index_area,index_pop,age_grp_index
#removes invalid rows having negative number, missing values, wrong formats
def remove_inv_rows(items1, items2, index_area, index_pop, age_grp_index):
    del_list = set()  # Store SA2 codes to remove from both datasets, using sets to store unique values
    pop_column_all_index = list(index_pop.values())+list(age_grp_index.values())

    # Removing invalid population rows
    for row in items2[:]: 
        if len(row) <= max(pop_column_all_index):
            del_list.add(row[index_pop['area_code_level2']])
            items2.remove(row)
            continue

        sa2_code = row[index_pop['area_code_level2']]
        invalid = False
        for index in age_grp_index.values():
            if not negative_num_check(row, index):#calls a subfunction to check for invalid values
                invalid = True
                break
        missing = False
        for index in index_pop.values():
            if len(row[index].strip()) == 0:
                missing = True
                break

        if invalid or missing: #checking whether condition true
            del_list.add(sa2_code)
            items2.remove(row)
            continue
        if not negative_num_check(row, index_pop['area_code_level2']):
            del_list.add(sa2_code)
            items2.remove(row)
    # Removing corresponding area rows
    for row in items1[:]:
        if row[index_area['sa2 code']] in del_list:
            items1.remove(row)

    # Checking for invalid area rows
    for row in items1[:]:
        if len(row) <= max(index_area.values()):
            del_list.add(row[index_area['sa2 code']])
            items1.remove(row)
            continue
        is_empty = False
        for i in index_area.values(): #checking to make sure there is no empty values
            if len(row[i].strip()) == 0:
                is_empty = True
                break
        if is_empty:
            del_list.add(row[index_area['sa2 code']])
            items1.remove(row)
            continue
        if not negative_num_check(row, index_area['sa2 code']):
            del_list.add(row[index_area['sa2 code']])
            items1.remove(row)
    # Removing corresponding population rows again
    for row in items2[:]:
        if row[index_pop['area_code_level2']] in del_list:
            items2.remove(row)
    return items1, items2
   
def get_largecode_with_sorting(data_dict): #function for sorting out area by largest population
    
    max_pop = -1 #asigning initial variable
    max_code = None
    
    for code in data_dict:
        pop = data_dict[code][1]
        if pop > max_pop:
            max_pop = pop
            max_code = code
            
        #for tiebreaking if there exists two largest population area codes
        elif pop == max_pop and (max_code is None or code < max_code): 
            max_code = code
    return max_code

# Function to calculate cosine similarity between two vectors
def cosine_similarity(li_st_pop1, li_st_pop2):
    sum1 = sum(li_st_pop1)
    sum2 = sum(li_st_pop2)
    
    #handling error
    if sum1 == 0 or sum2 == 0:
        return 0
    
    # Convert to a list of percentage vectors
    p1 = [value / sum1 for value in li_st_pop1]
    p2 = [value / sum2 for value in li_st_pop2]

    numerator = sum(a * b for a, b in zip(p1, p2)) #numerator is the sum of product of corresponding percentage vectors in p1,p2
    
    root1 = sum(a * a for a in p1) ** 0.5 #for finding root of sum of percentage square in p1
    root2 = sum(b * b for b in p2) ** 0.5 #for finding root of sum of percentage square in p2
    #handling error to prevent zero devision error
    if root1 == 0 or root2 == 0:
        return 0

    return numerator / (root1 * root2)
#sub function used to check for negative data and wrong format, its been called in multiple functions
def negative_num_check(row2,age_index):
    try:
        population_num = int(row2[age_index])
        # checks whether the population in that column is negative or none
        if population_num < 0 or population_num == None or population_num == '': 
            return False
        return True
    except:
        return False
#output 1 function that returns a dictionary with age group keys and values being a list containing state name,sa3 name,sa2 name with the largest area in that particular age group
def output_1(items1,items2,index_area,index_pop,age_grp_index):
    
    op1 = {}

    # Building a dictionary with SA2 codes as keys and values: {sa2 name, sa3 code, sa3 name, state code, state name}
    sa2_data = {}
    for row in items1:
        sa2code = row[index_area['sa2 code']].strip()
        sa2_data[sa2code] = { 'sa2 name': row[index_area['sa2 name']].strip().lower(),'sa3 code': row[index_area['sa3 code']].strip(),
                           'sa3 name': row[index_area['sa3 name']].strip().lower(),'state code': row[index_area['s_t code']].strip(),
                           'state name': row[index_area['s_t name']].strip().lower()}

    # For each age group, iterates over each age group
    for age in age_grp_index:
        column = age_grp_index[age]

        state_totals = {}
        sa3_totals = {}
        sa2_totals = {}

        for row in items2:
            sa2_code = row[index_pop['area_code_level2']].strip()
            if sa2_code not in sa2_data:
                continue
            if not negative_num_check(row,column):
                continue
            else:
                population = int(row[column])

            info = sa2_data[sa2_code]
            state_code = info['state code']
            sa3_code = info['sa3 code']
            
            # records the population of each State
            if state_code not in state_totals:
                state_totals[state_code] = [info['state name'], 0]
            state_totals[state_code][1] += population #This line of code updates the population through each iteration

            # records the population of each SA3 area
            if sa3_code not in sa3_totals:
                sa3_totals[sa3_code] = [info['sa3 name'], 0]
            sa3_totals[sa3_code][1] += population #This line of code updates the population through each iteration

            # records the population of each SA2 area
            if sa2_code not in sa2_totals:
                sa2_totals[sa2_code] = [info['sa2 name'], 0]
            sa2_totals[sa2_code][1] += population #This line of code updates the population through each iteration

        # geting max population with sorting and tie breaking
        # calling function
        max_state_code = get_largecode_with_sorting(state_totals)
        max_sa3_code = get_largecode_with_sorting(sa3_totals)
        max_sa2_code = get_largecode_with_sorting(sa2_totals)
        
        if max_state_code and max_sa3_code and max_sa2_code:
            op1[age] = [state_totals[max_state_code][0],sa3_totals[max_sa3_code][0],sa2_totals[max_sa2_code][0]]

    return op1

def output_2(items1, items2, index_area, index_pop, age_grp_index):
    op2 = {}
    #mapping sa2 code to sa3 and state code
    sa2_data = {}
    for row in items1:
        sa2_code = row[index_area['sa2 code']]
        sa2_data[sa2_code] = { 'sa3_code': row[index_area['sa3 code']],'state_code': row[index_area['s_t code']] }

    #SA2 population
    sa2_populations = {}
    for row in items2:
        sa2_code = row[index_pop['area_code_level2']]
        if sa2_code not in sa2_data:
            continue
        total = 0
        valid = True
        for i in age_grp_index.values():
            if negative_num_check(row,i):# calling function for check
                value = int(row[i])
                total += value
            else:
                valid = False
                break
        if valid:
            sa2_populations[sa2_code] = total

    #dictionary for storing state code and its corresponding sa3 as values
    sa3_state_dict = {}
    for sa2_code, pop in sa2_populations.items():
        sa3_code = sa2_data[sa2_code]['sa3_code']
        state_code = sa2_data[sa2_code]['state_code']
        
        if state_code not in sa3_state_dict:
            sa3_state_dict[state_code] = {}
            
        if sa3_code not in sa3_state_dict[state_code]:
            sa3_state_dict[state_code][sa3_code] = [0, {}]  # [total_pop, sa2_dict]
            
        sa3_state_dict[state_code][sa3_code][0] += pop
        sa3_state_dict[state_code][sa3_code][1][sa2_code] = pop

    #Build OP2 output
    for state_code in sorted(sa3_state_dict.keys(), key=str):# to make sure all the codes are in string format
        op2[state_code] = {}
        
        for sa3_code in sorted(sa3_state_dict[state_code].keys(), key=str):
            total_pop, sa2_dict = sa3_state_dict[state_code][sa3_code]
            
            if total_pop >= 150000:
                # Get max SA2 (with tie-breaking)
                max_sa2 = min([code for code, p in sa2_dict.items() if p == max(sa2_dict.values())])
                max_pop = sa2_dict[max_sa2]

                # Step 5: Calculate standard deviation
                pops = []
                for row in items2:
                    if row[index_pop['area_code_level2']] == max_sa2:#checking whether the sa2 area code matches that of max sa2 area code
                        for i in age_grp_index.values():
                            if negative_num_check(row,i):
                                pops.append(int(row[i]))
                            else:
                                continue
                        break
                if len(pops) > 1: #to make there is always more than one element
                    try:
                        avg = sum(pops) / len(pops) #for finding the standard diviation
                        var_iance = sum((x - avg) ** 2 for x in pops) / (len(pops) - 1)
                        std_dev = round(var_iance ** 0.5, 4)
                    #except TypeError: #handles typeError
                        #std_dev = 0
                    except ValueError:#handles ValueErrors
                        std_dev = 0
                else:
                    std_dev = 0

                # Save final result to op2
                op2[state_code][sa3_code] = [max_sa2, max_pop, std_dev]

    return op2

def output_3(rows_areas, rows_pop, index_areas, index_pop, age_groups):
    # creating a dictionary for mapping sa3 areas with a list of tuples having sa2 area name and code
    sa3_to_sa2list = {}
    # creating a dictionary for mapping sa2 code with sa2 name
    sa2code_to_nam = {}

    # Building the SA3 mapped to SA2 list
    for row1 in rows_areas:
        sa3_name = row1[index_areas['sa3 name']]
        sa2_name = row1[index_areas['sa2 name']]
        sa2_code = row1[index_areas['sa2 code']]
        sa3_to_sa2list.setdefault(sa3_name, [])
        sa3_to_sa2list[sa3_name].append((sa2_name, sa2_code)) #appending the tuple with sa2 name and code
        sa2code_to_nam[sa2_code] = sa2_name

    # Build population vectors for each SA2 for all age groups
    sa2_pop_dict = {}
    for row2 in rows_pop:
        sa2_code = row2[index_pop['area_code_level2']]
        if sa2_code not in sa2code_to_nam:
            continue

        # Collect population counts for all age groups
        list_population = []
        valid = True
        for age_index in age_groups.values():
            if negative_num_check(row2,age_index): #calling function
                list_population.append(int(row2[age_index]))
            else:
                valid = False
                break   
        if valid:
            sa2_pop_dict[sa2_code] = list_population

    op3 = {} #initializing variable(error corrected)
    # Process each SA3 with at least 15 SA2 areas
    for sa3_name, sa2_list in sa3_to_sa2list.items():
        
        if len(sa2_list) < 15:
            continue
        max_similarity = -1 #defining variable
        best_pair = None

        # Sort SA2 areas alphabetically
        sa2_list_sorted = sorted(sa2_list, key=lambda x: x[0])

        # Compare each pair to find max cosine similarity
        for indx in range(len(sa2_list_sorted)): 
            name1, code1 = sa2_list_sorted[indx]
            li_st_pop1 = sa2_pop_dict.get(code1)
            
            if li_st_pop1 is None: #if code1 did not exist in the dictionary keys
                continue

            for j in range(indx + 1, len(sa2_list_sorted)):
                name2, code2 = sa2_list_sorted[j]
                li_st_pop2 = sa2_pop_dict.get(code2)#li_st_pop2 will get value None of code2 is not found
                if li_st_pop2 is None:
                    continue

                similarity = cosine_similarity(li_st_pop1, li_st_pop2)# calling function to calculate cosine similarity
                if similarity > max_similarity:
                    max_similarity = similarity
                    best_pair = (name1, name2)
                elif similarity == max_similarity: #in case of two different pairs with same similarity, tiebreaker
                    if (code1, code2) < (best_pair[0], best_pair[1]):
                        best_pair = (name1, name2)

        if best_pair:
            op3[sa3_name] = [best_pair[0], best_pair[1], round(max_similarity, 4)] #finally rounding off the value to 4 decimal places

    return op3
           
def main(csvfile_1, csvfile_2):
    
    header1,items1,header2,items2 = openfile(csvfile_1, csvfile_2)
    if header1 == None :
        return {},{},{}
    #here items1 and items2 is a list of rows from file1 and file2 respectively
    items1,items2,index_area,index_pop,age_grp_index = sort_header(header1,items1,header2,items2)
    
    if items1 == [] or items2 == []: #incase an error occured
        return {},{},{}
    items1,items2 = remove_inv_rows(items1,items2,index_area,index_pop,age_grp_index)#haandling invalid data before calculations
    
    #calculations
    op1 = output_1(items1,items2,index_area,index_pop,age_grp_index)#call statement for output1
    op2 = output_2(items1,items2,index_area,index_pop,age_grp_index)#call statement for output2
    op3 = output_3(items1,items2,index_area,index_pop,age_grp_index)#call statement for output3
    
    return op1,op2,op3

'''
Debugging Documentation:

Issue 1(Date May 18,2025):

- Error Description:
    RuntimeError: dictionary changed size during iteration
- Erroneous Code Snippet:
    for ag in age_grp_index:    #line148
        for i in ag:
                if i in '()*^%$#@!~`=_+][{}|/".,<>?:;':
                    del age_grp_index[ag]
- Test Case:
    op1,op2,op3 = main('SampleData_Areas_P2.csv','SampleData_Populations_P2.csv')
- Reflection:
    I realised, iterating over a dictionary and removing the keys in the same dictionary within the loop leads
    to skipping over some keys during iteration. In order to fix the issue i used a copy of the dictionary in the for loop
    statement instead. I learned to never modify a dictionary while directly iterating over it.

Issue 2(Date May 18,2025):

- Error Description:
    Recieved wrong standard Deviation in output2
    #output2:
    {'4': {'40304': ['403041072', 16431, 456.1596]}, '5': {'50403': ['504031057', 24301, 1230.8762],
    '50501': ['505011072', 16908, 567.8302], '50502': ['505021089', 24126, 638.4175], '50503': ['505031099', 25259, 945.1807]},
    '6': {}}    
- Erroneous Code Snippet:
    var_iance = sum((x - avg) ** 2 for x in pops) / len(pops) #line 394   
- Test Case:
    op1,op2,op3 = main('SampleData_Areas_P2.csv','SampleData_Populations_P2.csv')   
- Reflection:
    I realised I calculated population standard deviation instead of sample standard deviation. Hence to fix the logical error, I changed
    the denominator to (len(pops) - 1) to match sample standard deviation. Therefore understood the difference between sample and population
    standard deviation.
    
Issue 3(Date May 18,2025):

- Error Description:
    TypeError: unsupported operand type(s) for +: 'int' and 'str'   
- Erroneous Code Snippet:
    avg = sum(pops) / len(pops)  #line 393 
- Test Case:
    op1,op2,op3 = main('SampleData_Areas_P2.csv','SampleData_Populations_P2.csv')
    #pops was a list of numbers in string format    
- Reflection:       
    I realised the elements of the list pops was in string format as read from the file. I resolved
    the error by using int() on the elements before appending them to the list pops before calculation.
    I Learned that I need to be cautious about datatype when executing arthemetic calculation.

'''
print(main('SampleData_Areas_P2.csv','SampleData_Populations_P2.csv'))
