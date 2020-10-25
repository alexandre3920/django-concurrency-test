import datetime
import requests
import re
import random
import string

PASSWORD_ALPHABET = string.printable


# define a base url
BASE_URL = 'http://localhost:8000'
ADMIN_URL = BASE_URL + '/admin'
LOGIN_URL = ADMIN_URL + '/login/'
CREATE_USER_URL = ADMIN_URL + '/main/dashboarduser/add/'
ADMIN_CREDENTIALS_USERNAME = 'admin@localhost'
ADMIN_CREDENTIALS_PASSWORD = 'admin'


def main():
    print("[", datetime.datetime.now(), "] Start requests")

    # Get cookies (with sessionid) by accessing the BASE_URL
    url = LOGIN_URL
    print("[", datetime.datetime.now(), "] GET : ", url)
    res = requests.get(url)
    print("[", datetime.datetime.now(), "] -> status code : ", res.status_code)
    html = res.text.encode('utf-8')
    # Get cookies
    cookies = res.cookies
    # Get CSRF token
    pattern = b'name="csrfmiddlewaretoken" value="(\w+)"'
    matches = re.findall(pattern, html)
    token = matches[0]
    print("[", datetime.datetime.now(), "] -> csrf token : ", token)

    # I need first to authenticate by login
    # with a superuser account on the Django Admin
    login_data = {
        'csrfmiddlewaretoken': token,
        'username': ADMIN_CREDENTIALS_USERNAME,
        'password': ADMIN_CREDENTIALS_PASSWORD,
    }

    headers = {
        'referer': BASE_URL,
    }
    print("[", datetime.datetime.now(), "] GET : ", url)
    res = requests.post(url, data=login_data, cookies=cookies, headers=headers)
    print("[", datetime.datetime.now(), "] -> status code : ", res.status_code)

    # Get cookies
    cookies = res.cookies

    # First I need to GET the url in order to get the csrf token
    url = CREATE_USER_URL
    print("[", datetime.datetime.now(), "] GET : ", url)
    res = requests.get(url, cookies=cookies)
    print("[", datetime.datetime.now(), "] -> status code : ", res.status_code)
    html = res.text.encode('utf-8')
    # Get the csrf token from the page html
    pattern = b'name="csrfmiddlewaretoken" value="(\w+)"'
    matches = re.findall(pattern, html)
    csrf_token = matches[0]
    print("[", datetime.datetime.now(), "] -> csrf token : ", csrf_token)
    # Get cookies
    cookies = res.cookies

    # Then when I get the csrf token, I can POST to the url
    # Generate random first name, last name, age and password
    random_first_name = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[random.randint(0, 25)]
    random_last_name = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[random.randint(0, 25)] + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[random.randint(0, 25)]
    random_age = str(random.randint(18, 70))
    random_password = "".join(PASSWORD_ALPHABET[random.randint(0, len(PASSWORD_ALPHABET) - 1)] for i in range(0, 10))
    print("[", datetime.datetime.now(), "] patient id : ", random_first_name + random_last_name + random_age)

    # Build the payload with required field
    payload = {
        'csrfmiddlewaretoken': csrf_token,
        'first_name': random_first_name,
        'last_name': random_last_name,
        'email': 'concurrency@djangotest.com',
        'password': random_password,
    }
    headers = {
        "referer": BASE_URL,
    }
    print("[", datetime.datetime.now(), "] POST : ", url)
    print("[", datetime.datetime.now(), "] -> paylod : ", payload)
    print("[", datetime.datetime.now(), "] -> headers : ", headers)
    print("[", datetime.datetime.now(), "] -> cookies : ", cookies)
    res = requests.post(url, cookies=cookies, data=payload, headers=headers)
    print("[", datetime.datetime.now(), "] -> status code : ", res.status_code)


if __name__ == "__main__":
    main()
