import requests

from xml.dom import minidom
from xml.dom.minidom import parse
from xml.etree import ElementTree

class PRTG(object):

    def __init__(self, url, **kwargs):
        payload = kwargs
        self.url = url
        self.sensortree = 'api/table.xml?content=sensortree'
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

    def get_id(self):
        """
        GET request to filter XML response and return ID : DEVCE NAME in a dictionary
        :return:
        """

        url = self.combine_url(self.sensortree)
        print(url)
        r = requests.get(url, params={'username': self.username,'password': self.password}, verify=False, stream=True)
        r.raw.decode_content = True
        print(r)
        events = ElementTree.iterparse(r.raw)
        name_output = []
        id_output = []
        output_dict = {}
        for event, elem in events:
            elem_str = str(elem)
            elem_name = name_output.append(elem.text) if 'name' in elem_str else False
            elem_id = id_output.append(elem.text) if 'id' in elem_str else False

        id_name_dict = zip(id_output, name_output)
        for key, value in id_name_dict:
            if '[Cisco Device]' in value:
                output_dict[key] = value
        return output_dict



    def pause_node(self):
        """
        POST request to pause monitoring for a node
        :return:
        """
        url = self.combine_url(self.pause)
        print('Pausing {}.....'.format(self.id))
        return requests.post(url, params={'username': self.username,'password': self.password,'id': self.id,  'pausemsg': self.pausemsg,'action': '0'}, verify=False)

    def resume_node(self):
        """
        POST request to resume monitoring for a node
        :return:
        """
        url = self.combine_url(self.pause)
        print('Resuming {}.....'.format(self.id))
        return requests.post(url, params={'username': self.username,'password': self.password,'id': self.id, 'action': '1'}, verify=False)
        #return request

    def delete_node(self):
        """
        DELETE request to remove a node
        :return:
        """
        url = self.combine_url(self.delete)
        print('Deleting {}.....'.format(self.id))
        return requests.delete(url, params={'username': self.username,'password': self.password,'id': self.id, 'approve': '1'}, verify=False)
