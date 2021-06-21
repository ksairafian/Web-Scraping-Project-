import smtplib
import ssl
import bs4
import requests
import schedule
import time

# Scrapes the APDS website for the latest job posting
def getsurgdate(url):
    # APDS website TLS certificate is not acquirable automatically - must link to certificate in a txt file
    res = requests.get(url, verify='/Users/kgs44/PycharmProjects/tkinterpractice/certificate.txt')
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    elems = soup.select('#filter-list > div:nth-child(1) > a')
    return elems[0].text.split()

# Scrapes the APDR website for latest radiology job posting date
def getradsdate(url):
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    elems = soup.select('#content > div > div > div.col > div:nth-child(4) > div > div > div > p:nth-child(3) > strong')
    return elems[0].text.split()

surg_text = getsurgdate('https://apds.org/education-careers/open-positions/')
rads_text = getradsdate('https://www.apdr.org/trainees/residency-information/residency-positions-available')

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "<desired email address to send emails>"
receiver_email = "<email address to receive emails>"
password = "<password for sender email>"
message = f"""\
Subject: Latest Job Postings


Latest APDS Post: {surg_text} \n
Latest APDR post: {rads_text}
"""

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)

