

extern _print
global _mains
extern _error
extern _input

extern _reprListReal
extern _initList
extern _appendList
extern _freeList
extern _deepfreeList

extern _mem_alloc
section .text
leaveret:
leave
ret



faJakeaJake1839845071360:
push ebp
mov ebp, esp
sub esp, 8
mov DWORD[ebp-8], 0
mov DWORD[ebp-4], 100
mov eax, DWORD[ebp-8]
cmp eax, 0
je b0
push DWORD[ebp-8]
call _error
add esp, 4
b0:
mov eax, DWORD[ebp-4]
push eax
call _print
add esp, 4
leave 
ret 
_mains:
push ebp
mov ebp, esp
sub esp, 24
mov DWORD[ebp-8], 5
push 4
call _mem_alloc
add esp, 4
mov DWORD[ebp-4], eax
push eax
call faJakeaJake1839845071360
add esp, 4
mov eax, DWORD[ebp-8]
cmp eax, 5
je b1
push DWORD[ebp-8]
call _error
add esp, 4
b1:
mov DWORD[ebp-16], 0
gdbtime:
mov eax, DWORD[ebp-4]
mov eax, DWORD[eax+4]
gdblime:


push eax
call _print
add esp, 4



mov DWORD[ebp-24], 0
mov DWORD[ebp-20], 200
mov eax, DWORD[ebp-24]
cmp eax, 0
je b3
push DWORD[ebp-24]
call _error
add esp, 4
b3:
mov eax, DWORD[ebp-20]
push eax
call _print
add esp, 4
leave 
ret 
