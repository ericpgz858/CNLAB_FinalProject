import pandas as pd
import os


def Check_file(Filename):
    if not os.path.exists(Filename):
        return 'File not found'
    if not Filename.endswith('.csv'):
        return 'File is not csv'
    df = pd.read_csv(Filename, nrows=0)
    if 'Student ID' not in df:
        return 'There is no Student ID attribute'
    return 'Pass'

def One_Student_Sign(Filename, Student_ID, Day):
    err = Check_file(Filename)
    if err != 'Pass':
        return err
    
    df = pd.read_csv(Filename)
    if not any(df['Student ID'] == Student_ID):
        return 'Student not in this Course'
    if Day not in df:
        df[Day] = 0

    if df.loc[df['Student ID'] == Student_ID, Day].values == 1:
        return 'Had Signed'
    df.loc[df['Student ID'] == Student_ID, Day] = 1
    df.to_csv(Filename, sep=',', encoding='utf-8', index=False)
    return 'Success'

def One_Student_Unsign(Filename, Student_ID, Day):
    err = Check_file(Filename)
    if err != 'Pass':
        return err
    
    df = pd.read_csv(Filename)
    if not any(df['Student ID'] == Student_ID):
        return 'Student not in this Course'
    if Day not in df:
        df[Day] = 0

    if df.loc[df['Student ID'] == Student_ID, Day].values == 0:
        return 'Has Not Signed'
    df.loc[df['Student ID'] == Student_ID, Day] = 0
    df.to_csv(Filename, sep=',', encoding='utf-8', index=False)
    return 'Success'
    

def All_students(Filename):
    err = Check_file(Filename)
    if err != 'Pass':
        return err
    
    df = pd.read_csv(Filename)
    ID_list = list(df['Student ID'])
    return ID_list

def Add_A_Day(Filename, Day):
    err = Check_file(Filename)
    if err != 'Pass':
        return err
    
    df = pd.read_csv(Filename)
    if Day in df:
        return 'Success'
    df[Day] = 0
    df.to_csv(Filename, sep=',', encoding='utf-8', index=False)
    return 'Success'

def Delete_a_Day(Filename, Day):
    err = Check_file(Filename)
    if err != 'Pass':
        return err
    
    df = pd.read_csv(Filename)
    if Day not in df:
        return 'Success'
    df = df.drop(Day, axis=1)
    df.to_csv(Filename, sep=',', encoding='utf-8', index=False)
    return 'Success'

def Search_one_Student(Filename, Student_ID):
    err = Check_file(Filename)
    if err != 'Pass':
        return err
    
    df = pd.read_csv(Filename)
    isInFile = (df['Student ID'] == Student_ID)
    if not any(isInFile):
        return 'Student not in this course'
    Student_out = df[isInFile].to_dict('list')
    D = [[], []]
    for key in Student_out:
        if key not in ['Student ID', 'Name', 'Unnamed: 0']:
            D[0].append(key)
            D[1].append(Student_out[key][0])
    return D

def Create_File(Filename, Student_ID_list, Student_Name_list, Day_list=[]):
    if os.path.exists(Filename):
        return 'File exists'
    if not Filename.endswith('.csv'):
        return 'File is not csv'

    if len(Student_ID_list) != len(set(Student_ID_list)):
        return 'There are duplicate ID in ID list'
    if len(Student_ID_list) != len(Student_Name_list):
        return 'ID list and Name list not match'
    
    D = {'Student ID': Student_ID_list, 'Name': Student_Name_list}
    df = pd.DataFrame(D)
    for Day in set(Day_list):
        df[Day] = 0
    df.to_csv(Filename, sep=',', encoding='utf-8', index=False)
    return 'Success'

def Add_one_Student(Filename, Student_ID, Student_Name):
    err = Check_file(Filename)
    if err != 'Pass':
        return err
    
    df = pd.read_csv(Filename)
    if any(df['Student ID'] == Student_ID):
        return 'Student ID exists'
    D = {'Student ID':[Student_ID], 'Name':[Student_Name]}
    new_df = pd.DataFrame(D)
    for Day in df.columns.values[2:]:
        new_df[Day] = 0
    new_df.to_csv(Filename, sep=',', encoding='utf-8', index=False, mode='a', header=False)
    return 'Success'

def Delete_one_Student(Filename, Student_ID):
    err = Check_file(Filename)
    if err != 'Pass':
        return err
    
    df = pd.read_csv(Filename)
    if not any(df['Student ID'] == Student_ID):
        return 'Student ID not exists'
    df = df.drop(df[df['Student ID'] == Student_ID].index, axis=0)
    df.to_csv(Filename, sep=',', encoding='utf-8', index=False)
    return 'Success'

def Attend_Student(Filename, Day):
    err = Check_file(Filename)
    if err != 'Pass':
        return err
    
    df = pd.read_csv(Filename)
    if  Day not in df:
        return 'No this day'
    return df.loc[df.loc[:, Day].values == 1, 'Student ID'].values.tolist()

def No_Attend_Student(Filename, Day):
    err = Check_file(Filename)
    err = Check_file(Filename)
    if err != 'Pass':
        return err
    
    df = pd.read_csv(Filename)
    if  Day not in df:
        return 'No this day'
    return df.loc[df.loc[:, Day].values == 0, 'Student ID'].values.tolist()

# TODO:Return Attend student(a day)(O)
#      Add a student(O)
#      Add a Student with Data(O)
#      Add a Day(O)
#      Delete a Student(O)
#      Delete a day(O)
#      Search a student(O)
#      If a student attend in day(O)
#      Multiple version

# fname = './test.csv'
# print(Check_file('./test.csv'))
# print(One_Student_Sign(fname, 'B09902117', '5/12'))
# print(One_Student_Sign(fname, 'B09902071', '5/12'))
# print(All_students(fname))
# print(Add_A_Day(fname, '5/20'))
# print(Add_A_Day(fname, '5/21'))
# print(Delete_a_Day(fname, '5/21'))
# print(Delete_a_Day(fname, '5/19'))
# print(Search_one_Student(fname, 'B09902117'))
# print(Create_File('./tet.csv', ['B09902117', 'B09902001', 'B09902000', 'B09902002'], ['Alice', 'Bob', 'Eve', 'Candy'], ['5/12', '5/13', '5/14', '5/15']))
# print(Create_File('./tett.csv', ['B09902117', 'B09902001', 'B09902000', 'B09902002'], ['Alice', 'Bob', 'Eve', 'Candy']))
# print(Add_one_Student(fname, 'B09902045', 'Ted'))
# print(Delete_one_Student(fname, 'B09902001'))
# print(Add_one_Student(fname, 'B09902001', 'Andy'))
# #print(One_Student_Unsign(fname, 'B09902117', '5/12'))
# print(Attend_Student(fname, '5/12'))
# print(No_Attend_Student(fname, '5/12'))
