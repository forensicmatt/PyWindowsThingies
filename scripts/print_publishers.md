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
Publisher: Microsoft-Windows-Kernel-Process
GUID: 22FB2CD6-0E7B-422B-A0C7-2FAD1FD0E716
----------------------------------------------
Resource Path: C:\WINDOWS\system32\Microsoft-Windows-System-Events.dll
Message Path: C:\WINDOWS\system32\Microsoft-Windows-System-Events.dll
Help Link: https://go.microsoft.com/fwlink/events.asp?CoName=Microsoft%20Corporation&ProdName=Microsoft%c2%ae%20Windows%c2%ae%20Operating%20System&ProdVer=10.0.17134.1&FileName=Microsoft-Windows-System-Events.dll&FileVer=10.0.17134.1
--- Channels ---
0x0000000000000000: Microsoft-Windows-Kernel-Process/Analytic
--- Keywords ---
0x0000000000000010: WINEVENT_KEYWORD_PROCESS
0x0000000000000020: WINEVENT_KEYWORD_THREAD
0x0000000000000040: WINEVENT_KEYWORD_IMAGE
0x0000000000000080: WINEVENT_KEYWORD_CPU_PRIORITY
0x0000000000000100: WINEVENT_KEYWORD_OTHER_PRIORITY
0x0000000000000200: WINEVENT_KEYWORD_PROCESS_FREEZE
0x0000000000000400: WINEVENT_KEYWORD_JOB
0x0000000000000800: WINEVENT_KEYWORD_ENABLE_PROCESS_TRACING_CALLBACKS
0x0000000000001000: WINEVENT_KEYWORD_JOB_IO
0x0000000000002000: WINEVENT_KEYWORD_WORK_ON_BEHALF
0x0000000000004000: WINEVENT_KEYWORD_JOB_SILO
--- Operations ---
0x0000000000000000: win:Info [Info]
0x0000000000010000: win:Start [Start]
0x0000000000020000: win:Stop [Stop]
--- Levels ---
0x0000000000000004: win:Informational [Information]
--- Tasks ---
0x0000000000000001: ProcessStart
0x0000000000000002: ProcessStop
0x0000000000000003: ThreadStart
0x0000000000000004: ThreadStop
0x0000000000000005: ImageLoad
0x0000000000000006: ImageUnload
0x0000000000000007: CpuBasePriorityChange
0x0000000000000008: CpuPriorityChange
0x0000000000000009: PagePriorityChange
0x000000000000000A: IoPriorityChange
0x000000000000000B: ProcessFreeze
0x000000000000000D: JobStart
0x000000000000000E: JobTerminate
0x000000000000000F: ProcessRundown
0x0000000000000010: PsDiskIoAttribution
0x0000000000000011: PsIoRateControl
0x0000000000000012: ThreadWorkOnBehalfUpdate
0x0000000000000013: JobServerSiloStart

----------------------------------------------
Publisher: Microsoft-Windows-Kernel-Processor-Power
GUID: 0F67E49F-FE51-4E9F-B490-6F2948CC6027
----------------------------------------------
Resource Path: C:\WINDOWS\system32\microsoft-windows-kernel-processor-power-events.dll
Message Path: C:\WINDOWS\system32\microsoft-windows-kernel-processor-power-events.dll
Help Link: https://go.microsoft.com/fwlink/events.asp?CoName=Microsoft%20Corporation&ProdName=Microsoft%c2%ae%20Windows%c2%ae%20Operating%20System&ProdVer=10.0.17134.1&FileName=microsoft-windows-kernel-processor-power-events.dll&FileVer=10.0.17134.1
--- Channels ---
0x0000000000000000: System [System]
0x0000000000000001: Microsoft-Windows-Kernel-Processor-Power/Diagnostic
--- Keywords ---
0x0000000000000001: Perf
0x0000000000000002: Diag
0x0000000000000004: PowerDiagnostics
0x0000000000000008: Lpi
0x0000000000000010: SleepStudy
0x0000000000000020: Algorithm
0x0000000000000040: Profiles
0x0000000000000080: PerfDiag
0x0000000000000100: EnergyEstimation
--- Operations ---
0x0000000000000000: win:Info [Info]
0x0000000000010000: win:Start [Start]
0x0000000000020000: win:Stop [Stop]
0x0000000000210000: Makeup
0x0000000000220000: FailedStart
--- Levels ---
0x0000000000000002: win:Error [Error]
0x0000000000000003: win:Warning [Warning]
0x0000000000000004: win:Informational [Information]
0x0000000000000005: win:Verbose [Verbose]
--- Tasks ---
0x0000000000000001: IdleStatesError
0x0000000000000002: PerfStatesError
0x0000000000000003: ThrottleStatesError
0x0000000000000004: Summary
...
```