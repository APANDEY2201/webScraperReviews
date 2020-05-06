from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup as bsoup
import time
import csv
import re

def germanMonthsToEnglish(gMonth):
    if gMonth.lower() == 'januar':
        return 'January'
    if gMonth.lower() == 'februar':
        return 'February'
    if gMonth.lower() == 'märz':
        return 'March'
    if gMonth.lower() == 'april':
        return 'April'
    if gMonth.lower() == 'mai':
        return 'May'
    if gMonth.lower() == 'juni':
        return 'June'
    if gMonth.lower() == 'juli':
        return 'July'
    if gMonth.lower() == 'august':
        return 'August'
    if gMonth.lower() == 'september':
        return 'September'
    if gMonth.lower() == 'oktober':
        return 'October'
    if gMonth.lower() == 'november':
        return 'November'
    if gMonth.lower() == 'dezember':
        return 'December'

def orgSector(org):
    if org.lower() == 'adidas ag':
        return 'Handel'
    if org.lower() == 'allianz se':
        return 'Finanz'
    if org.lower() == 'basf se':
        return 'Chemie'
    if org.lower() == 'bayerische motoren werke ag':
        return 'Automobil'
    if org.lower() == 'beiersdorf aktiengesellschaft':
        return 'Handel'
    if org.lower() == 'deutsche bank ag':
        return 'Banken'
    if org.lower() == 'deutsche lufthansa ag':
        return 'Transport/Verkehr/Logistik'
    if org.lower() == 'deutsche post ag':
        return 'Transport/Verkehr/Logistik'
    if org.lower() == 'sap se':
        return 'IT'
    if org.lower() == 'wirecard ag':
        return 'Finanz'

# Step 1: To get the source code of page.
rev_pages=500
count_final=0

rev_org_dict={'adidas ag':'adidas','Allianz SE':'allianz-deutschland','BASF SE':'basf-se','Bayerische Motoren Werke AG':'bayerische-motoren-werke','Beiersdorf Aktiengesellschaft':'beiersdorf','Deutsche Bank AG':'deutsche-bank','Deutsche Lufthansa AG':'deutsche-lufthansa','Deutsche Post AG':'deusche-post','SAP SE':'sap','Wirecard AG':'wirecard'}
# rev_org_dict={'SAP SE':'sap','Wirecard AG':'wirecard'}
rev_org_domain=''
OrgSales= ''
OrgNoOfEmployees= ''
OrgKununuScore= ''
OrgTotalKununuReviews= ''
OrgRecomPercent= ''
OrgProfileViews= ''

masterDataFileName = 'Master_Data_Milestone1.csv'
masterDataFile = open(masterDataFileName, "w", newline='',encoding='utf-8')
csv_out = csv.writer(masterDataFile, delimiter = '|')
csv_out.writerows([("Org","OrgSector","RverMonthYear","RverReviewer","RverPosition","RverLoc","RverRecom","RvReviewAbout","RvScore","RvComment")])

orgDataFileName = 'Orgs_Data_Milestone1.csv'
orgDatafile = open(orgDataFileName, "w", newline='',encoding='utf-8')
csv_out = csv.writer(orgDatafile, delimiter = '|')
csv_out.writerows([("Org","OrgSector","OrgSales","OrgNoOfEmployees","OrgKununuScore","OrgTotalKununuReviews","OrgRecomPercent","OrgProfileViews","OrgBenefits")])

base_url='https://www.kununu.com/de/'
komment_url='/kommentare/'
#base_url='https://www.kununu.com/de/deutschebahn/kommentare/'
#base_url='https://www.kununu.com/de/infosyslimited/kommentare/'

for Org, org_url_alias in rev_org_dict.items():
    time.sleep(0.5)
    passFlag = False  # Jaykishan
    print('Fetching Reviews of', Org, ',Please wait...')
    OrgSector = orgSector(Org)
    url_org_home=base_url+org_url_alias
    page_org_home=urlopen(url_org_home)
    html_org_home=page_org_home.read()
    page_org_home.close()
    parsed_html_org=bsoup(html_org_home,"html.parser")
#    rev_org_domain=parsed_html_org.find("div",{"class":"company-profile-sub-title"}).a.text # Domain
    key_fig_div=parsed_html_org.find_all("div",{"class":"col-xs-7 col-sm-12 col-md-12 col-lg-12 company-profile-number-data"})

    try: # OrgSales
        OrgSalesTemp = key_fig_div[0].text.strip().split(' ')
        num = ''
        unit = ''
        currency = ''
        for t in OrgSalesTemp:
            if t[0].isnumeric():
                num = t
            if "mio" in t.lower():
                unit = 'million'
            if "mrd" in t.lower():
                unit = 'billion'
            if "usd" in t.lower():
                currency = 'usd'
            if "eur" in t.lower():
                currency = 'eur'
        newnum = ''
        for t in range(len(num)):
            if num[t] == '.':
                newnum = newnum + ''
            elif num[t] == ',':
                newnum = newnum + '.'
            else:
                newnum = newnum + num[t]
        finalVal = 0
        if unit == 'million':
            finalVal = float(newnum) / 1000
            if currency == 'usd':
                finalVal = finalVal * 0.9
        if unit == 'billion':
            finalVal = float(newnum)
            if currency == 'usd':
                finalVal = finalVal * 0.9
        OrgSales=str(str(finalVal))
    except:
        OrgSales= '  '

    try: # OrgNoOfEmployees
        OrgNoOfEmployeesTemp=key_fig_div[1].text.strip().split(' ')
        num = []
        for t in OrgNoOfEmployeesTemp:
            if t[0].isnumeric():
                num.append(t)
        newnum = []
        for a in num:
            newnumTemp = ''
            for t in range(len(a)):
                if a[t] == '.':
                    newnumTemp = newnumTemp + ''
                elif a[t] == ',':
                    newnumTemp = newnumTemp + '.'
                else:
                    newnumTemp = newnumTemp + a[t]
            newnum.append(newnumTemp)
        finalVal = 0
        for a in newnum:
            finalVal = finalVal + int(a)

        OrgNoOfEmployees=str(finalVal)
    except:
        OrgNoOfEmployees= '  '
    kununu_dtls=parsed_html_org.find("div",{"class":"col-sm-5 col-md-7 overview-main"}).div
    try:
        OrgKununuScore=kununu_dtls.div.span.text.strip().replace('.', '').replace(',', '.')
    except:
        OrgKununuScore= '  '
    try:
        OrgRecomPercent=kununu_dtls.find("div", {"class": "col-xs-6 col-sm-6 col-md-3 col-lg-3 relative"}).a.span.text.strip().replace('%','').replace('.', '').replace(',', '.')
    except:
        OrgRecomPercent= '  '
    try:
        OrgProfileViews=kununu_dtls.find("div", {"class": "col-md-2 col-lg-2 hidden-sm hidden-xs relative"}).a.span.text.strip().replace('.', '').replace(',', '.')
    except:
        OrgProfileViews= '  '
    try:
        OrgTotalKununuReviews=parsed_html_org.find_all("div", {"class": "base-comparison"})[0].text.strip().split(' ')[0].replace('.', '').replace(',', '.') # Total reviews in kununu
    except:
        OrgTotalKununuReviews= '  '
    try:
        OrgBenefits = ''
        regex = re.compile('.*cp-tile company-profile-benefits.*')
        size = len(parsed_html_org.find_all("div", {"class": regex})[0].div.find_all("benefit"))
        for p in range(size):
            OrgBenefits = OrgBenefits + " (" + str(p+1) + ") " + re.sub(' +', ' ',parsed_html_org.find_all("div", {"class": regex})[0].div.find_all("benefit")[p].text.strip())
    except:
        OrgBenefits= '  '

    f_csv_list_org = []
    f_csv_list_org.append((Org, OrgSector, OrgSales, OrgNoOfEmployees, OrgKununuScore, OrgTotalKununuReviews,
                       OrgRecomPercent, OrgProfileViews, OrgBenefits))
    csv_out = csv.writer(orgDatafile, delimiter='|')
    csv_out.writerows(f_csv_list_org)

    for page in range(1, rev_pages):
        time.sleep(0.5)
        target_url = base_url +org_url_alias+komment_url+str(page)
        #    target_url='https://www.kununu.com/de/deutschebahn/kommentare/1'
        #    print('Base url is: '+target_url)
        try:
            page_obj = urlopen(target_url)  # Object of HTTPResponse from the url
        except HTTPError:
            print("404 Page not found") # Jaykishan
            passFlag = True  # Check it later for all # Jaykishan
            break # Jaykishan
        #    print('page_obj:: ',page_obj)
        html_page = page_obj.read()  # Open the HTTPResponse object to get the html source code.
        #    print('html_page:: ',html_page)
        page_obj.close()  # Close the HTTPResponse object

        # Step 2: To get the Review part from kununu page
        parsed_page = bsoup(html_page, "html.parser")  # html_page is parsed in bs4 readable format
        # print('parsed_page:: ', parsed_page)
        # print(parsed_page.article,"\n")
        all_divs = parsed_page.find_all("div", {"class": "index__reviewBlock__27gnB"})  # Got all review frames of different reviewers
        # print('\n \n all divs \n', all_divs)
        count_div = 0
        #    print('----Loop Starts----')
        #    print('\n *************************************************** \n')
        userCounter = 1
        for indiv_divs in all_divs:
            count_div += 1
            #    print(indiv_divs)
            try:
                engMonth = germanMonthsToEnglish(indiv_divs.div.span.time.text.split(' ')[0])
                RverMonthYear = engMonth + " " + indiv_divs.div.span.time.text.split(' ')[1]  # extracted datetime from the time tag
            except:
                RverMonthYear= '  '
            #print('rev_mnth:: ', rev_mnth)
            try:
                RvComment1 = indiv_divs.div.h3.get_text(separator=" ").replace('\n', ' ').replace('\r', ' ') # Jaykishan 2
            except:
                RvComment1= '  '
            #print('rev_heading:: ', rev_heading)
            try:
                RvScore1 = indiv_divs.find("div", {"class": "index__block__36tsj index__scoreBlock__138n3"}).span.text.replace('.', '').replace(',', '.')
            except:
                RvScore1= '  '
            #print('rev_rating:: ', rev_rating)
            # Employee details
            try:
                RverPosition = indiv_divs.find("span", {"class": "index__position__mCyeO"}).text.replace('\n', ' ').replace('\r', ' ') # Jaykishan 2
            except:
                RverPosition= '  '
            #print(rev_emp_position)
            try:
                RverLoc = indiv_divs.find("span", {"class": "index__sentence__3PKUg index__middot__3vlu3"}).text  # Emp department with location
            except:
                RverLoc= '  '
            #print(rev_emp_dept_loc)
            try:
                RverRecom = indiv_divs.find("span", {"class": "index__recommendation__jftd3"}).text.replace('\n', ' ').replace('\r', ' ') # Jaykishan 2
            except:
                RverRecom= '  '




            # try:
            #     RvComment1 = indiv_divs.find_all("div", {"class": "index__factor__3Z15R"}).text.replace('\n', ' ').replace('\r', '') # Jaykishan 2
            # except:
            #     RvComment1= '  '




            #print('rev_emp_recmndatn :: ', rev_emp_recmndatn)

            # defining all variables
            # Ratings
            RvReviewAbout2 = ''
            RvScore2 = ''
            RvComment2 = ''
            RvReviewAbout3 = ''
            RvScore3 = ''
            RvComment3 = ''
            RvReviewAbout4 = ''
            RvScore4 = ''
            RvComment4 = ''
            RvReviewAbout5 = ''
            RvScore5 = ''
            RvComment5 = ''
            RvReviewAbout6 = ''
            RvScore6 = ''
            RvComment6 = ''
            RvReviewAbout10 = ''
            RvScore10 = ''
            RvComment10 = ''

            RvReviewAbout7 = 'Corona1' # Corona 1 # Wofür möchtest du deinen Arbeitgeber im Umgang mit der Corona-Situation loben?
            RvComment7 = ''
            RvReviewAbout8 = 'Corona2' # Corona 2 # Wo siehst du Chancen für deinen Arbeitgeber mit der Corona-Situation besser umzugehen?
            RvComment8 = ''
            RvReviewAbout9 = 'Corona3' # Corona 3 # Wie kann dich dein Arbeitgeber im Umgang mit der Corona-Situation noch besser unterstützen?
            RvComment9 = ''

            #    list_diversity=['Arbeitsatmosphäre','Kollegenzusammenhalt','Gleichberechtigung','Umgang mit älteren Kollegen','Umwelt-/Sozialbewusstsein']
            rev_internalAttributes = indiv_divs.find_all("div", {"class": "index__factor__3Z15R"})
            for rev_class in rev_internalAttributes:
                #        print('rev_class', rev_class)
                if ('Wofür möchtest du deinen Arbeitgeber' in rev_class.h4.text):
                    try:
                        RvComment7 = rev_class.p.get_text(separator=" ").replace('\n', ' ').replace('\r', ' ') # Jaykishan 2
                    except:
                        RvComment7 = '  '
                if ('Wo siehst du Chancen' in rev_class.h4.text):
                    try:
                        RvComment8 = rev_class.p.get_text(separator=" ").replace('\n', ' ').replace('\r', ' ') # Jaykishan 2
                    except:
                        RvComment8 = '  '
                if ('Wie kann dich dein Arbeitgeber' in rev_class.h4.text):
                    try:
                        RvComment9 = rev_class.p.get_text(separator=" ").replace('\n', ' ').replace('\r', ' ') # Jaykishan 2
                    except:
                        RvComment9 = '  '
                if (rev_class.h4.text == 'Arbeitsatmosphäre'):
                    try:
                        RvReviewAbout2 = rev_class.h4.text
                    except:
                        RvReviewAbout2= '  '
                    try:
                        RvScore2 = rev_class.span["data-score"].replace('.', '').replace(',', '.')
                    except:
                        RvScore2= '  '
                    try:
                        RvComment2 = rev_class.p.get_text(separator=" ").replace('\n', ' ').replace('\r', ' ') # Jaykishan 2
                    except:
                        RvComment2 = '  '
                if (rev_class.h4.text == 'Kollegenzusammenhalt'):
                    try:
                        RvReviewAbout3 = rev_class.h4.text
                    except:
                        RvReviewAbout3= '  '
                    try:
                        RvScore3 = rev_class.span["data-score"].replace('.', '').replace(',', '.')
                    except:
                        RvScore3= '  '
                    try:
                        RvComment3 = rev_class.p.get_text(separator=" ").replace('\n', ' ').replace('\r', ' ') # Jaykishan 2
                    except:
                        RvComment3 = '  '
                if (rev_class.h4.text == 'Gleichberechtigung'):
                    try:
                        RvReviewAbout4 = rev_class.h4.text
                    except:
                        RvReviewAbout4= '  '
                    try:
                        RvScore4 = rev_class.span["data-score"].replace('.', '').replace(',', '.')
                    except:
                        RvScore4= '  '
                    try:
                        RvComment4 = rev_class.p.get_text(separator=" ").replace('\n', ' ').replace('\r', ' ') # Jaykishan 2
                    except:
                        RvComment4 = '  '
                if (rev_class.h4.text == 'Umgang mit älteren Kollegen'):
                    try:
                        RvReviewAbout5 = rev_class.h4.text
                    except:
                        RvReviewAbout5= '  '
                    try:
                        RvScore5 = rev_class.span["data-score"].replace('.', '').replace(',', '.')
                    except:
                        RvScore5= '  '
                    try:
                        RvComment5 = rev_class.p.get_text(separator=" ").replace('\n', ' ').replace('\r', ' ') # Jaykishan 2
                    except:
                        RvComment5 = '  '
                if (rev_class.h4.text == 'Umwelt-/Sozialbewusstsein'):
                    try:
                        RvReviewAbout6 = rev_class.h4.text
                    except:
                        RvReviewAbout6= '  '
                    try:
                        RvScore6 = rev_class.span["data-score"].replace('.', '').replace(',', '.')
                    except:
                        RvScore6= '  '
                    try:
                        RvComment6 = rev_class.p.get_text(separator=" ").replace('\n', ' ').replace('\r', ' ') # Jaykishan 2
                    except:
                        RvComment6 = '  '
                if (rev_class.h4.text == 'Work-Life-Balance'):
                    try:
                        RvReviewAbout10 = rev_class.h4.text
                    except:
                        RvReviewAbout10= '  '
                    try:
                        RvScore10 = rev_class.span["data-score"].replace('.', '').replace(',', '.')
                    except:
                        RvScore10= '  '
                    try:
                        # RvComment10= rev_class.p.text.replace('\n', ' ').replace('\r', ' ') # Jaykishan 2
                        RvComment10 = rev_class.p.get_text(separator=" ").replace('\n', ' ').replace('\r', ' ')
                    except:
                        RvComment10 = '  '

            #    print('rev_internalAttributes:: ',rev_internalAttributes)
            #     print('rev_wrk_atmos:: ', rev_wrk_atmos)
            #     print('rev_work_atmos_score:: ', rev_work_atmos_score)
            #     print('rev_wrk_atmos_comment:: ', rev_wrk_atmos_comment)
            #     print('rev_coll_coh:: ', rev_coll_coh)
            #     print('rev_coll_coh_score:: ', rev_coll_coh_score)
            #     print('rev_coll_coh_comment:: ', rev_coll_coh_comment)
            #     print('rev_eq_rights:: ', rev_eq_rights)
            #     print('rev_eq_rights_score:: ', rev_eq_rights_score)
            #     print('rev_eq_rights_comment:: ', rev_eq_rights_comment)
            #     print('rev_old_coll:: ', rev_old_coll)
            #     print('rev_old_coll_score:: ', rev_old_coll_score)
            #     print('rev_old_coll_comment:: ', rev_old_coll_comment)
            #     print('rev_soc_awareness:: ', rev_soc_awareness)
            #     print('rev_soc_awareness_score:: ', rev_soc_awareness_score)
            #     print('rev_soc_awareness_comment:: ', rev_soc_awareness_comment)

            f_csv_list = []
            f_csv_list.append((Org, OrgSector, RverMonthYear, str(userCounter),
                                    RverPosition, RverLoc, RverRecom, "Overall", RvScore1, RvComment1))
            f_csv_list.append((Org, OrgSector, RverMonthYear, str(userCounter),
                                    RverPosition, RverLoc, RverRecom, RvReviewAbout2, RvScore2, RvComment2))
            f_csv_list.append((Org, OrgSector, RverMonthYear, str(userCounter),
                                    RverPosition, RverLoc, RverRecom, RvReviewAbout3, RvScore3, RvComment3))
            f_csv_list.append((Org, OrgSector, RverMonthYear, str(userCounter),
                                    RverPosition, RverLoc, RverRecom, RvReviewAbout4, RvScore4, RvComment4))
            f_csv_list.append((Org, OrgSector, RverMonthYear, str(userCounter),
                                    RverPosition, RverLoc, RverRecom, RvReviewAbout5, RvScore5, RvComment5))
            f_csv_list.append((Org, OrgSector, RverMonthYear, str(userCounter),
                                    RverPosition, RverLoc, RverRecom, RvReviewAbout6, RvScore6, RvComment6))
            f_csv_list.append((Org, OrgSector, RverMonthYear, str(userCounter),
                               RverPosition, RverLoc, RverRecom, RvReviewAbout7, "NA", RvComment7))
            f_csv_list.append((Org, OrgSector, RverMonthYear, str(userCounter),
                               RverPosition, RverLoc, RverRecom, RvReviewAbout8, "NA", RvComment8))
            f_csv_list.append((Org, OrgSector, RverMonthYear, str(userCounter),
                               RverPosition, RverLoc, RverRecom, RvReviewAbout9, "NA", RvComment9))
            f_csv_list.append((Org, OrgSector, RverMonthYear, str(userCounter),
                               RverPosition, RverLoc, RverRecom, RvReviewAbout10, RvScore10, RvComment10))
            userCounter = userCounter + 1
            csv_out = csv.writer(masterDataFile, delimiter='|')
            csv_out.writerows(f_csv_list)

        count_final = count_div + count_final
    #    print('----Loop Ended with ',count_div,' divs---- \n \n')
    if passFlag == True: # Jaykishan
        passFlag = False # Jaykishan
        pass # Jaykishan
    print('Total Reviews Fetched Until Now :: ', count_final,'\n')
