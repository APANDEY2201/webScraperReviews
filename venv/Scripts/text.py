import csv
import sys

companyListFile = '200429_Companies_List_for_Python.csv'
#companyListFile='C:\\Users\\tabis\\PycharmProjects\\webScraperReviews\\venv\\Scripts\\200429_Companies_List_for_Python.csv'
companyName = ''
companyUrl = ''
companyType = ''
rev_org_dict = {}
rev_org_type_dict = {}
with open(companyListFile, encoding='utf-8') as companyDataFile:
    print('File opened')
    data = csv.reader(companyDataFile, delimiter=',')
    #print('After data')
    for row in data:
        companyName = row[1]
        companyUrl = row[3]
        companyType = row[4]
#        print(companyName, companyUrl, companyType)
        rev_org_dict.update({companyName: companyUrl})
        rev_org_type_dict.update({companyName: companyType})

for Org, org_url_alias in rev_org_dict.items():
    print('Fetching Reviews of', Org, ',Please wait...', org_url_alias)
for Org, reg_type in rev_org_type_dict.items():
    print('Fetching Reviews of', Org, ',Please wait...', reg_type)
