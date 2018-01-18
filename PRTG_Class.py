import requests

class PRTG(object):

    def __init__(self, url, **kwargs):
        payload = kwargs
        self.url = url
        self.pause ='api/pause.htm?'
        self.delete = '/api/deleteobject.htm?'
        self.username = payload.get('username') if 'username' in payload else False
        self.password = payload.get('password') if 'password' in payload else False
        self.id = payload.get('id') if 'id' in payload else False
        self.pausemsg = payload.get('pausemsg') if 'pausemsg' in payload else False

    def combine_url(self, uri):
        """
        Combines base URL with URI
        :param uri:
        :return:
        """
        urls = self.url + '{}'
        request = urls.format(uri)
        return request

    def pause_node(self):
        """
        POST request to pause monitoring for a node
        :return:
        """
        url = self.combine_url(self.pause)
        print(url)
        return requests.post(url, params={'username': self.username,'password': self.password,'id': self.id,  'pausemsg': self.pausemsg,'action': '0'}, verify=False)

    def resume_node(self):
        """
        POST request to resume monitoring for a node
        :return:
        """
        url = self.combine_url(self.pause)
        return requests.post(url, params={'username': self.username,'password': self.password,'id': self.id, 'action': '1'}, verify=False)
        #return request

    def delete_node(self):
        """
        DELETE request to remove a node
        :return:
        """
        url = self.combine_url(self.delete)
        return requests.delete(url, params={'username': self.username,'password': self.password,'id': self.id, 'approve': '1'}, verify=False)
