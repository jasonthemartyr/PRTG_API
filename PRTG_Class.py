import requests

class PRTG(object):

    def __init__(self, url, **kwargs):
        self.url = url
        self.pause ='api/pause.htm?'
        payload = kwargs

        for i in payload:
            self.username = payload.get('username') if 'username' in payload else False
            self.password = payload.get('password') if 'password' in payload else False
            self.id = payload.get('id') if 'id' in payload else False
            self.pausemsg = payload.get('pausemsg') if 'pausemsg' in payload else False

    def modifyURL(self, uri):
        """
        Modifies base URL with URI
        :param uri:
        :return:
        """
        urls = self.url + '{}'
        request = urls.format(uri)
        return request

    def pause_node(self):
        """
        Pauses node
        :return:
        """
        url = self.modifyURL(self.pause)
        print(url)
        request = requests.post(url, params={'username': self.username,'password': self.password,'id': self.id,  'pausemsg': self.pausemsg,'action': '0'}, verify=False)
        return request

    def resume_node(self):
        """
        Resumes node
        :return:
        """
        url = self.modifyURL(self.pause)
        request =requests.post(url, params={'username': self.username,'password': self.password,'id': self.id, 'action': '1'}, verify=False)
        return request



username = 'jmarter'
password = 'November19!'
id = '5133'
message = "'API testing will resume monitoring shortly'"
base_url = 'https://192.168.239.60/'
test_params = {'username': username,'password': password,'id': id,  'pausemsg': message}
site = PRTG(base_url,**test_params)
print(site.resume_node())