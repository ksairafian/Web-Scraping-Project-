import smtplib
import ssl
import bs4
import certifi
import requests
import urllib3


def getsurgerydate(url):
    res = requests.get(url, verify='/Users/kgs44/PycharmProjects/tkinterpractice/certificate.txt')
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    elems = soup.select('#filter-list > div:nth-child(1) > a > div.card-block.m-l-auto.text-muted.item-flex.align-items-flex-end > span')
    return elems[0].text.strip()

class Mail:

    def __init__(self):
        self.port = 465
        self.smtp_server_domain_name = "smtp.gmail.com"
        self.sender_mail = "residencyjobcheckerbot@gmail.com"
        self.password = "Looking4Surgery&OtherResidencyPositions"

    def send(self, emails, subject, content):
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
        service.login(self.sender_mail, self.password)

        for email in emails:
            result = service.sendmail(self.sender_mail, email, f"Subject: {subject}\n{content}")

        service.quit()


if __name__ == '__main__':
    mails = input("Enter emails: ").split()
    subject = input("Enter subject: Latest APDS Post")
    text = getsurgerydate('https://apds.org/education-careers/open-positions/')
    content = input("Enter content: " + f'{text}')

    mail = Mail()
    mail.send(mails, subject, content)

