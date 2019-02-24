# etw_mon.py
`etw_mon.py` is a tool that can custom monitor etw based off of yaml templates.

```
usage: etw_mon.py [-h] -t TEMPLATE

Monitor ETW.

optional arguments:
  -h, --help            show this help message and exit
  -t TEMPLATE, --template TEMPLATE
                        The template.
```

# Example YML Templates
```yaml
session_name: NT Kernel Logger
providers:
  - name: Windows Kernel Trace
    guid: "{9E814AAD-3204-11D2-9A82-006008A86939}"
    match_any_keyword: 0x04000000
filter:
  query: "ends_with(to_string(OpenPath), '.pf')"
output:
  format: "{record['TimeStamp']}: {record['OpenPath']}"
``` 
*kernel-fileio.yml*

```
C:\Python36\python.exe etw_mon.py -t kernel-fileio.yml
2019-02-24 22:30:16.696926: \Device\HarddiskVolume6\Windows\Prefetch\BACKGROUNDTASKHOST.EXE-E08DE009.pf
2019-02-24 22:30:16.699686: \Device\HarddiskVolume6\Windows\Prefetch\BACKGROUNDTASKHOST.EXE-E08DE009.pf
2019-02-24 22:30:16.699798: \Device\HarddiskVolume6\Windows\Prefetch\BACKGROUNDTASKHOST.EXE-E08DE009.pf
2019-02-24 22:30:17.700542: \Device\HarddiskVolume6\Windows\Prefetch\BACKGROUNDTASKHOST.EXE-E08DE009.pf
2019-02-24 22:30:23.394640: \Device\HarddiskVolume6\Windows\Prefetch\CALC.EXE-A7D3F5D3.pf
2019-02-24 22:30:23.396876: \Device\HarddiskVolume6\Windows\Prefetch\CALC.EXE-A7D3F5D3.pf
2019-02-24 22:30:23.397020: \Device\HarddiskVolume6\Windows\Prefetch\CALC.EXE-A7D3F5D3.pf
```

# Template Reference
`session_name`: The Session name for this ETW trace. (Must be 'NT Kernel Logger' 
if using Kernel Trace providers)

`providers`: A list of providers.
  - `name`: The name of the provider
  - `guid`: The GUID of the provider
  - `match_any_keyword`: A bitmask of keywords that determine the category of 
  events that you want the provider to write. The provider writes the event 
  if any of the event's keyword bits match any of the bits set in this mask.
  - `match_all_keyword`: This bitmask is optional. This mask further restricts 
  the category of events that you want the provider to write. If the event's 
  keyword meets the MatchAnyKeyword condition, the provider will write the 
  event only if all of the bits in this mask exist in the event's keyword. 
  This mask is not used if MatchAnyKeyword is zero

`filter.query`: A JMES Path query that must evaluate as true for the 
record to be processed.

`output.format`: A specific output format fstring.

# References
https://docs.microsoft.com/en-us/windows/desktop/etw/enabletraceex2