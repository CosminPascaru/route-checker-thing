from potraceroute import Traceroute, parse_options
import config_reader
from save_thread_result import ThreadWithResult
from threading import Thread

class ThreadWithReturnValue(Thread):
    
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

def handle_test(general, test_config, test_index):
    max_hops = int(general.max_hops)
    timeout  = general.timeout
    
    gateway = test_config.gateway
    dest = test_config.destination
    port = test_config.port
    protocol = test_config.protocol
    
    if test_config.protocol == "tcp":
        (options, args) = parse_options([
                    "--port", port,
                    "--wait-time", timeout,
                    "--no-dns", dest])
    elif test_config.protocol == "icmp":
        (options, args) = parse_options([
                    "--wait-time", timeout,
                    "--no-dns", 
                    f"--{protocol}", dest])
    else:
        (options, args) = parse_options([
                    "--port", port,
                    "--wait-time", timeout,
                    "--no-dns", 
                    f"--{protocol}", dest])

    t1 = ThreadWithReturnValue(target=run_probe, args=(max_hops, dest, options))
    t2 = ThreadWithReturnValue(target=run_probe, args=(max_hops, dest, options))
    t3 = ThreadWithReturnValue(target=run_probe, args=(max_hops, dest, options))
    
    t1.start()
    t2.start()
    t3.start()
    
    t1_result = t1.join()
    t2_result = t2.join()
    t3_result = t3.join()
    
    if t1_result == 0 | t2_result == 0 | t3_result == 0:
        print(f"it worky {test_index}")
    else: 
        print(f"it no worky {test_index}")
    

def run_probe(max_hops, dest, options):
    trace = Traceroute(options, dest)
    #print(trace.header) #only for debugging :)
    ttl = 1
    while ttl <= max_hops:
        hop = trace.probe(ttl)
        #print(hop) #state of art debugging
        if hop.final:
            break
        ttl += 1
    return 0 if hop.reached else 1

def func():
    filepath = 'config.ini'
    
    try:
        general, tests = config_reader.read_config(filepath)
    except:
        print("lmao")
    
    test_index = 1
    for test in tests:
        thread = ThreadWithReturnValue(target=handle_test, args=(general, test, test_index))
        thread.start()
        test_index += 1
        
    print("Bruh it already started")
    
func()   
    

    