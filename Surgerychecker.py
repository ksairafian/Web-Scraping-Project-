import smtplib
import ssl
import bs4
import requests
import lxml

# Scrapes the APDS website for the latest job posting
def getsurgdate(url):
    # APDS website TLS certificate is not acquirable automatically - must link to certificate in a txt file
    res = requests.get(url, verify='/Users/kgs44/PycharmProjects/tkinterpractice/certificate.txt')
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'lxml')
    elems = soup.select('#filter-list > div:nth-child(1) > a')
    return elems[0].text.strip()

# Scrapes non-APDS websites for latest job posting date
def getdate(url, path):
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'lxml')
    elems = soup.select(path)
    return elems[0].text.strip()


surg_text = getsurgdate('https://apds.org/education-careers/open-positions/')
rads_text = getdate('https://www.apdr.org/trainees/residency-information/residency-positions-available', '#content > div > div > div.col > div:nth-child(4) > div > div > div > p:nth-child(4)')
psych_text = getdate('https://www.psychiatry.org/residents-medical-students/residents/vacant-resident-positions', '#ctl01_fwTxtPatients_ctl00 > ul > li:nth-child(1) > div > h3:nth-child(1) > strong')
peds_text = getdate('https://www.appd.org/careers-opportunities/job-board/?fwp_job_categor=residents', '#fl-post-461 > div > div > div.fl-row.fl-row-full-width.fl-row-bg-none.fl-node-5db9d9af37354 > div > div > div > div.fl-col.fl-node-5db9d9af385ff > div > div.fl-module.fl-module-post-grid.fl-node-5db9d9bfaebec.job-feed-grid.facetwp-template.facetwp-bb-module > div > div.fl-post-grid.fl-paged-scroll-to > div:nth-child(1) > div > div.fl-post-text > div.fl-post-meta.job-details > h5:nth-child(1)')

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "<Sender Email>"
receiver_email = "<Receiving Email>"
password = "<Sender Email Password>"
message = f"""\
Subject: Latest Job Postings


Latest APDS Post: {surg_text} \n
Latest APDR Post: {rads_text} \n
Latest APA Post: {psych_text} \n
Latest APPD Post: {peds_text} 
"""

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)



