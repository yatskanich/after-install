#!/usr/bin/env python3
# -*-coding: utf-8 -*-
__author__ = 'yurik'
import os
import getpass


def install(file):
    file_data = open(file)
    line = file_data.readline()
    while line:
        if line.strip() != '' and line[0] != '#':
            os.system(line)
        line = file_data.readline()
    file_data.close()


def ssh_generator():
    email = input('Enter e-mail for ssh-key:')
    if email == '':
        ssh_generator()

    os.system('ssh-keygen -t rsa -C "{0}"'.format(email))
    os.system('xclip -sel clip < ~/.ssh/id_rsa.pub')
    print('Key copy to clipboard...')


def install_soft():
    install('soft.txt')


def change_apache_user(user_name):
    with open('/etc/apache2/envvars', 'r') as f:
        data = f.read()
        new_data = data.replace('www-data', user_name)

    with open('/tmp/env.tmp', 'wt') as n:
        n.write(new_data)

    os.system('sudo mv /tmp/env.tmp /etc/apache2/envvars')

if __name__ == "__main__":
    install('commands.txt')

    with open('/etc/apache2/apache2.conf', 'a') as apache_conf:
        apache_conf.write("ServerName localhost")

    ss = input('Generate SSH key (y/n):')
    if ss == 'y':
        ssh_generator()

    ch = input('Install other soft (y/n):')
    if ch == 'y':
        install_soft()

    user_name = getpass.getuser()
    mess = 'Run apache with current user {0} (y/n):'.format(user_name)

    uc = input(mess)
    if uc == 'y':
        change_apache_user(user_name)
