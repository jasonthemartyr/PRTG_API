import requests
from xml.etree import ElementTree

class PRTG(object):

    def __init__(self, url, **kwargs):
        payload = kwargs
        self.url = url
        self.sensortree = 'api/table.xml?content=sensortree'
        self.pause ='api/pause.htm?'
        self.delete = 'api/deleteobject.htm?'
        self.duplicateobject = 'api/duplicateobject.htm?'

        self.username = payload.get('username') if 'username' in payload else False
        self.password = payload.get('password') if 'password' in payload else False
        self.id = payload.get('id') if 'id' in payload else False
        self.pausemsg = payload.get('pausemsg') if 'pausemsg' in payload else False
        self.cloneid = payload.get('clone_id') if 'clone_id' in payload else False
        self.newid = payload.get('new_id') if 'new_id' in payload else False
        self.name = payload.get('name') if 'name' in payload else False


    def combine_url(self, uri):
        """
        Combines base URL with URI
        :param uri:
        :return:
        """
        urls = self.url + '{}'
        request = urls.format(uri)
        return request

    def get_device_ids(self):
        """
        GET request to filter XML response and return ID : DEVICE NAME in a dictionary
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

    #need 'get_group_id' method

    def pause_node(self, node_id):
        """
        POST request ro pause monitoring for a node ID specified by user
        :param node_id:
        :return:
        """
        url = self.combine_url(self.pause)
        print('Pausing {}.....'.format(self.id))
        return requests.post(url, params={'username': self.username,'password': self.password,'id': node_id,  'pausemsg': self.pausemsg,'action': '0'}, verify=False)

    def resume_node(self, node_id):
        """
        POST request to resume monitoring for a node ID specified by user
        :param node_id:
        :return:
        """
        url = self.combine_url(self.pause)
        print('Resuming {}.....'.format(self.id))
        return requests.post(url, params={'username': self.username,'password': self.password,'id': node_id, 'action': '1'}, verify=False)
        #return request

    def delete_node(self, node_id):
        """
        DELETE request to delete node ID specified by user
        :param node_id:
        :return:
        """

        url = self.combine_url(self.delete)
        print('Deleting {}.....'.format(self.id))
        return requests.delete(url, params={'username': self.username,'password': self.password,'id': self.id, 'approve': '1'}, verify=False)


    #last two methods need variable cleanup

    def duplicate_group_or_sensor(self):
        """
        POST request to duplicate a group or sensor object ID with a new name/ID
        :return:
        """
        url = self.combine_url(self.duplicateobject)
        print(url)
        print('Cloning Group or Sensor: {} and renaming {} with new ID of {}'.format(self.cloneid, self.name, self.newid))
        print("Group monitoring is paused. Please resume via the GUI or with 'site.resume_node'")

        return requests.post(url, params={'username': self.username,'password': self.password,'id': self.cloneid, 'name':self.name, 'targetid':self.newid}, verify=False)


    def duplicate_device(self):
        """
        POST request to duplicate a device object ID with a new name/ID
        :return:
        """
        url = self.combine_url(self.duplicateobject)


        print('Cloning Device: {} and renaming {} with new ID of {}'.format(self.cloneid, self.name, self.newid))

        return requests.post(url, params={'username': self.username,'password': self.password,'id': self.cloneid, 'name':self.name,'host':self.name, 'targetid':self.newid}, verify=False)




