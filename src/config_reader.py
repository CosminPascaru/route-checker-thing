import configparser
import ipaddress
import config_classes as cfg_class

def read_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)

    try:# to read first section to check if filepath is correct
        general_section = config['general']
    except ValueError:
        print("Error: Incorrect file path")
        return None

    options_check = True
    try:# to read & convert to check if values are valid
        options = cfg_class.General(general_section['retest_time'],
                                    general_section['max_hops'],
                                    general_section['timeout'])
        int(options.retest_time)
        int(options.max_hops)
        int(options.timeout)
    except ValueError:
        print('Error: something is wrong is the general section, using default values')
        options_check = False

    test_string = 'test_'
    test_index = 1
    test_list = []

    while True:
        try:# to read next test
            test_section = config[f'{test_string}{test_index}']
        except KeyError:
            break

        try:# to read & convert to check if values are valid
            test_values = cfg_class.TestConfig(test_section['gateway'],
                                               test_section['dest'],
                                               test_section['port'],
                                               test_section['protocol'].lower())
            ipaddress.ip_address(test_values.gateway)
            ipaddress.ip_address(test_values.destination)
            int(test_values.port)
        except ValueError:
            print(f'Error: test_{test_index} is invalid!')
        else:
            if test_values.check(test_index):
                test_list.append(test_values)
        test_index += 1

    if len(test_list) == 0:
        print('Error: At lest one valid test is required')
        return None

    if options_check:
        return (options, test_list)

    return (cfg_class.General(), test_list)
