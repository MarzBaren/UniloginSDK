from unilogin import MINUDDANNELSE_LOGIN_URL, login

def get_minuddannelse_name(ses):

    previous_request = ses.get('https://www.minuddannelse.net/Home/AuthenticationPostAuthenticate')

    instituation_id = previous_request.text.split('name="instId" value="')[1].split('"')[0]
    person_type = previous_request.text.split('name="personType" value="')[1].split('"')[0]
    r = ses.post('https://www.minuddannelse.net//Home/AuthenticationPostAuthenticate', data={'instId': instituation_id, 'personType': person_type})
    
    return r.text.split('fornavn":"')[1].split('"')[0]

username = "<username>" #fx. mikk3716
password = "<password>"

ses, latest_request = login(username, password, MINUDDANNELSE_LOGIN_URL)
print( get_minuddannelse_name(ses) )

