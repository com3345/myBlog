#!/usr/bin/expect
set timeout 10
spawn pyenv global system
expect eof
spawn fab build 
expect eof
spawn fab deploy
expect "key:"
send "x\r"
expect "password"
send "ddlDLM3345\r"
expect eof
spawn pyenv global 3.5.1
expect eof
