import numpy as np
import sys
sys.path.append('C:\\Program Files (x86)\\PIPC\\AF\\PublicAssemblies\\4.0\\')
import clr
clr.AddReference('OSIsoft.AFSDK')

from OSIsoft.AF.PI import *
from OSIsoft.AF.Search import *
from OSIsoft.AF.Asset import *
from OSIsoft.AF.Data import *
from OSIsoft.AF.Time import *

def pi_api(tagname, mode):
    pi = PIConnector()
    pi.connect(True)
    if mode == 'read_current':
        name, value = pi.get_tag_snapshot(tagname)
        pi.connect(False)

        results = {
                'name': name,
                'value': float(value)
            }
        return results

def pi_timed_api(tagname, start_date, end_date):
    pi = PIConnector()
    pi.connect(True)
    results = pi_get_tag_timed(tagname, start_date, end_date)
    '''name, value = pi.get_tag_timed(tagname, start_date, end_date)
    results = {
            'name':name,
            'value':value
        }
    '''
    return results
        

class PIConnector():

        # connects and disconnects from database 
    def connect(self, status):
        piServers = PIServers()
        global piServer
        piServer = piServers.DefaultPIServer
        if status == True:
            piServer.Connect()
        else:
            piServer.Disconnect()

        # Gets last value for tag
    def get_tag_snapshot(self, tagname):
        pt = PIPoint.FindPIPoint(piServer, tagname)
        name = pt.Name
        current_value = pt.CurrentValue().ToString()
        return name, current_value

        # Gets timed data from start to finished
    def get_tag_timed(self, tagname, start_date, end_date):
        pt = PIPoint.FindPIPoint(piServer, tagname)
        t_range = AFTimeRange(start_date, end_date)
        boundary = AFBoundaryType.Inside
        
        data = pt.RecordedValues(t_range, boundary,'',False, 0)
        data_list = list(data)
        result = data_list
        results = np.zeros((len(data_list), 2), dtype='object')
        for i, sample in enumerate(data):
            results[i,:]= np.array([str(sample.Timestamp), float(sample.Value)])

        new_results = []
        for r in results:
            new_result = {
                    'date': str(r[0]),
                    'value': r[1]
                }
            new_results.append(new_result)
        
        return new_results


