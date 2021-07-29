

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



faJakeaJake2340167373680:
push ebp
mov ebp, esp
sub esp, 8
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
jmp leaveret
leave 
ret 
_mains:
push ebp
mov ebp, esp
sub esp, 16
mov DWORD[ebp-4], 0
mov DWORD[ebp-8], -1
mov eax, DWORD[ebp-8]
cmp eax, 5
je b2
push DWORD[ebp-8]
call _error
add esp, 4
b2:
mov DWORD[ebp-16], 0
mov DWORD[ebp-12], 1
mov eax, DWORD[ebp-16]
cmp eax, 0
je b3
push DWORD[ebp-16]
call _error
add esp, 4
b3:
mov eax, DWORD[ebp-12]
jmp leaveret
leave 
ret 
