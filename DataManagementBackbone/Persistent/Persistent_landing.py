
import shutil
import os
import datetime

def persistent():
    
    PERSISTENT = os.getcwd()
    PERSISTENT = PERSISTENT[0:-41]+'Landing_Zone\\Persistent_Landing\\'

    TEMPORAL = PERSISTENT[0:-19]+'Temporal_Landing\\'
    TEMPORAL

    for data in ('ATPdata.csv','tennis_data.csv'):
        destination = PERSISTENT + data
        source = TEMPORAL + data
        task = 'copy %s %s' % (source,destination)
        os.popen(task)
