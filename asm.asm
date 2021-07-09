extern _print
global _epic
section .text






_epic:
        push esp
        mov ebp,esp
        sub esp,28
        ;greatest
        mov eax,99999


        mov edx,ebp
        add edx,20

        mov edi,0
        
        mov ecx,ebp
        add ecx,8
        
        outer:
                ;t greatest
                mov ebx,-1
                inner:

                        cmp DWORD[ecx],ebx
                         jle done
                        cmp DWORD[ecx],eax 
                        jge done
                        nop
                        nop
                        nop
                        add eax,10000
                        analyse:
                        nop
                        nop
                        sub eax,10000
                        mov ebx,DWORD[ecx]
                                
                        done:

                        
                add ecx,4
                cmp ecx,edx
                jle inner
 

                mov DWORD[ebp-4], eax
                mov DWORD[ebp-8], ecx
                mov DWORD[ebp-12], edi
                mov DWORD[ebp-16], esi
                mov DWORD[ebp-20], ebx
                mov DWORD[ebp-24], edx

                push ebx
                call _print
                add esp, 4

                mov  eax ,DWORD[ebp-4]
                mov  ecx ,DWORD[ebp-8]
                mov edi, DWORD[ebp-12]
                mov esi,DWORD[ebp-16]
                mov ebx,DWORD[ebp-20]
                mov edx,DWORD[ebp-24]
                
        
                mov eax,ebx
                

        add edi,1
        cmp edi,4
        jl outer

        leave
        ret



