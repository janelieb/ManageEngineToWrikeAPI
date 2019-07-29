import os
import pandas
import pyodbc
import requests
import io

#print('hello world')
fileName = 'new_test_file.txt'
f = open(fileName, 'a+')
#program variables
task_numeric = '1234'
time_hrs_str = 'get time in hours as a string from manage engine query'
dateYesterday = 'yyyy-mm-dd'
time_log_comment = 'logged from task id'
#connection string. can change server / database
conn_str = (
    r'Driver={SQL Server};'
    r'Server=mau-sql01;'
    r'Database=ServiceDesk;'
    r'Trusted_Connection=yes;'
    )
#Nateisha token
token_file = open("Token.txt")
token = token_file.read()

f = open(fileName, 'a+')
QueryFile = open('Query.txt', encoding='utf-8')
Query = QueryFile.read()
cnxn = pyodbc.connect(conn_str)
data = pandas.read_sql(Query,cnxn)
DataToShow = data.filter(items=['Worked_On_Date','TimeMins','TimeSpent_Formatted','Title','FIRST_NAME','WrikeID','ItemID'])
#need to put together hyperlinks from this data
DataToShow = data.filter(items=['Worked_On_Date','TimeMins','TimeSpent_Formatted','Title','FIRST_NAME','WrikeID','ItemID'])

for index, row in DataToShow.iterrows():
    #numeric task id from manage engine
    task_numeric = row['WrikeID']
    time_hrs_str = 'get time in hours as a string from manage engine query'
    dateYesterday = 'yyyy-mm-dd'
    time_log_comment = 'logged from task id'
    #url to get task id from wrike given numeric id
    url_get = 'https://www.wrike.com/api/v4/tasks?'
    permalink = '=https://www.wrike.com/open.htm?id='+task_numeric
    # defining a params dict for the parameters to be sent to the API 
    PARAMS = {'permalink':permalink} 
    # sending get request and saving the response as response object 
    r = requests.get(url = url_get, headers = {'Authorization':'Bearer ' +token}, params = PARAMS)
    f.write('\nsent get to api')
    # extracting data in json format 
    dataget = r.json() 
    #parse json response
    task_str = str(dataget['data'][0]['id'])
    #put together time in hours, date yesterday and time log comment
    time_hrs_str = round(float(row['TimeMins']/60),2)
    time_hrs_str = str(time_hrs_str)
    dateYesterday = str(row['Worked_On_Date'])
    time_log_comment = 'ManageEngineTask' + str(row['ItemID'])
    #put together post command url
    url_str = 'https://www.wrike.com/api/v4/tasks/'+task_str+'/timelogs?hours='+ time_hrs_str + '&trackedDate=' + dateYesterday + '&comment='+ time_log_comment 
    r = requests.post(url = url_str, headers = {'Authorization':'Bearer '+token}) 
    f.write('\nsent post to api')

f.close()
QueryFile.close()
token_file.close()
cnxn.close()
