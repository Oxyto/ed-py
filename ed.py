
##
## Small python implementation of ed
##

CMD_MODE = 0
INS_MODE = 1
APP_MODE = 2
CHG_MODE = 3
NB_PRT_MODE = 4
PRT_MODE = 5
EX_MODE = 6


def quit_cmd(_buffer: list[str], _line: str, cursor: int)\
-> tuple[int, int]:
    return cursor, EX_MODE

def change_cmd(_buffer: list[str], _line: str, cursor: int)\
-> tuple[int, int]:
    return cursor, CHG_MODE

def append_cmd(_buffer: list[str], _line: str, cursor: int)\
-> tuple[int, int]:
    return cursor, APP_MODE

def insert_cmd(_buffer: list[str], _line: str, cursor: int)\
-> tuple[int, int]:
    return cursor, INS_MODE

def delete_cmd(buffer: list[str], _line: str, cursor: int)\
-> tuple[int, int]:
    buffer.pop(cursor)
    print(buffer[cursor], end='')
    return cursor, CMD_MODE

def print_cmd(buffer: list[str], _line: str, cursor: int)\
-> tuple[int, int]:
    print(buffer[cursor],end='')
    return cursor, CMD_MODE

def printall_cmd(buffer: list[str], _line: str, cursor: int)\
-> tuple[int, int]:
    for ln in buffer:
        print(ln, end='')
    return cursor, CMD_MODE

def printnb_cmd(buffer: list[str], _line: str, cursor: int)\
-> tuple[int, int]:
    print("%d\t| %s" % (cursor + 1, buffer[cursor]), end='')
    return cursor, CMD_MODE

def printnball_cmd(buffer: list[str], _line: str, cursor: int)\
-> tuple[int, int]:
    for i in range(len(buffer)):
        print("%d\t| %s" % (i + 1, buffer[i]), end='')
    return cursor, CMD_MODE

def write_cmd(buffer: list[str], line: str, cursor: int)\
-> tuple[int, int]:
    with open(line[2:], 'w') as file:
        file.writelines(buffer)
    return cursor, CMD_MODE

def edit_cmd(buffer: list[str], line: str, cursor: int)\
-> tuple[int, int]:
    with open(line[2:], 'r') as file:
        buffer.clear()
        buffer.extend(file.readlines())
    return cursor, CMD_MODE

def lastline_cmd(buffer: list[str], _line: str, _cursor: int)\
-> tuple[int, int]:
    return len(buffer) - 1, CMD_MODE

def error_cmd(_buffer: list[str], _line: str, cursor: int)\
-> tuple[int, int]:
    print("?")
    return cursor, CMD_MODE


OP_LOT = {
    'q': quit_cmd,
    'Q': quit_cmd,
    'c': change_cmd,
    'a': append_cmd,
    'i': insert_cmd,
    'd': delete_cmd,
    'p': print_cmd,
    'P': printall_cmd,
    'n': printnb_cmd,
    'N': printnball_cmd,
    'w': write_cmd,
    'e': edit_cmd,
    '$': lastline_cmd
}

def get_command_input(buffer: list[str], cursor: int, _: int)\
-> tuple[int, int]:
    line: str = input()
    if len(line) < 1:
        print("?")
        return cursor, CMD_MODE
    try:
        if type(int(line)) is int:
            print(buffer[int(line) - 1], end='')
            return int(line) - 1, CMD_MODE
    except (ValueError, IndexError):
        pass
    return OP_LOT.get(line[0], error_cmd)(buffer, line, cursor)

def get_text_input(buffer: list[str], cursor: int, mode: int)\
-> tuple[int, int]:
    line: str = input()
    if mode == APP_MODE:
        cursor += 1
    if mode == CHG_MODE:
        buffer.pop(cursor)
    if len(line) == 1 and line[0] == '.':
        return cursor - 1, CMD_MODE
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
