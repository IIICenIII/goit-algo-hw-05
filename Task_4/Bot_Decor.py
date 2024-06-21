def input_error(function:function)->function:
    def iner(*args,**kwargs):
        try: return function(*args,**kwargs)
        except ValueError:return 'Enter a argument for the command.'
        except IndexError:return 'Enter the argument for the command.'
        except KeyError: return 'There is no such contact.'
    return iner

def parse_input(user_input:str)->tuple:
    cmd,*args=user_input.split()
    cmd=cmd.strip().casefold()
    return cmd,*args

@input_error
def add_contact(args:list,contacts:dict):
    name,number=args
    if name in contacts:
        return 'The number already exists.'
    else:
        contacts[name]=number
        return 'Contact added.'

@input_error
def change_contact(args:list,contacts:dict):
    name,number=args
    if name not in contacts:return 'There is no such contact.'
    contacts[name]=number
    return 'Contact updated.'

@input_error
def show_phone(args:list,contacts:dict)->str:return contacts[args[0]]

@input_error
def show_all(contacts:dict)->str:
    if not contacts: return 'Contacts list is empty'
    result=''
    for key,value in contacts.items(): result+=f'{key:<10}{value}\n'
    return result.strip()


def main():
    print('Welcome to the assistant bot!')
    contacts={}
    while True:
        user_input=input('Enter a comand here please: ')
        cmd,*args=parse_input(user_input)
        
        if cmd in ['exit','close','quit','q']:
            print('Good bye')
            break
        elif cmd=='hello':
            print('How can I help you?')
        elif cmd=='add':
            print(add_contact(args,contacts))
        elif cmd=='change':
            print(change_contact(args,contacts))
        elif cmd=='all':
            print(show_all(contacts))
        elif cmd=='phone':
            print(show_phone(args,contacts))
        else:
            print('Invalid command')



if __name__=='__main__':
    main()
