#pragma once
#include <Windows.h>

class Injector
{
public:
    Injector(void);
    ~Injector(void);
    bool Inject(char* procName,char* dllName);

private:
    DWORD GetTargetThreadIDFromProcName(const char* procName);
};
