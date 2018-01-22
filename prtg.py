from PRTG_Class import PRTG

username = 'jmarter'
password = 'PASSWORD'
id = '5133'
message = "'API testing will resume monitoring shortly'"
base_url = 'https://192.168.239.60/'
test_params = {'username': username,'password': password,'id': id,  'pausemsg': message}
site = PRTG(base_url,**test_params)

print(site.get_ids())
print(help(site))


# import requests
#
# def modifyURL(base_url, uri):
#     base_url += '{}'
#     request = base_url.format(uri)
#
#     return request
#
#
# username = 'jmarter'
# password = 'PASSWORD'
# id = '23060'
# message = "'API testing will resume monitoring shortly'"
#
# base_url = 'http://prtg.wernerds.net/'
# login_uri = 'table.xml?content=sensors&columns=sensor&'
# pause_uri = 'api/pause.htm?'
# all_sensors_uri = 'api/table.xml?'
#
#
# #login_params = {'username': username,'password': password}
# #pause_params = {'id': id, 'pausemsg': message, 'action': '0'}
#
# #switch 'action' to '1' to resume. The 'pausemsg' will need to be removed
# test_params = {'username': username,'password': password,'id': id,  'pausemsg': message,'action': '1'}
#
#
#
#
# r2 = requests.post(modifyURL(base_url, pause_uri),params=test_params)
# #
#
# print(r2.status_code, r2.reason)
# #
# r3 = requests.get('http://prtg.wernerds.net//api/table.xml?content=sensors&columns=objid,group,device,sensor,status,message,lastvalue,priority,favorite')
# print(r3.status_code, r3.reason, r3.text)
#

