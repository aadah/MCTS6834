import re


def connect_four_console_source():
    INPUT_RE = re.compile(r'\s*(\d+)\s+(\d+)\s*')
    
    while True:
        inp = raw_input("Enter column and row as two whitespace separated integers: ")
        m = INPUT_RE.match(inp)

        if m:
            col = int(m.group(1))
            row = int(m.group(2))
            break
        else:
            print 'Incorrect format. Syntax: [COLUMN NUMBER] [ROW NUMBER]'
        
    return (col, row)
