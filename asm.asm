

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



faJakeaJake1187541886480:
push ebp
mov ebp, esp
sub esp, 16
mov DWORD[ebp-8], 0
mov DWORD[ebp-4], 5
mov eax, DWORD[ebp-8]
cmp eax, 0
je b0
push DWORD[ebp-8]
call _error
add esp, 4
b0:
mov eax, DWORD[ebp-4]
mov ecx, DWORD[ebp+8]
mov DWORD[ecx+4], eax
mov eax, DWORD[ebp-8]
cmp eax, 0
je b1
push DWORD[ebp-8]
call _error
add esp, 4
b1:
mov DWORD[ebp-16], 0
mov DWORD[ebp-12], 100
mov eax, DWORD[ebp-16]
cmp eax, 0
je b2
push DWORD[ebp-16]
call _error
add esp, 4
b2:
mov eax, DWORD[ebp-12]
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
call faJakeaJake1187541886480
add esp, 4
mov eax, DWORD[ebp-8]
cmp eax, 5
je b3
push DWORD[ebp-8]
call _error
add esp, 4
b3:
mov DWORD[ebp-16], 0
mov eax, DWORD[ebp-4]
mov eax, DWORD[eax+4]
mov DWORD[ebp-12], eax
mov eax, DWORD[ebp-16]
cmp eax, 0
je b4
push DWORD[ebp-16]
call _error
add esp, 4
b4:
mov eax, DWORD[ebp-12]
push eax
call _print
add esp, 4
mov DWORD[ebp-24], 0
mov DWORD[ebp-20], 200
mov eax, DWORD[ebp-24]
cmp eax, 0
je b5
push DWORD[ebp-24]
call _error
add esp, 4
b5:
mov eax, DWORD[ebp-20]
push eax
call _print
add esp, 4
leave 
ret 
