import configparser
import ipaddress
import config_classes as cfg_class

def read_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)

    try:
        general_section = config['general']
    except ValueError:
        print("Error: Incorrect file path")
        return None

    options_check = True
    options_default = cfg_class.General()
    try:
        options = cfg_class.General(float(general_section['retest_time']),
                            int(general_section['max_hops']),
                          float(general_section['timeout']))
    except ValueError:
        print('Error: something is wrong is the general section, using default values')
        options_check = False

    test_string = 'test_'
    test_index = 0
    test_list = []

    while True:
        test_index += 1
        try:
            test_section = config[f'{test_string}{test_index}']
        except KeyError:
            break

        try:
            test_values = cfg_class.TestConfig(ipaddress.ip_address(test_section['gateway']),
                                     ipaddress.ip_address(test_section['dest']),
                                                      int(test_section['port']),
                                                          test_section['protocol'].lower())
        except ValueError:
            print(f'Error: test_{test_index} is invalid!')
        else:
            if test_values.check(test_index):
                test_list.append(test_values)

    if len(test_list) == 0:
        print('Error: At lest one valid test is required')
        return None

    if options_check:
        return(options, test_list)

    return(options_default, test_list)
