from bs4 import BeautifulSoup
import requests
import re

SEARCh_URL = "https://www.europarl.europa.eu/meps/en/search/advanced?countryCode={}"
COUNTRY = "PT"

country_url = SEARCh_URL.format(COUNTRY)


def remove_cute_anti_bot(email):
    """
        Europa site reverses emails and adds [dot] and [at] to throw off bots 
    """
    return email.replace("[dot]", ".").replace("[at]", "@")[::-1]



def get_members_url():
    """
        Gets all members pages urls in the main page
    """
    r = requests.get(country_url)

    soup = BeautifulSoup(r.content, "html.parser")
    members = soup.findAll("div", {"id" : re.compile(r'member\-block\-\d{4,8}')})

    return [m.a.get("href") for m in members]


def get_member_email(contents):
    """
        Gets email from member page content
    """
    soup = BeautifulSoup(contents, "html.parser")

    email_tag = soup.findAll("a", {"class": re.compile(r"link_email.*")})

    if email_tag:
        email = email_tag[0].get("href").split(":")[1]
        
        email = remove_cute_anti_bot(email)
        return email
    else:
        return None



def fetch_emails():
    """
        Fetches all emails
    """

    for member_url in get_members_url():
        r = requests.get(member_url)

        yield get_member_email(r.content)



if __name__ == "__main__":
    for email in fetch_emails():
        print(email)