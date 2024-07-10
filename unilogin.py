import requests
from html import unescape


AULA_LOGIN_URL = 'https://www.aula.dk/auth/login.php?type=unilogin'
MINUDDANNELSE_LOGIN_URL = 'https://www.minuddannelse.net/KmdIdentity/Login?domainHint=unilogin-idp-prod&toFa=False'


def login(username, password, login_url):
    ses = requests.session()
    ses.allow_redirects = True

    original_form_url = extract_form_url(ses.get(login_url).text)

    chosen_login_type = ses.post(original_form_url, data={'selectedIdp':'uni_idp'}).text
    username_form_url = extract_form_url(chosen_login_type)

    username_login = ses.post(username_form_url, data={'username': username}).text
    password_form_url = extract_form_url(username_login)

    previous_request = ses.post(password_form_url, data={'username': '', 'password': password})


    while True:
        payload = extract_saml_and_relay(previous_request.text)
        url = extract_form_url(previous_request.text)

        if not "unilogin.dk" in url and not "kmd.dk" in url and payload == {}:
            break

        previous_request = ses.post(url, data=payload)

    return ses, previous_request


def extract_form_url(text):
    try:
        return unescape(
            text.split('<form')[1]\
                .split('action="')[1]\
                .split('"')[0]
            )
    except:
        return ""

def extract_saml_and_relay(text):
    try:
        return {
            'SAMLResponse': text.split('name="SAMLResponse" value="')[1]\
                                .split('"')[0],
            'RelayState': text.split('name="RelayState" value="')[1]\
                                .split('"')[0]
        }
    except:
        return {}

