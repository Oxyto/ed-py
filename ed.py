##
## ed.py : a small python implementation of ed
##

CMD_MODE = 0
INS_MODE = 1
APP_MODE = 2
CHG_MODE = 3
NB_PRT_MODE = 4
PRT_MODE = 5
EX_MODE = 6

def get_command_input(buffer: list[str], cursor: int, _: int)\
-> tuple[int, int]:
    line: str = input()
    if len(line) < 1:
        print("?")
        return cursor, CMD_MODE
    try:
        if line[0] == 'Q' or line[0] == 'q':
            return cursor, EX_MODE
        if line[0] == 'c':
            return cursor, CHG_MODE
        if line[0] == 'a':
            return cursor, APP_MODE
        if line[0] == 'i':
            return cursor, INS_MODE
        if line[0] == 'd':
            buffer.pop(cursor)
            return cursor, CMD_MODE
        if line[0] == 'p':
            print(buffer[cursor],end='')
            return cursor, CMD_MODE
        if line[0] == 'P':
            for line in buffer:
                print(line, end='')
            return cursor, CMD_MODE
        if line[0] == 'n':
            print("%d\t| %s" % (cursor + 1, buffer[cursor]), end='')
            return cursor, CMD_MODE
        if line[0] == 'N':
            for i in range(len(buffer)):
                print("%d\t| %s" % (i + 1, buffer[i]), end='')
            return cursor, CMD_MODE
        if line[0] == 'w':
            with open(line[2:], 'w') as file:
                file.writelines(buffer)
            return cursor, CMD_MODE
        if line[0] == 'e':
            with open(line[2:], 'r') as file:
                buffer.clear()
                buffer.extend(file.readlines())
            return cursor, CMD_MODE
        if type(int(line)) is int:
            return int(line) - 1, CMD_MODE
    except (ValueError, IndexError):
        pass
    print("?")
    return cursor, CMD_MODE

def get_text_input(buffer: list[str], cursor: int, mode: int)\
-> tuple[int, int]:
    line: str = input()
    if mode == APP_MODE:
        cursor += 1
    if mode == CHG_MODE:
        buffer.pop(cursor)
    if len(line) == 1 and line[0] == '.':
        return cursor, CMD_MODE
    buffer.insert(cursor, line + '\n')
    return cursor + 1, INS_MODE

def main() -> int:
    buffer: list[str] = []
    mode: int = CMD_MODE
    cursor: int = 0
    while True:
        if mode == CMD_MODE:
            cursor, mode = get_command_input(buffer, cursor, mode)
        if mode in (INS_MODE, APP_MODE, CHG_MODE):
            cursor, mode = get_text_input(buffer, cursor, mode)
        if mode == EX_MODE:
            break
    return 0

if __name__ == '__main__':
    main()
