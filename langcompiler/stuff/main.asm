
extern _print
global _mains
section .text

_mains:
push esp
mov ebp,esp
mov eax,0
add eax, 51
add eax, 90
add eax, 7
push eax
call _print
add esp ,4
pop ebp
ret
