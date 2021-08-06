

extern _print
global _mains
global _inits
extern _error
extern _input

extern _getHashmapAsm
extern _reprListReal
extern _initList
extern _appendList
extern _freeList
extern _deepfreeList
extern _addHashmapAsm
extern _callFunc
extern _mem_alloc
section .text
leaveret:
leave
ret



_inits:
push 6
push 0
push 5
push 0
call _addHashmapAsm
add esp, 16
push 0
push 0
push 6
push 1
call _addHashmapAsm
add esp, 16
push 0
push 4
push 6
push 2
call _addHashmapAsm
add esp, 16
push 0
push 0
push 7
push 3
call _addHashmapAsm
add esp, 16
call _mains
leave 
ret 
faJakeaJake2788507163856:
push ebp
mov ebp, esp
sub esp, 8
mov DWORD[ebp-4], 0
mov DWORD[ebp-8], -1
mov eax, DWORD[ebp-8]
cmp eax, 6
je b0
push DWORD[ebp-8]
call _error
add esp, 4
b0:
mov eax, DWORD[ebp-4]
mov ecx, DWORD[ebp+8]
mov DWORD[ecx-0], eax
cmp DWORD[ebp+12], -2
jne b1
push -2
call _error
b1:
leave 
ret 
faJohnaJohn2788507164288:
push ebp
mov ebp, esp
sub esp, 16
mov DWORD[ebp-8], 0
mov DWORD[ebp-4], 50
mov eax, DWORD[ebp-8]
cmp eax, 0
je b2
push DWORD[ebp-8]
call _error
add esp, 4
b2:
mov eax, DWORD[ebp-4]
mov ecx, DWORD[ebp+8]
mov DWORD[ecx-0], eax
mov DWORD[ebp-16], 0
mov DWORD[ebp-12], 51
mov eax, DWORD[ebp-16]
cmp eax, 0
je b3
push DWORD[ebp-16]
call _error
add esp, 4
b3:
mov eax, DWORD[ebp-12]
mov ecx, DWORD[ebp+8]
mov DWORD[ecx-4], eax
cmp DWORD[ebp+12], -2
jne b4
push -2
call _error
b4:
leave 
ret 
faAaA2788507181168:
push ebp
mov ebp, esp
sub esp, 8
mov DWORD[ebp-8], 0
mov DWORD[ebp-4], 100
mov eax, DWORD[ebp-8]
cmp eax, 0
je b5
push DWORD[ebp-8]
call _error
add esp, 4
b5:
mov eax, DWORD[ebp-4]
mov ecx, DWORD[ebp+8]
mov DWORD[ecx-0], eax
cmp DWORD[ebp+12], -2
jne b6
push -2
call _error
b6:
leave 
ret 
faAaaify2788507181456:
push ebp
mov ebp, esp
sub esp, 8
mov eax, DWORD[ebp+12]
cmp eax, 0
je b7
push DWORD[ebp+12]
call _error
add esp, 4
b7:
cmp DWORD[ebp+16], -2
jne b8
push -2
call _error
b8:
mov eax, DWORD[ebp+12]
mov DWORD[ebp-8], eax
mov eax, DWORD[ebp+8]
mov DWORD[ebp-4], eax
push DWORD[ebp+12]
push 3
call _getHashmapAsm
add esp, 8
mov ecx, DWORD[eax+8]
sub DWORD[ebp+8], ecx
mov ecx, DWORD[ebp+8]
mov eax, DWORD[ebp-4]
mov DWORD[ecx], eax
leave 
ret 
fm2788507181216:
push ebp
mov ebp, esp
sub esp, 8
mov eax, DWORD[ebp+12]
cmp eax, 0
je b9
push DWORD[ebp+12]
call _error
add esp, 4
b9:
cmp DWORD[ebp+16], -2
jne b10
push -2
call _error
b10:
mov eax, DWORD[ebp+12]
mov DWORD[ebp-8], eax
mov eax, DWORD[ebp+8]
mov DWORD[ebp-4], eax
mov eax, DWORD[ebp-8]
cmp eax, 0
je b11
push DWORD[ebp-8]
call _error
add esp, 4
b11:
mov eax, DWORD[ebp-4]
push eax
call _print
add esp, 4
leave 
ret 
_mains:
push ebp
mov ebp, esp
sub esp, 0
cmp DWORD[ebp+12], -2
jne b12
push -2
call _error
b12:
leave 
ret 
