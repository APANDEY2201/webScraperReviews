from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup as bsoup

#print('First Line')

# Step 1: To get the source code of page.
rev_pages=4
count_final=0
# Define organizational variables
# rev_org_dict={'DeutscheBahn':'deutschebahn','volkswagenconsulting':'volkswagenconsulting','IBM':'ibm-deutschland','Infosys':'infosyslimited','Tata Consultancy Services':'tata-consultancy-services-deutschland','volkswagenconsulting':'volkswagenconsulting'}
# Jaykishan
rev_org_dict={'ICO_LUX':'ico-lux','volkswagenconsulting':'volkswagenconsulting','IBM':'ibm-deutschland','Infosys':'infosyslimited','Tata Consultancy Services':'tata-consultancy-services-deutschland','volkswagenconsulting':'volkswagenconsulting'}
#rev_org_dict={'DeutscheBahn':'deutschebahn'}
#rev_org_dict={'Tata Consultancy Services':'tata-consultancy-services-deutschland','volkswagenconsulting':'volkswagenconsulting'}
rev_org_domain=''
rev_sales=''
rev_no_of_emp=''
rev_kununu_score=''
rev_count_kun=''
rev_recmndtn_prcnt=''
rev_kun_profile_views=''
rev_org_file_dsv='OrgDTLS.csv'
org_file_heading="organization | sales | no of employee | kununu score | total reviews in kununu | recommendation percent | profile views\n"

org_csv=open(rev_org_file_dsv,'w')
org_csv.write(org_file_heading)

rev_filename_csv='kununuRevCsv001.csv'
rev_filename_dsv='kununuRevDsv001.csv'
rev_heading_csv="Organization,Month,Heading,OverallRating,WorkingAtmosphereScore,WorkingAtmosphereComment,ColleagueCohesionScore,ColleagueCohesionComment,EqualRightsScore,EqualRightsComment,DealingWithOlderColleaguesScore,DealingWithOlderColleaguesComment,EnvironmentalSocialAwarenessScore,EnvironmentalSocialAwarenessComment\n"
rev_heading_dsv="Organization|Month|Heading|OverallRating|WorkingAtmosphereScore|WorkingAtmosphereComment|ColleagueCohesionScore|ColleagueCohesionComment|EqualRightsScore|EqualRightsComment|DealingWithOlderColleaguesScore|DealingWithOlderColleaguesComment|EnvironmentalSocialAwarenessScore|EnvironmentalSocialAwarenessComment\n"
f_csv=open(rev_filename_csv, 'w',encoding='utf-8')
f_csv.write(rev_heading_csv)
f_dsv=open(rev_filename_dsv, 'w',encoding='utf-8')
f_dsv.write(rev_heading_dsv)
base_url='https://www.kununu.com/de/'
komment_url='/kommentare/'
#base_url='https://www.kununu.com/de/deutschebahn/kommentare/'
#base_url='https://www.kununu.com/de/infosyslimited/kommentare/'
for org_name, org_url_alias in rev_org_dict.items():
    passFlag = False  # Jaykishan
    print('Fetching Reviews of',org_name,',Please wait...')
    url_org_home=base_url+org_url_alias
    page_org_home=urlopen(url_org_home)
    html_org_home=page_org_home.read()
    page_org_home.close()
    parsed_html_org=bsoup(html_org_home,"html.parser")
#    rev_org_domain=parsed_html_org.find("div",{"class":"company-profile-sub-title"}).a.text # Domain
    key_fig_div=parsed_html_org.find_all("div",{"class":"col-xs-7 col-sm-12 col-md-12 col-lg-12 company-profile-number-data"})
    try:
        rev_sales=key_fig_div[0].text.strip()
    except:
        rev_sales='  '
    try:
        rev_no_of_emp=key_fig_div[1].text.strip()
    except:
        rev_no_of_emp='  '
    kununu_dtls=parsed_html_org.find("div",{"class":"col-sm-5 col-md-7 overview-main"}).div
    try:
        rev_kununu_score=kununu_dtls.div.span.text.strip()
    except:
        rev_kununu_score='  '
    try:
        rev_recmndtn_prcnt=kununu_dtls.find("div",{"class":"col-xs-6 col-sm-6 col-md-3 col-lg-3 relative"}).a.span.text.strip()
    except:
        rev_recmndtn_prcnt='  '
    try:
        rev_kun_profile_views=kununu_dtls.find("div",{"class":"col-md-2 col-lg-2 hidden-sm hidden-xs relative"}).a.span.text.strip()
    except:
        rev_kun_profile_views='  '
    try:
        rev_count_kun=parsed_html_org.find_all("div",{"class":"base-comparison"})[0].text.strip() # Total reviews in kununu
    except:
        rev_count_kun='  '
    org_csv.write(org_name+'|'+rev_sales+'|'+rev_no_of_emp+'|'+rev_kununu_score+'|'+rev_count_kun+'|'+rev_recmndtn_prcnt+'|'+rev_kun_profile_views+'\n')

    for page in range(1, rev_pages):
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
        for indiv_divs in all_divs:
            count_div += 1
            #    print(indiv_divs)
            try:
                rev_mnth = indiv_divs.div.span.time.text  # extracted datetime from the time tag
            except:
                rev_mnth='  '
            #print('rev_mnth:: ', rev_mnth)
            try:
                rev_heading = indiv_divs.div.h3.text.replace('\n', ' ').replace('\r', '') # Jaykishan 2
            except:
                rev_heading='  '
            #print('rev_heading:: ', rev_heading)
            try:
                rev_rating = indiv_divs.find("div", {"class": "index__block__36tsj index__scoreBlock__138n3"}).span.text
            except:
                rev_rating='  '
            #print('rev_rating:: ', rev_rating)
            # Employee details
            try:
                rev_emp_position = indiv_divs.find("span", {"class": "index__position__mCyeO"}).text.replace('\n', ' ').replace('\r', '') # Jaykishan 2
            except:
                rev_emp_position='  '
            #print(rev_emp_position)
            try:
                rev_emp_dept_loc = indiv_divs.find("span", {"class": "index__sentence__3PKUg index__middot__3vlu3"}).text  # Emp department with location
            except:
                rev_emp_dept_loc='  '
            #print(rev_emp_dept_loc)
            try:
                rev_emp_recmndatn = indiv_divs.find("span", {"class": "index__recommendation__jftd3"}).text.replace('\n', ' ').replace('\r', '') # Jaykishan 2
            except:
                rev_emp_recmndatn='  '
            #print('rev_emp_recmndatn :: ', rev_emp_recmndatn)

            # defining all variables
            # Ratings
            rev_wrk_atmos = ''
            rev_work_atmos_score = ''
            rev_wrk_atmos_comment = ''
            rev_coll_coh = ''
            rev_coll_coh_score = ''
            rev_coll_coh_comment = ''
            rev_eq_rights = ''
            rev_eq_rights_score = ''
            rev_eq_rights_comment = ''
            rev_old_coll = ''
            rev_old_coll_score = ''
            rev_old_coll_comment = ''
            rev_soc_awareness = ''
            rev_soc_awareness_score = ''
            rev_soc_awareness_comment = ''

            #    list_diversity=['Arbeitsatmosphäre','Kollegenzusammenhalt','Gleichberechtigung','Umgang mit älteren Kollegen','Umwelt-/Sozialbewusstsein']
            rev_internalAttributes = indiv_divs.find_all("div", {"class": "index__factor__3Z15R"})
            for rev_class in rev_internalAttributes:
                #        print('rev_class', rev_class)
                if (rev_class.h4.text == 'Arbeitsatmosphäre'):
                    try:
                        rev_wrk_atmos = rev_class.h4.text
                    except:
                        rev_wrk_atmos= '  '
                    try:
                        rev_work_atmos_score = rev_class.span["data-score"]
                    except:
                        rev_work_atmos_score='  '
                    try:
                        rev_wrk_atmos_comment = rev_class.p.text.replace('\n', ' ').replace('\r', '') # Jaykishan 2
                    except:
                        rev_wrk_atmos_comment = '  '
                if (rev_class.h4.text == 'Kollegenzusammenhalt'):
                    try:
                        rev_coll_coh = rev_class.h4.text
                    except:
                        rev_coll_coh='  '
                    try:
                        rev_coll_coh_score = rev_class.span["data-score"]
                    except:
                        rev_coll_coh_score='  '
                    try:
                        rev_coll_coh_comment = rev_class.p.text.replace('\n', ' ').replace('\r', '') # Jaykishan 2
                    except:
                        rev_coll_coh_comment = '  '
                if (rev_class.h4.text == 'Gleichberechtigung'):
                    try:
                        rev_eq_rights = rev_class.h4.text
                    except:
                        rev_eq_rights='  '
                    try:
                        rev_eq_rights_score = rev_class.span["data-score"]
                    except:
                        rev_eq_rights_score='  '
                    try:
                        rev_eq_rights_comment = rev_class.p.text.replace('\n', ' ').replace('\r', '') # Jaykishan 2
                    except:
                        rev_eq_rights_comment = '  '
                if (rev_class.h4.text == 'Umgang mit älteren Kollegen'):
                    try:
                        rev_old_coll = rev_class.h4.text
                    except:
                        rev_old_coll='  '
                    try:
                        rev_old_coll_score = rev_class.span["data-score"]
                    except:
                        rev_old_coll_score='  '
                    try:
                        rev_old_coll_comment = rev_class.p.text.replace('\n', ' ').replace('\r', '') # Jaykishan 2
                    except:
                        rev_old_coll_comment = '  '
                if (rev_class.h4.text == 'Umwelt-/Sozialbewusstsein'):
                    try:
                        rev_soc_awareness = rev_class.h4.text
                    except:
                        rev_soc_awareness='  '
                    try:
                        rev_soc_awareness_score = rev_class.span["data-score"]
                    except:
                        rev_soc_awareness_score='  '
                    try:
                        rev_soc_awareness_comment = rev_class.p.text.replace('\n', ' ').replace('\r', '') # Jaykishan 2
                    except:
                        rev_soc_awareness_comment = '  '

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

            f_csv.write(org_name + "," + rev_mnth + "," + rev_heading + "," + rev_rating + "," + rev_work_atmos_score + "," + rev_wrk_atmos_comment + "," + rev_coll_coh_score + "," + rev_coll_coh_comment + "," + rev_eq_rights_score + "," + rev_eq_rights_comment + "," + rev_old_coll_score + "," + rev_old_coll_comment + "," + rev_soc_awareness_score + "," + rev_soc_awareness_comment + "\n")
            f_dsv.write(org_name + "|" + rev_mnth + "|" + rev_heading + "|" + rev_rating + "|" + rev_work_atmos_score + "|" + rev_wrk_atmos_comment + "|" + rev_coll_coh_score + "|" + rev_coll_coh_comment + "|" + rev_eq_rights_score + "|" + rev_eq_rights_comment + "|" + rev_old_coll_score + "|" + rev_old_coll_comment + "|" + rev_soc_awareness_score + "|" + rev_soc_awareness_comment + "\n")
        #       print('\n ***************************************************')

        count_final = count_div + count_final
    #    print('----Loop Ended with ',count_div,' divs---- \n \n')
    if passFlag == True: # Jaykishan
        passFlag = False # Jaykishan
        pass # Jaykishan
    print('Total Reviews Fetched Until Now :: ', count_final,'\n')
