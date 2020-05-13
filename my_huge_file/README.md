# My huge file 297 points
>I have a very big file for you. I hid a present inside.
>Classic tools wont be useful here.
>Connect with ssh big@sharkyctf.xyz -p 9000. Password : big.
>Creator : Nofix

SSH into it:
```bash
big@ee6e73167aa0:~$ls -lh
total 256K
-rw-r--r-- 1 root root 31G May 11 23:13 my_huge_file
big@ee6e73167aa0:~$
```
Notice the `my_huge_file` is **31G!!!**

I tried to use `tr` `cat | grep` but it takes to much time so it been killed

Then do some research on `grep all except null` found:
[Remove blank lines with grep](https://stackoverflow.com/questions/3432555/remove-blank-lines-with-grep)

Then i try:
```bash
grep -v -e '^$' my_huge_file
Binary file my_huge_file matches
```

Then i do more research found this link:
[Grep 'binary file matches'
](https://stackoverflow.com/questions/23512852/grep-binary-file-matches-how-to-get-normal-grep-output)

Need add `-a` option

But i tried, it been killed
```bash
grep -av -e '^$' my_huge_file 
Killed
```

Then i look at the man page of `grep`, notice an option:
```
-z, --null-data

Treat input and output data as sequences of lines, each terminated by a zero byte (the ASCII NUL  character)  instead
of  a newline.  Like the -Z or --null option, this option can be used with commands like sort -z to process arbitrary
file names.

```

Then I quickly test it out:
```
grep -avz -e '^$' my_huge_file 
😏shkCTF{sp4rs3_f1l3s_4r3_c001_6cf61f47f6273dfa225ee3366eacb8eb}
```

Yes!! We get the damn flag!!

## Flag
```
shkCTF{sp4rs3_f1l3s_4r3_c001_6cf61f47f6273dfa225ee3366eacb8eb}
```

## Other solutions
After the CTF ends, I notice this is a sparse file (Means physically the file is not 31G)

[Use tail command](https://github.com/TheLeagueOfSociallyDistancedGentlemen/SharkyCTF2020/blob/master/Misc.md)

[Sparse file](https://github.com/LibWTF/ctf_writeups/blob/master/SharkyCTF-2020/MyHugeFile.md)