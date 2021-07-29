#include "StdAfx.h"
#include "Injector.h"
#include <TlHelp32.h>
#include <shlwapi.h>
#include <conio.h>
#include <stdio.h>
#include <windows.h>


Injector::Injector(void)
{
}


Injector::~Injector(void)
{
}

#define CREATE_THREAD_ACCESS (PROCESS_CREATE_THREAD | PROCESS_QUERY_INFORMATION | PROCESS_VM_OPERATION | PROCESS_VM_WRITE | PROCESS_VM_READ)

bool Injector::Inject(char* procName,char* dllName)
{
    DWORD pId=GetTargetThreadIDFromProcName(procName);

    if(!pId)
        return false;

    char dll_name[MAX_PATH]={0};

    GetFullPathName(dllName,MAX_PATH,dll_name,NULL);

    printf(dll_name);
    printf("\n");

    HANDLE proc=0;
    HMODULE hLib=0;

    char buf[50]={0};

    LPVOID RemoteString, LoadLibAddy;


    proc=OpenProcess(PROCESS_ALL_ACCESS,FALSE,pId);

    if(!proc)
    {
        printf("failed to open process");
        return false;
    }

    //GetProcAddress :: Retrieves the address of an exported function or variable from the specified dynamic-link library (DLL).
    LoadLibAddy = (LPVOID) GetProcAddress(GetModuleHandle("kernel32.dll"),"LoadLibraryA");

    //Allocate memory space for the dll name in the process space
    RemoteString=(LPVOID)VirtualAllocEx(proc,NULL,strlen(dll_name),MEM_RESERVE|MEM_COMMIT,PAGE_READWRITE);

    //write the name of the dll in this address space
    WriteProcessMemory(proc,RemoteString,dll_name,strlen(dll_name),NULL);


    //Load our dll using loadlibrary
    CreateRemoteThread(proc,NULL,NULL,(LPTHREAD_START_ROUTINE)LoadLibAddy,(LPVOID)RemoteString,NULL,NULL);


    CloseHandle(proc);

    return TRUE;

}


DWORD Injector::GetTargetThreadIDFromProcName(const char* procName)
{
    PROCESSENTRY32 pe;
    HANDLE thSnapShot;

    BOOL retval, procFound=false;

    thSnapShot=CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS,0);
    if(thSnapShot==INVALID_HANDLE_VALUE)
    {
        printf("Error: unable to create toolhelp snapshot");
        return false;
    }

    pe.dwSize=sizeof(PROCESSENTRY32);

    retval=Process32First(thSnapShot,&pe);
    while(retval)
    {
        if(!strcmp(pe.szExeFile,procName))
        {
            return pe.th32ProcessID;
        }
        retval=Process32Next(thSnapShot,&pe);
       
    }

    return 0;

}


