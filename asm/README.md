# Simple 89 points

>Description:
>A really simple crackme to get started ;) Your goal is to find the correct input so that the program return 1. The correct input will be the flag.
>Creator : Nofix

[main.asm](main.asm)

If correct input will return 1, so we need to get to `win` function and avoid `exit`:
```asm
win:
	mov rdi, 1   ; return 1
	mov rax, 60
	syscall
exit:
	mov rdi, 0   ; return 0
	mov rax, 60
	syscall
```
In order to get to `win`, we need to pass though `main`,`l1` and `follow_the_label`

## Analyse

In function main:
```asm
mov rdx, [rsp] ; rsp is argc in C programming (Numbers of arg)
cmp rdx, 2	   ; If not equal 2 then exit
jne exit

mov rsi, [rsp+0x10] ; [rsp+0x10] is our input (2nd arg)
mov rdx, rsi        ; Put the pointer to rdx
mov rcx, 0
```

In function l1:
```asm
cmp byte [rdx], 0   ; If is null then jump to follow_the_label
je follow_the_label 
inc rcx             ; Increase rcx and rdx and continue from top
inc rdx             ; So it loops until (\0) null bytes of our input
jmp l1
```	

In function follow_the_label:
```asm
mov al, byte [rsi+rcx-1]  ; rsi is the input pointer and rcx is index at null
                          ; And get a byte from the pointer
                          ; So it begin at end of our input
mov rdi,  some_array      ; Put the some_array address to rdi
mov rdi, [rdi+rcx-1]      ; Also starts at the end
add al, dil               ; dil is last 8bit of rdi, add it with our input
xor rax, 42               ; XOR it with 42
mov r10, the_second_array ; Does the same thing with first array
add r10, rcx              
dec r10
cmp al, byte [r10]        ; If second_array not equal al then exit
jne exit
dec rcx                   ; Decrease index by 1
cmp rcx, 0                ; If index not equal 0 continue from top
jne follow_the_label
```

## Conclusion
```
(flag + some_array) XOR 42 = second_array
```

Do some maths to solve the flag!
```
(flag + some_array) XOR 42 = second_array
(flag + some_array) = second_array XOR 42
flag = (second_array XOR 42) - some_array
```
I wrote a [python script](solve.py) to solve this:
```py
a = [10,2,30,15,3,7,4,2,1,24,5,11,24,4,14,13,5,6,19,20,23,9,10,2,30,15,3,7,4,2,1,24]
b = [0x57,0x40,0xa3,0x78,0x7d,0x67,0x55,0x40,0x1e,0xae,0x5b,0x11,0x5d,0x40,0xaa,0x17,0x58,0x4f,0x7e,0x4d,0x4e,0x42,0x5d,0x51,0x57,0x5f,0x5f,0x12,0x1d,0x5a,0x4f,0xbf]
flag = ''
for i in zip(a,b):
	flag += chr((42^i[1])-i[0])
print(flag)
```
## Flag
Thats it!
```
Result: shkCTF{h3ll0_fr0m_ASM_my_fr13nd}
```
## Reference
[Registers](https:;www.tortall.net/projects/yasm/manual/html/arch-x86-registers.html)