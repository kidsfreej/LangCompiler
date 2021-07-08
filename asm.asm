extern _print
global _epic
section .text
_epic:
epic:
        push ebp
        mov ebp , esp
        ; mov eax, 5
        call _print
        ret



