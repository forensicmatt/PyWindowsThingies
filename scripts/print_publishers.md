# Usage
```
usage: print_publishers.py [-h] [-p PUBLISHER]

Print metadata of all registered Windows Event publishers or a specific publisher. Version: 0.0.1

optional arguments:
  -h, --help            show this help message and exit
  -p PUBLISHER, --publisher PUBLISHER
                        A specific publisher.
```

# Output
`python print_publishers.py`

```
...
----------------------------------------------
Publisher: Microsoft-Windows-AppModel-State
GUID: BFF15E13-81BF-45EE-8B16-7CFEAD00DA86
----------------------------------------------
0x0000000000000001: Structured [Structured State]
0x0000000000000002: UnstructuredReset [Unstructured Reset]
0x0000000000000004: OutOfMemory [Out Of Memory]
0x0000000000000008: ApiSetError [Apiset Error]
0x0000000000000010: WinRT [WinRT]
0x0000000000000020: DataStoreError [Low-level Data Store Error]
0x0001000000000000: win:ResponseTime [Response Time]

----------------------------------------------
Publisher: Microsoft-Windows-AppReadiness
GUID: F0BE35F8-237B-4814-86B5-ADE51192E503
----------------------------------------------
0x0000000000000001: Service
0x0000000000000002: User
0x0000000000000004: Tasks
0x0000000000000008: Api
0x0000000000000010: Scoring
0x0000000000000020: BrokerSession
0x0000000000000040: Triggers
0x0000000000000080: Error
0x0000000000000100: Timeline
0x0000400000000000: ms:Measures
0x0001000000000000: win:ResponseTime [Response Time]

----------------------------------------------
Publisher: Microsoft-Windows-AppSruProv
GUID: 0CC157B3-CF07-4FC2-91EE-31AC92E05FE1
----------------------------------------------

----------------------------------------------
Publisher: Microsoft-Windows-AppXDeployment
GUID: 8127F6D4-59F9-4ABF-8952-3E3A02073D5F
----------------------------------------------
0x0000000000000001: APPXDEPLOYMENT_KEYWORD [AppXDeployment]
0x0000000000000002: APPMODEL_RUNTIME_DMR_KEYWORD [DMR]
0x0000000000010000: AppXDeployment
0x0000000000020000: DMR
0x0000400000000000: ms:Measures
0x0001000000000000: win:ResponseTime [Response Time]
...
```