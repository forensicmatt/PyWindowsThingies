#  Cool win-thingies
My repository for doing cool windows things.

# Scripts

## scripts/print_handles.py
```
usage: print_handles.py [-h] [-p PID] [-t TYPE]

Print Open Handles. I recommend using the --type param.
Some handle enumeration can cause hanging. Working on fix...

optional arguments:
  -h, --help            show this help message and exit
  -p PID, --pid PID     A specific PID.
  -t TYPE, --type TYPE  Only print specific handle types. [File, Key, etc.]
```

### Example Output
Get opened Key handles for Explore.exe (with pid 6604):

`print_handles.py -p 6604 -t Key`

```
...
{"CreatorBackTraceIndex":0,"Reserved":0,"Name":"\\REGISTRY\\USER\\S-1-5-21-2350377626-499376046-3523757530-1001\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist\\{CEBFF5CD-ACE2-4F4F-9178-9926F41749EA}\\Count","HandleValue":10092,"HandleAttributes":0,"ObjectTypeIndex":43,"Type":"Key","GrantedAccess":196639,"Object":18446626440585191536,"UniqueProcessId":6604}
{"CreatorBackTraceIndex":0,"Reserved":0,"Name":"\\REGISTRY\\USER\\S-1-5-21-2350377626-499376046-3523757530-1001\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist\\{F4E57C4B-2036-45F0-A9AB-443BCFE33D9F}\\Count","HandleValue":10096,"HandleAttributes":0,"ObjectTypeIndex":43,"Type":"Key","GrantedAccess":196639,"Object":18446626440585261776,"UniqueProcessId":6604}
{"CreatorBackTraceIndex":0,"Reserved":0,"Name":"\\REGISTRY\\USER\\S-1-5-21-2350377626-499376046-3523757530-1001\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist\\{B267E3AD-A825-4A09-82B9-EEC22AA3B847}\\Count","HandleValue":10100,"HandleAttributes":0,"ObjectTypeIndex":43,"Type":"Key","GrantedAccess":196639,"Object":18446626440588625584,"UniqueProcessId":6604}
{"CreatorBackTraceIndex":0,"Reserved":0,"Name":"\\REGISTRY\\USER\\S-1-5-21-2350377626-499376046-3523757530-1001\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist\\{9E04CAB2-CC14-11DF-BB8C-A2F1DED72085}\\Count","HandleValue":10104,"HandleAttributes":0,"ObjectTypeIndex":43,"Type":"Key","GrantedAccess":196639,"Object":18446626440586308592,"UniqueProcessId":6604}
{"CreatorBackTraceIndex":0,"Reserved":0,"Name":"\\REGISTRY\\USER\\S-1-5-21-2350377626-499376046-3523757530-1001\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist\\{FA99DFC7-6AC2-453A-A5E2-5E2AFF4507BD}\\Count","HandleValue":10108,"HandleAttributes":0,"ObjectTypeIndex":43,"Type":"Key","GrantedAccess":196639,"Object":18446626440587252752,"UniqueProcessId":6604}
{"CreatorBackTraceIndex":0,"Reserved":0,"Name":"\\REGISTRY\\USER\\S-1-5-21-2350377626-499376046-3523757530-1001\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist\\{CAA59E3C-4792-41A5-9909-6A6A8D32490E}\\Count","HandleValue":10112,"HandleAttributes":0,"ObjectTypeIndex":43,"Type":"Key","GrantedAccess":196639,"Object":18446626440587730624,"UniqueProcessId":6604}
{"CreatorBackTraceIndex":0,"Reserved":0,"Name":"\\REGISTRY\\USER\\S-1-5-21-2350377626-499376046-3523757530-1001\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist\\{A3D53349-6E61-4557-8FC7-0028EDCEEBF6}\\Count","HandleValue":10116,"HandleAttributes":0,"ObjectTypeIndex":43,"Type":"Key","GrantedAccess":196639,"Object":18446626440587767920,"UniqueProcessId":6604}
{"CreatorBackTraceIndex":0,"Reserved":0,"Name":"\\REGISTRY\\USER\\S-1-5-21-2350377626-499376046-3523757530-1001\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist\\{F2A1CB5A-E3CC-4A2E-AF9D-505A7009D442}\\Count","HandleValue":10120,"HandleAttributes":0,"ObjectTypeIndex":43,"Type":"Key","GrantedAccess":196639,"Object":18446626440569601136,"UniqueProcessId":6604}
{"CreatorBackTraceIndex":0,"Reserved":0,"Name":"\\REGISTRY\\USER\\S-1-5-21-2350377626-499376046-3523757530-1001\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist\\{BCB48336-4DDD-48FF-BB0B-D3190DACB3E2}\\Count","HandleValue":10124,"HandleAttributes":0,"ObjectTypeIndex":43,"Type":"Key","GrantedAccess":196639,"Object":18446626440562674192,"UniqueProcessId":6604}
...
```

# Thanks
Thanks to other people's work that were great win32 ctype references.
 
- https://github.com/hakril/PythonForWindows
- https://github.com/NadavRazDev/dotfiles
