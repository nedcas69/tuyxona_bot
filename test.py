import ast
import json

import requests
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth('API', '@3395')

r = requests.get('http://167.124.210.211:8888/isup/hs/employee/getEmployee/'+'57394', auth=auth)

r_name = r.text
# j_name = r.json()
html = r.text.encode('ISO-8859-1').decode('utf-8-sig')
# name = html.replace('\"', '\'')
name = json.loads(html)
# ast.literal_eval(html)
day = [i for i in range(1,32)]
print(day)
