from PRTG_Class import PRTG


def main():
    base_url = 'https://prtg-monitor.XXXXX.net'

    username = 'jmarter'
    password = 'PASSWORD'

    id_of_device_to_clone = '14756'  # Device ID for Joliet-IL-109.2

    new_name = ' Joliet-IL-109.2 [Cisco Device]'
    new_hostname_or_ip = '172.16.109.3'
    id_of_target_group = '14754'  # Group ID for Joliet, IL -> Routers
    object_type = 'device'

    auth_payload = {'username': username,
                    'password': password
                    }

    parameters_payload = {'id_of_device_to_clone': id_of_device_to_clone,
                          'new_name': new_name,
                          'new_hostname_or_ip': new_hostname_or_ip,
                          'id_of_target_group': id_of_target_group,
                          'object_type': object_type}

    site = PRTG(base_url, **auth_payload)

    # site.pause_node()
    # site.resume_node()
    # site.delete_node()

    #print(site.duplicate_object(**parameters_payload))
#    print(site.get_devices())
    print(set(site.get_devices()))
    # for dizzle in site.get_devices():
    #     print(dizzle)
    #print(site.get_devices())

if __name__ == "__main__":
    main()
