import re
import argparse
import os
from googletrans import Translator
import socket
import socks

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int,
                        help="Specifies the starting line number for processing. Use 1 to begin from the first line.")
    parser.add_argument("--end", type=int,
                        help="Sets the line number at which to stop processing, without including this line itself. Use 1 to indicate the first line.")
    parser.add_argument("--overwrite", action='store_true',
                        help='Enables modification of the original input file. If not set, the output will be saved to a new file with a \'_converted\' suffix.')
    parser.add_argument("--nobackup", action='store_true',
                        help='Prevents the creation of a backup file. This option is only applicable when --overwrite is enabled.')
    parser.add_argument("--translate", action='store_true',
                        help="Appends a Google Translate translation below each original line.")
    parser.add_argument("--socks5", type=int,
                        help="Configures a SOCKS5 proxy for Google Translate, requiring the proxy's port number.")
    parser.add_argument("--at_mark", action="store_true",
                        help=" Processes only the lines that begin with the '@' symbol.")
    parser.add_argument("--keep_indentation", action="store_true",
                        help="Retains the original line's indentation in the output.")
    parser.add_argument("filename", help='The file to be converted.')


    args = parser.parse_args()
    if args.translate:
        if args.socks5:
            socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", args.socks5)
            socket.socket = socks.socksocket
        translator = Translator(service_urls=[
            'translate.google.com',
            'translate.google.com.hk'])

    with open(args.filename, "r", encoding='utf-8') as f_input:
        input_lines = f_input.readlines()
    input_tuple = os.path.splitext(args.filename)
    if args.overwrite:
        if not args.nobackup:
            with open(input_tuple[0] + "_backup" + input_tuple[1], "w", encoding='utf-8') as f_backup:
                f_backup.writelines(input_lines)
        f_output = open(args.filename, "w", encoding='utf-8')
    else:
        f_output = open(input_tuple[0] + "_converted" + input_tuple[1], "w", encoding='utf-8')
    if args.start:
        start = args.start - 1
    else:
        start = 0
    if args.end:
        end = args.end - 1
    else:
        end = len(input_lines)
    f_output.writelines(input_lines[:start])
    for k in range(start, end):
        line = input_lines[k]
        if line[0] != ";":
            f_output.write(line)
        elif line.split()[1][0] == "@":
            f_output.write(line)
            line_split = line.split("\"")
            if args.translate:
                flag = False
                for part in line_split:
                    if not flag:
                        f_output.write(part)
                    else:
                        f_output.write("\"")
                        translation = translator.translate(part, dest='zh-cn')
                        f_output.write(translation.text)
                        f_output.write("\"")
                    flag = not flag
            if args.at_mark:
                flag = False
                if args.keep_indentation:
                    line_split[0] = " " + line_split[0][1:]
                else:
                    line_split[0] = re.sub("^;\\s*", "", line_split[0])
                for part in line_split:
                    if not flag:
                        f_output.write(part)
                    else:
                        f_output.write("\"\"")
                    flag = not flag
            else:
                if args.keep_indentation:
                    f_output.write(" " + line[1:])
                else:
                    f_output.write(re.sub("^;\\s*", "", line))

        elif "<<" in line and ">>" in line:
            f_output.write(line)
            split_pattern = "<<\\s*|\\s*>>"
            split_line = re.split(split_pattern, line)
            spliter = re.findall(split_pattern, line)
            if args.translate:
                flag = False
                for i in range(len(spliter)):
                    if flag:
                        translation = translator.translate(split_line[i], dest='zh-cn')
                        f_output.write(translation.text)
                        f_output.write(spliter[i])
                    else:
                        f_output.write(split_line[i])
                        f_output.write(spliter[i])
                    flag = not flag
                f_output.write(split_line[-1])
            flag = False
            if args.keep_indentation:
                split_line[0] = " " + split_line[0][1:]
            else:
                split_line[0] = re.sub("^;\\s*", "", split_line[0])
            for i in range(len(spliter)):
                if flag:
                    f_output.write(spliter[i])
                else:
                    f_output.write(split_line[i])
                    f_output.write(spliter[i])
                flag = not flag
            f_output.write(split_line[-1])
        else:
            f_output.write(line)
            if line[-1] == "\n":
                line = line[:-1]
                n_flag = True
            keep_pattern = "^;\\s*|\\s*[\\[<].*?[\\]>]\\s*|\\s*:\\s*|\\.{2,}"
            split_line = re.split(keep_pattern, line)
            elements = re.findall(keep_pattern, line)
            if args.translate:
                temp_line = []
                temp_elements = []
                for i in range(len(elements)):
                    temp_line.append(split_line[i])
                    temp_elements.append(elements[i])
                    if elements[i] == '[br]':
                        for j in range(len(temp_line)):
                            if temp_line[j]:
                                translation = translator.translate(temp_line[j], dest='zh-cn')
                                f_output.write(translation.text)
                                f_output.write(temp_elements[j])
                            else:
                                f_output.write(temp_elements[j])
                        temp_line = []
                        temp_elements = []
                    elif "<" not in elements[i] and ">" not in elements[i] and "[" not in elements[i] and "]" not in elements[i] and ":" in elements[i]:
                        for j in range(len(temp_line)):
                            f_output.write(temp_line[j])
                            f_output.write(temp_elements[j])
                        temp_line = []
                        temp_elements = []
                for j in range(len(temp_line)):
                    if temp_line[j]:
                        translation = translator.translate(temp_line[j], dest='zh-cn')
                        f_output.write(translation.text)
                        f_output.write(temp_elements[j])
                    else:
                        f_output.write(temp_elements[j])
                if split_line[len(elements)]:
                    translation = translator.translate(split_line[len(elements)], dest='zh-cn')
                    f_output.write(translation.text)
                if n_flag:
                    f_output.write("\n")
            if args.keep_indentation:
                elements[0] = " " + elements[0][1:]
            else:
                elements[0] = ""
            temp_line = []
            temp_elements = []
            for i in range(len(elements)):
                temp_line.append(split_line[i])
                temp_elements.append(elements[i])
                if elements[i] == '[br]':
                    for j in range(len(temp_line)):    
                        f_output.write(temp_elements[j])
                    temp_line = []
                    temp_elements = []
                elif "<" not in elements[i] and ">" not in elements[i] and "[" not in elements[i] and "]" not in elements[i] and ":" in elements[i]:
                    for j in range(len(temp_line)):
                        f_output.write(temp_line[j])
                        f_output.write(temp_elements[j])
                    temp_line = []
                    temp_elements = []
            for j in range(len(temp_line)):
                f_output.write(temp_elements[j])
            if n_flag:
                f_output.write("\n")
    f_output.writelines(input_lines[max(start, end):])
    f_output.close()