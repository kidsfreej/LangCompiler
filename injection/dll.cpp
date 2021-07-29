#include <windows.h>


BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
    case DLL_THREAD_ATTACH:
        OutputDebugStringA("Injected");

        MessageBoxA(NULL,"Injected","Info",0);
        break;
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        OutputDebugStringA("Good bye");
        break;
    }
    return TRUE;
}