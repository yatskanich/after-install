#!/usr/bin/env python3
# -*-coding: utf-8 -*-
__author__ = 'Yatskanych Oleksandr'
import getpass
import os


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


def make_www_in_home(user_name):
    os.system("mkdir /home/{username}/www/".format(username=user_name))

    os.system('cp /etc/apache2/apache2.conf /home/{username}/apache_conf.tmp'.format(username=user_name))

    with open('/home/{username}/apache_conf.tmp'.format(username=user_name), 'a') as new_apache_conf:
        conf = '<Directory /home/{username}/www/>\n'.format(username=user_name)
        conf += '\tOptions Indexes FollowSymLinks\n'
        conf += '\tAllowOverride All\n'
        conf += '\tRequire all granted\n'
        conf += '</Directory>\n\n'
        conf += 'ServerName localhost'
        new_apache_conf.write(conf)

    os.system('sudo mv /home/{username}/apache_conf.tmp /etc/apache2/apache2.conf'.format(username=user_name))


def change_sql_mode(user_name):
    os.system('cp /etc/mysql/my.cnf /home/{username}/mysql_conf.tmp'.format(username=user_name))

    with open('/home/{username}/mysql_conf.tmp'.format(username=user_name), 'a') as new_mysql_conf:
        data = "[mysqld]\n"
        data += "sql_mode='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'\n"
        data += "skip-character-set-client-handshake\n"
        data += "sort_buffer_size = 256M\n"
        data += "character-set-server = utf8\n"
        data += "init-connect='SET NAMES utf8'\n"
        data += "collation-server=utf8_general_ci\n"
        data += "[client]\n"
        data += "default-character-set=utf8\n"
        data += "[mysqldump]\n"
        data += "default-character-set=utf8"
        new_mysql_conf.write(data)

    os.system('sudo mv /home/{username}/mysql_conf.tmp /etc/mysql/my.cnf'.format(username=user_name))

    os.system('sudo systemctl restart mysql')

if __name__ == "__main__":
    install('commands.txt')

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
    
    mess = 'Make www dir in {username} home folder? (y/n):'.format(username=user_name)
    user_choice = input(mess)
    if user_choice == 'y':
        make_www_in_home(user_name)

    mess = 'Set sql mode to null? (y/n):'
    user_choice = input(mess)
    if user_choice == 'y':
        change_sql_mode(user_name)
