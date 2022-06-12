import requests
import pprint
import time
from datetime import datetime

key = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InJmbG9yZXMiLCJjb21wYW55IjoieCIsImlhdCI6MTY0Njc5NzIzNn0.0aaN9QuYphotnY7tXMbMNnAVj3wgtxyQTVWBhDpcYEw'

def send_study(study):
    print(study)
    linked_comp = list(study["linkedCompanies"])
    #missing linkedCompanies/
    stud = {
            "public":study["public"],
            "study_name": study['studyName'],
            "description":study['description'],
            "document":study['document'],
            "groups":study['groups'],
            "linked_companies":linked_comp
        }
    # printer = pprint
    # printer.pprint(study['substudies'])
    # print()
    substudy = study['substudies']
    # print(substudy["1"])
    study_id = requests.post("http://127.0.0.1:6767/v1/studies/register", headers={'Authorization': key},json=stud)
    for sub in substudy:
        #not using interactions, description, 'totalThemes', 'type', 'totalQuestions', 'themeState'
        substud = {
            "study_id":study_id.json()['study_id'],
            "substudy_name":substudy[str(sub)]['name'],
            "questions":substudy[str(sub)]['questions'],
            "imagesURL":substudy[str(sub)]['keyThemeQuotes'],
            "key_themes":substudy[str(sub)]['keyThemes'],
            "key_theme_quotes":substudy[str(sub)]['keyThemeQuotes'],
            "key_tags":"",
            "noise_text":substudy[str(sub)]['noiseText']
        }
        requests.post("http://127.0.0.1:6767/v1/studies/register/sub", headers={'Authorization': key},json=substud)

def send_company(company):
    # not using notes GUID
    comp = {
            "name":company["companyName"],
            "industry": company['industry'],
            "role":company['role'],
            "url":company['url'],
            "logo_url":company['url'],
            "street_address":company['streetAddress'],
            "city":company['city'],
            "state_province":company['stateProvince'],
            "country":company['country'],
            "region":company['region'],
            "phone":company['phone'],
            "icon":company['phone'],
            "description":company['simpleDesc'],
            "cik":company['cik'],
            "stock_symbol":company['stockSymbol'],
            "recent10k_url":company['Recent10kURL'],
            "recent10q_url":company['Recent10qURL'],
            "zip_postal":company['zipPostal'],
            "latitude":company['longitude'],
            "longitude":company['latitude']
        }
    x = requests.post("http://127.0.0.1:6767/v1/companies/register", headers={'Authorization': key},json=comp)
     
    
def send_interaction(interaction):
    # not using time/date (wrong format) state
    time_translated = datetime.now().isoformat()
    interaction_type = 0
    if interaction['interactionType'] == "Interview":
        interaction_type = 1
    interaction_status = 0
    if interaction['status'] == "Scheduled":
        interaction_status = 1
    if interaction['status'] == "Canceled":
        interaction_status = 2
    if interaction['status'] == "Completed":
        interaction_status = 3
    if interaction['status'] == "Planned":
        interaction_status = 4
    interact = {
        "creator_id":1,
        "owner_id": 1,
        "name":interaction['interactionName'],
        "description":interaction['simpleDesc'],
        "creation_date":time_translated,
        "modification_date":time_translated,
        "date_time":time_translated,
        "public":interaction['public'],
        "groups":"N/A",
        "latitude":0,
        "longitude":0,
        "contact_name":interaction['contactName'],
        "contact_email":interaction['contactEmail'],
        "contact_linkedin":interaction['contactLinkedIn'],
        "contact_twitter":interaction['contactTwitter'],
        "url":interaction['url'],
        "city":"N/A",
        "street_address":"N/A",
        "zip_postal":"N/A",
        "state_province":"N/A",
        "country":"N/A",
        "region":"N/A",
        "phone":"N/A",
        "interaction_type":interaction_type,
        "status":interaction_status,
        "abstract":interaction['abstract'],
        "thumbnail":interaction['thumbnail']
    }
    x = requests.post("http://127.0.0.1:6767/v1/interactions/register", headers={'Authorization': key},json=interact)
