from collections import Counter #імпортуємо функціїю що допомоєе порахувати к-сть логів за їх рівнем
import sys,re #перший модуль для передачі аргументів через командну строку.Дургий для перевірки коректності написання логів

#ф-ція що визначає як виводити опрацьовані дані.
def display_log_counts(counts: dict):
    print(f"{'Рівень логування'} | {'Кількість'}")
    print("-"*28)
    for key, volue in counts.items():
        print(f"{key:<16} | {volue}")
    print('')

 #ф-ція підраховує логи за їх рівнем.
def count_logs_by_level(logs: list) -> dict:
    return Counter([level['level'] for level in logs])
    
#ф-ція повертає логи конкретного рівня, що вказується в другому аргументі під час запиту в командній строці
def filter_logs_by_level(logs: list, level: str) -> list: 
    return [log for log in logs if log['level']==level]
    
#ф-ція обробляє строку логу. Повертає словник де ключами буде дата, час, рівень і місце з відповідними значеннями
def parse_log_line(line: str) -> dict:
    re_for_check=r'\d[\d-]+\s+\d[\d:]+\s+(?:INFO|DEBUG|ERROR|WARNING)\s+[\w\s]+'
    check=re.search(re_for_check,line)
    #Перевірка коректності записів всередині файлу. Якщо записи не вірні буде помилка з підказкою.
    if not check:exit('Помилилка. Невірні дані всередині файлу. Перевірте правильність запису файлів.')
    log=line.strip().split(' ',3)
    return {'date':log[0],'time':log[1],'level':log[2],'message':log[3]}

#ф-ція відкриває файл з логами за директорією вказаною в першому аргументі командної строки. Додає інформацію в список.
def load_logs(file_path: str) -> list:
    logs_list=[]
    with open(file_path,'r',encoding='utf-8') as fh: 
        for line in fh.readlines():
            log_dict_of_el=parse_log_line(line)#на цьому моменті строка логу перетворюється в словник де інф розбита ключами
            logs_list.append(log_dict_of_el)
    return logs_list


def main():
    #перевірка к-сті введених аргументів і вивід підказки що інформує про помилку.
    if len(sys.argv) not in [2,3]:exit("Помилка введення. Введіть шлях до файлу з логами та рівень логування(необов'язково)")
    
    #назначення змінних введеним аргументам з командної строки.
    path=sys.argv[1]
    try:level_input=(sys.argv[2]).upper()
    except IndexError:level_input=None #Якщо другий аргумент відсутній зміна отримає значення None
    
    try:logs=load_logs(path) #запуск файлу за вказаною директорією і вивід підказки якщо директорія не коректна
    except FileNotFoundError: exit('Помилка директорії. Перегляньте правильність написання шляху до файлу з логами')
    
    pos_levels=['INFO','ERROR','DEBUG','WARNING'] #змінна для перевірки коректності вводу другого аргументу

    counts=count_logs_by_level(logs)#Виклик ф-ції що розраховує логі за рівнем.
    display_log_counts(counts)#Викликф-ції що виведе отримані результати.
    
    #Якщо другий аргумент був заданий в командній строці, то ця умова виведе логи за заданим рівнем. 
    # Також якщо аргумент був введений не коректно, поверне повідомлення з підказкою.
    if level_input:
        if level_input not in pos_levels:exit('Аргумент №2 приймає тільки наступні значення:INFO,ERROR,DEBUG,WARNING')
        this_level_logs=filter_logs_by_level(logs,level_input)
        print(f"Деталі логів для рівня '{level_input}'': ")
        for line in this_level_logs:
            print(f'{line['date']} {line['time']} - {line['message']}')
    
if __name__=='__main__':
    main()