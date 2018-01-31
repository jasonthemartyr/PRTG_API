import requests
from xml.etree import ElementTree
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class PRTG(object):
    def __init__(self, url, **kwargs):
        auth_payload = kwargs
        self.url = url
        self.sensortree = '/api/table.xml?content=sensortree'
        self.pause = '/api/pause.htm?'
        self.delete = '/api/deleteobject.htm?'
        self.duplicateobject = '/api/duplicateobject.htm?'

        self.username = auth_payload.get('username') if 'username' in auth_payload else False
        self.password = auth_payload.get('password') if 'password' in auth_payload else False

    def __combine_url(self, uri):
        """
        Combines base URL with URI
        :param uri:
        :return:
        """
        urls = self.url + '{}'
        request = urls.format(uri)
        return request

    def __get_device_ids(self, device_name):
        """
        GET request to filter XML response and return ID : DEVICE NAME in a dictionary
        :return:
        """

        url = self.__combine_url(self.sensortree)
        # print(url)
        r = requests.get(url, params={'username': self.username, 'password': self.password}, verify=False, stream=True)
        r.raw.decode_content = True
        # print(r)
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
            if device_name in value:
                output_dict[key] = value
        return output_dict

    # need 'get_group_id' method

    def pause_node(self, node_id):
        """
        POST request ro pause monitoring for a node ID specified by user
        :param node_id:
        :return:
        """
        url = self.__combine_url(self.pause)
        pause_msg = 'Pausing {}.....'.format(node_id)
        print(pause_msg)
        return requests.post(url, params={'username': self.username, 'password': self.password, 'id': node_id,
                                          'pausemsg': pause_msg, 'action': '0'}, verify=False)

    def resume_node(self, node_id):
        """
        POST request to resume monitoring for a node ID specified by user
        :param node_id:
        :return:
        """
        url = self.__combine_url(self.pause)
        return requests.post(url, params={'username': self.username, 'password': self.password, 'id': node_id,
                                          'action': '1'}, verify=False)
        # return request

    def delete_node(self, node_id):
        """
        DELETE request to delete node ID specified by user
        :param node_id:
        :return:
        """

        url = self.__combine_url(self.delete)
        print('Deleting {}.....'.format(node_id))
        return requests.delete(url, params={'username': self.username, 'password': self.password, 'id': node_id,
                                            'approve': '1'}, verify=False)

    def duplicate_object(self, **kwargs):
        """
        POST request to duplicate a device, group, or sensor
        :param kwargs:
        :return:
        """

        parameters_payload = kwargs
        url = self.__combine_url(self.duplicateobject)

        id_of_device_to_clone = parameters_payload.get(
            'id_of_device_to_clone') if 'id_of_device_to_clone' in parameters_payload else False
        new_name = parameters_payload.get('new_name') if 'new_name' in parameters_payload else False
        new_hostname_or_ip = parameters_payload.get(
            'new_hostname_or_ip') if 'new_hostname_or_ip' in parameters_payload else False
        id_of_target_group = parameters_payload.get(
            'id_of_target_group') if 'id_of_target_group' in parameters_payload else False

        if 'device' in parameters_payload.get('object_type'):
            requests.post(url, params={'username': self.username, 'password': self.password,
                                       'id': id_of_device_to_clone, 'name': new_name,
                                       'host': new_hostname_or_ip, 'targetid': id_of_target_group}, verify=False)
            node_id = self.__get_device_ids(new_name)
            self.resume_node(node_id)

            return 'Cloned device {} to Group {} as {}'.format(id_of_device_to_clone, id_of_target_group, new_name)

        elif 'group' in parameters_payload.get('object_type') or 'sensor' in parameters_payload.get('object_type'):
            requests.post(url, params={'username': self.username, 'password': self.password,
                                       'id': id_of_device_to_clone, 'name': new_name,
                                       'targetid': id_of_target_group}, verify=False)
            return 'Cloned group {} as {}'.format(id_of_device_to_clone, id_of_target_group)

            # group_id = self.__get_device_ids(new_name)  # need get group ID method
            # return self.resume_node(group_id)
