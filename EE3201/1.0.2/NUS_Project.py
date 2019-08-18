import sys
import os
import csv
from collections import defaultdict
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import datetime
from googletrans import Translator
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import time

monty_data = defaultdict(list)
PC_path = "D:/abc.csv"
PC_download_tem_path= "D:/download.csv"
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication.
drive = GoogleDrive(gauth)

user =''


def whatsapp_send(data):
    account_sid = 'AC6173c8edc8d417740113527fb69a9712'
    auth_token = 'e65fbc3c8b64c46bf3fd874ecd2c3719'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                              body=data,
                              from_='whatsapp:+14155238886',
                              to='whatsapp:+6588764892'
                          )
    # if message.sid != None : print('Done')


def login():
    while(1):
        dict = {'Xinghe': '1', 'Shulin': '2', 'Ayi': '3'}

        input_account =str(input('Please input your account:  '))
        password= dict.get(str(input_account))

        if password != None:
            input_password = str(input('Please input your password:  '))

            if input_password == password:
                return input_account


class translate:
    def __init__(self,language):
        if language == 'cn': language = 'zh-cn'
        self.language = language

    def translater_result(self,data):
        translator = Translator()
        translations = translator.translate(data, dest=self.language)

        for translation in translations:
            # print(translation.origin, ' -> ', translation.text)
            return str(translation.text)



class google_drive():

    def __init__(self,user):
        self.user =user

        while(1):
            selection = input('>>>please enter your action  ')
            if selection  == 'upload':
                self.upload()
            elif selection == 'list':
                self.get_list()
            elif selection == 'delete':
                self.delete()
            elif selection == 'download':
                self.download()
            elif selection == 'exit':
                break
            else:
                print('I can not identify your input')


    def upload(self,user):

        print('uploading to Google drive .......')
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file1 = drive.CreateFile({'title': str(user) + '_Monty_record_'+ str(date) + '.csv'})
        file1.SetContentFile(PC_path)
        file1.Upload()
        print('Uploaded file with title {}'.format(file1.get('title')))


    def get_list(self):

        counter=0
        file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        print('--------------------------------------------------')
        for file1 in file_list:

            text = file1['title']
            text_counter = text.find(self.user)
            if text_counter != 0: continue
            print('S/N: %s,title: %s,id: %s ' % (counter,file1['title'],file1['id']))
            counter=counter+1
        if counter == 0:

            print('Nothing')
            print('--------------------------------------------------')
            return False
        print('--------------------------------------------------')

    def delete(self):

        status = self.get_list()
        if status == False:
            print('You have nothing can be deleted\n')
            return

        counter = 0
        file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        item_no = 'a'

        number = input('>>>Please enter the S/N to delete the file   ')

        for file1 in file_list:

            text = file1['title']
            text_counter = text.find(self.user)
            if text_counter != 0: continue
            if str(counter) == str(number):
                item_no = file1['id']
                break
            counter = counter + 1

        if item_no != 'a' :         print('Delete item is :' + str(item_no) + ' (file id)')

        file1 = drive.CreateFile({'id': item_no})
        try:
          file1.Trash()
        except Exception as e:
            print(e)

    def download(self):

        self.get_list()
        number = input('Please enter the S/N to delete the file   ')
        counter = 0
        file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()



        for file1 in file_list:
            # print('title: %s, id: %s, S/N: %s' % (file1['title'], file1['id'],counter))
            if str(counter) == str(number):
                item_no = file1['id']
                break
            counter = counter + 1

        downloaded = drive.CreateFile({'id': item_no})  # replace the id with id of file you want to access
        downloaded.GetContentFile(PC_download_tem_path)
        print('Done')

        StorageManager(PC_download_tem_path).load_data_to_sys()
        Todo.print_list()

class UserInterface:

    def show_greeting(self):
        welcome = """
*******************************************************************************************
*  __          __  _                            _          __  __             _           *
*  \ \        / / | |                          | |        |  \/  |           | |          *
*   \ \  /\  / /__| | ___ ___  _ __ ___   ___  | |_ ___   | \  / | ___  _ __ | |_ _   _   *
*    \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \  | |\/| |/ _ \| '_ \| __| | | |  *
*     \  /\  /  __/ | (_| (_) | | | | | |  __/ | || (_) | | |  | | (_) | | | | |_| |_| |  *
*      \/  \/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/  |_|  |_|\___/|_| |_|\__|\__, |  *
*                                                                                  __/ |  *
*                                                                                 |___/   *
******************************************************************************************* """

        print(welcome.strip(), '\n')

    def display(self, data):
        print(data)

class StorageManager():

    def __init__(self, path):
        self.path = path

    def save_data_to_csv(self, data):
        # path = "/home/runner/Monty7.csv"
        with open(self.path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            for list in data:
                csv_writer.writerow(data[list])
        print("Saving ->Done")
        print("Showing file content")
        print("--------------------------------------------------")

        csv_reader = csv.reader(open(self.path))
        for line in csv_reader:
            print(line)
        print("--------------------------------------------------")

    def load_data_to_sys(self):

        csv_reader = csv.reader(open(self.path))
        monty_data.clear()
        counter = 1
        for line in csv_reader:
            monty_data[str(counter)].append(line[0])
            monty_data[str(counter)].append(line[1])
            monty_data[str(counter)].append(line[2])
            monty_data[str(counter)].append(line[3])
            counter = counter+1
        print("Loading ->Done\n")


class TaskManager(StorageManager):
    def __init__(self, path):
        self.path = path


class Todo :

    def add(task):
        for i in range(1, 9999):
            if str(i) not in monty_data.keys():
                # monty_data[str(i)].append("✗")
                monty_data[str(i)].append(False)
                monty_data[str(i)].append(i)
                monty_data[str(i)].append(task)
                monty_data[str(i)].append('-')
                break



    def print_list():

        item_send_to_whatsapp = ''

        print('>>> Here is the list of tasks:')
        print('==================================================')
        print('STATUS | INDEX | DESCRIPTION | DEADLINE')
        print('--------------------------------------------------')


        for line in monty_data:
            if str(monty_data[line][0]) == "True":
                print(str('✓').ljust(4, ' ') + '   |  ' + str(line).ljust(3, ' ') + ' |  ' + str(
                    monty_data[line][2].ljust(11, ' ')) + ' | ' + monty_data[line][3])

            else:
                print(str('✗').ljust(4, ' ') + '   |  ' + str(line).ljust(3, ' ') + ' |  ' + str(
                    monty_data[line][2].ljust(11, ' ')) + ' | ' + monty_data[line][3])
        print('--------------------------------------------------')





    def delete(command):
        try:
            delete_number = command[7:]
            if int(delete_number) > len(monty_data) or int(delete_number) <= 0:
                print('>>> SORRY, I could not perform that command. Due to out of data range ')

            for line in monty_data:
                if line == delete_number:
                    monty_data.pop(line)
                    print(">>> Task deleted from the list")
                    break
                else:
                    continue
        except ValueError:
            print('>>> SORRY, I could not perform that command. Problem: ' + command[7:] + ' is not a number')


    def is_exit_confirmed():
        print('>>> Are you sure? y/n')
        response = input()
        return response == 'y'

    def done(command):
        try:
            done_number = int(command[5:])
            if isinstance(done_number, int):
                if done_number <= len(monty_data):
                    if done_number != 0:
                        # monty_data[str(done_number)][0] = '✓'
                        monty_data[str(done_number)][0] = True
                    else:
                        print('>>>  SORRY, I could not perform that command. Problem: Index must be greater than 0')
                else:
                    print('>>> SORRY, I could not perform that command. Problem: No item at index ' + str(done_number))

        except ValueError:
            print('>>> SORRY, I could not perform that command. Problem: ' + command[5:] + ' is not a number')
        except IndexError:
            print('>>> SORRY, I could not find the tesk. Tesk S/N: ' + command[5:])

    def pending(command):
        try:
            done_number = int(command[8:])
            if isinstance(done_number, int):
                if done_number <= len(monty_data):
                    if done_number != 0:
                        # monty_data[str(done_number)][0] = '✓'
                        monty_data[str(done_number)][0] = False
                    else:
                        print('>>>  SORRY, I could not perform that command. Problem: Index must be greater than 0')
                else:
                    print('>>> SORRY, I could not perform that command. Problem: No item at index ' + str(done_number))
        except ValueError:
            print('>>> SORRY, I could not perform that command. Problem: ' + str(done_number) + ' is not a number')
        except IndexError:
            print('>>> SORRY, I could not find the tesk. Tesk S/N: ' + str(done_number))

    def deadline(command):
        try:
            key = command[9:int(command.index("by:") - 1)]
            status = False
            deadline_date = command[int(command.index("by:") + 3):]

            for line in monty_data:
                if monty_data[line][2] == key:
                    monty_data[line][3] = deadline_date
                    status = True
                else:
                    continue

            if status != True:
                print("Can not found the task!")
        except ValueError:
            print("command format is invalid,please follow  deadline<space><task><space>by:<date>  ")

    def help():
        help = """
==================================================
Monty can understand the following commands:

  Todo :Todo DESCRIPTION 
    Adds a task to the list
    Example: Todo read book
  done INDEX:
    Marks the task at INDEX as 'done'(✓)
    Example: done 1
  pending INDEX:
   make item as pending (✗)
  exit:
    Exits the application
  help:
    Shows the help information
  list:
    Lists the tasks in the list
  save:
    Aave current list to google drive , PC_temp file , and push to your whatsapps
  translate:
    translate description to any google translator supported  language 

  google drive:
    enter google drive moulde
      list:
        get list of content under user account
      delete:
        delete any file under user account
      download:
        download any file under user account
--------------------------------------------------  """
        print(help)

    def translate_list():

        languague_short_form = input('please enter the short form of language  :')
        translater = translate(languague_short_form)

        print('>>> Here is the list of tasks:')
        print('==================================================')
        print('STATUS | INDEX | DESCRIPTION | DEADLINE')
        print('--------------------------------------------------')

        for line in monty_data:
            if str(monty_data[line][0]) == "True":
                translated_data = str(translater.translater_result([monty_data[line][2]]))
                print(str('✓').ljust(4, ' ') + '   |  ' + str(line).ljust(3, ' ') + ' |  ' + translated_data.ljust(11, ' ') + ' | ' + monty_data[line][3])
            else:
                translated_data =  str(translater.translater_result([monty_data[line][2]]))
                print(str('✗').ljust(4, ' ') + '   |  ' +  str(line).ljust(3, ' ') + ' |  ' + translated_data.ljust(11, ' ')  + ' | ' + monty_data[line][3])
        print('--------------------------------------------------')


def execute_command(command,user):
    if command == '':
        return
    elif command == 'exit':
        if Todo.is_exit_confirmed():
            print('>>> Bye!')
            sys.exit()

    elif command[0:4] == 'todo' and command[5:] != '':
        Todo.add(command[5:])


    elif command == 'list':
        if len(monty_data) == 0:
            print('>>> Nothing to list')
        else:
            Todo.print_list()

    elif command == 'load':
        # storage = StorageManager('/home/runner/Monty7.csv')
        storage = StorageManager(PC_path)
        storage.load_data_to_sys()




    elif command == 'save':
        # storage = StorageManager('/home/runner/Monty7.csv')
        storage = StorageManager(PC_path)
        storage.save_data_to_csv(monty_data)

        ok= google_drive.upload(monty_data,user)

        'below code will send list to Xinghe s whatsapp'
        item_send_to_whatsapp= ""
        for line in monty_data:
            if str(monty_data[line][0]) == "True":

                item_send_to_whatsapp = item_send_to_whatsapp + (str('✓').ljust(4, ' ') + '   |  ' + str(line).ljust(3, ' ') + ' |  ' + str(
                    monty_data[line][2].ljust(11, ' ')) + ' | ' + monty_data[line][3]) +'\n'
            else:
                item_send_to_whatsapp = item_send_to_whatsapp + (str('✗').ljust(4, ' ') + '   |  ' + str(line).ljust(3, ' ') + ' |  ' + str(
                    monty_data[line][2].ljust(11, ' ')) + ' | ' + monty_data[line][3]) + '\n'

        print('Pushing to your phone.......')
        whatsapp_send('>>> Here is the list of tasks:\n' +
            ('STATUS | INDEX | DESCRIPTION | DEADLINE\n'
                      '----------------------------------\n'
                      ) + item_send_to_whatsapp + '-----------------------------------')
        print('Check you phone please: )')


    elif command[0:6] == 'delete':
        Todo.delete(command)

    elif command[0:12] == 'google drive':
        ok =google_drive(user)


    elif command[0:4] == 'done':
        Todo.done(command)


    elif command[0:7] == 'pending':
        Todo.pending(command)

    elif command[0:8] == 'deadline':
        Todo.deadline(command)


    elif command[0:9] == 'translate':

        # if len(monty_data) == 0:
        # #     print('>>> Nothing to list')
        # # else:
            Todo.translate_list()

    elif command == 'help':
        Todo.help()

    else:
        print('>>> SORRY, I could not perform that command. Problem: Command not recognized')

def read_command():


    answer = input('>>> What can I do for you?\n')
    answer = answer.strip(" ").lower()
    return answer


def main():

    ui = UserInterface()
    ui.show_greeting()

    # user = login()
    user ='Xinghe'

    while True:
        command = read_command()
        execute_command(command,user)

def userLogin():

    ui = UserInterface()
    ui.show_greeting()

    # user = 'Shulin'
    print('>>> Hi ' + user)


def getInputFromOtherFunction(_content):

    userLogin()

    while True:
        print('>>> What can I do for you?\n')
        command = read_command(_content)
        execute_command(command,user)


if __name__== '__main__':
    main()

    ok = google_translate(['what your name'], 'cn').translater()




