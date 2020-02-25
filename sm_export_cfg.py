import ConfigParser
import os

class SmExportCfg:
    warn_connections = True 
    header_file = True
    debug_state_change = False
    multithread_enable = True
    config = None
    config_fname = 'sm_export.cfg'

    def __init__(self):
        home = os.path.join("C:\\Users",os.getenv('username'))
        dia_path = os.path.join(home,".dia")
        # Check if 'python' directory exists
        dia_path = os.path.join(dia_path,"python")
        if os.path.isdir(dia_path) == False:
            os.mkdir(dia_path)
        self.config_path = os.path.join(dia_path,self.config_fname)
        self.config = ConfigParser.SafeConfigParser()
        self.load()
        
    def load(self):
        if not os.path.exists(self.config_path):
            print "Configuration file [%s] not found!!! It will be created." % (self.config_path)
            self.config.add_section('options')
            self.config.set('options','warn_connections',self.warn_connections)
            self.config.set('options','header_file',self.header_file)
            self.config.set('options','debug_state_change',self.debug_state_change)
            self.config.set('options', 'multithread_enable',self.multithread_enable)
            configfile = open(self.config_path,"w")
            self.config.write(configfile)
            configfile.close() 
        else:
            self.config.read(self.config_path)
            print "Configuration file [%s] successfully read!!!" % (self.config_path)
            self.warn_connections = self.config.getboolean('options', 'warn_connections')
            self.header_file = self.config.getboolean('options','header_file')
            self.debug_state_change = self.config.getboolean('options','debug_state_change')
            self.multithread_enable = self.config.getboolean('options','multithread_enable')             

    def save(self):
        self.config = ConfigParser.SafeConfigParser()
        self.config.add_section('options')

        if self.warn_connections:
            value = 'True'
        else:
            value = 'False'        
        self.config.set('options','warn_connections',value)
        
        if self.header_file:
            value = 'True'
        else:
            value = 'False'        
        self.config.set('options','header_file',value)

        if self.debug_state_change:
            value = 'True'
        else:
            value = 'False'        
        self.config.set('options','debug_state_change',value)

        if self.multithread_enable:
            value = 'True'
        else:
            value = 'False'
        self.config.set('options','multithread_enable',value)

        configfile = open(self.config_path,"w")
        self.config.write(configfile)
        configfile.close()