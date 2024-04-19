from lexer import lexer
from ast_definitions import *


def p_start_command(p):
    '''start_command : START_COMMAND target_flag command_sequence'''
    p[0] = StartCommand(p[1], p[2], p[3])


def p_img_flag(p):
    '''target_flag : FLAG EQUALS IMAGE_PATH'''
    p[0] = TargetFlag(p[1], p[3])


def p_folder_flag(p):
    '''target_flag : FLAG EQUALS FOLDER_PATH'''
    p[0] = TargetFlag(p[1], p[3])


def p_command_sequence(p):
    '''command_sequence : command
                        | pipelined_command'''
    p[0] = p[1]


def p_pipelined_command(p):
    '''pipelined_command : command PIPELINE command_sequence'''
    p[0] = p[1]
    p[0].next_command = p[3]


def p_pipeline_error(p):
    '''pipelined_command : command PIPELINE error'''
    print(
        f"PIPELINE operator must always be followed by a command sequence, but '{p[3].value}' found")
    p[0] = p[1]


def p_command(p):
    '''command : COMMAND'''
    p[0] = Command(p[1])


def p_command_with_flags(p):
    '''command : COMMAND flag_sequence'''
    p[0] = Command(p[1], p[2])


def p_flag(p):
    '''flag : FLAG EQUALS value'''
    p[0] = Flag(p[1], p[3])


def p_flag_sequence(p):
    '''flag_sequence : flag
                     | flag flag_sequence'''
    flags = [p[1]] + (p[2] if len(p) > 2 else [])
    p[0] = flags


def p_value(p):
    '''value : NUMBER
                | IMG_FORMAT
                | IMAGE_PATH'''
    p[0] = p[1]


def p_error(p):
    if p is not None:
        print(f"Syntax error at token '{p.value}'")
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()
