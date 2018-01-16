import requests

def modifyURL(base_url, uri):
    base_url += '{}'
    request = base_url.format(uri)

    return request


username = 'jmarter'
password = 'PASSWORD'
id = 'SITE ID'
message = "'API testing will resume monitoring shortly'"

base_url = 'URL'
login_uri = 'table.xml?content=sensors&columns=sensor&'

pause_uri = 'api/pause.htm?'

# login_params = {'username': username,'password': password}
# pause_params = {'id': id, 'pausemsg': message, 'action': '0'}

#switch 'action' to '1' to resume. The 'pausemsg' will need to be removed
test_params = {'username': username,'password': password,'id': id, 'pausemsg': message, 'action': '0'}


r2 = requests.put(modifyURL(base_url, pause_uri),params=test_params)

print(r2.status_code, r2.reason)



