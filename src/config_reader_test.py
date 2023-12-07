import config_reader as cr

def test_reader(filepath):
    x = cr.read_config(filepath)
    
    try:
        general_values, test_values = x
    except:
        print("wew")
        return
    
    print(general_values.retest_time,general_values.max_hops, general_values.timeout)
    for x in test_values:
        print(x.gateway, x.destination, x.port, x.protocol)
    
test_reader("../random_test/config_3.ini")   
    