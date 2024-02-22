# naniconvert
A simple tool for NANINOVEL localization. Use PyInstaller first so you don't need to type *python* every time.

# Requirements
- [googletrans](https://pypi.org/project/googletrans/)==4.0.0rc1
- [PySocks](https://pypi.org/project/PySocks/)

# Usage

- naniconvert.exe [-h] [--start START] [--end END] [--overwrite] [--nobackup] [--translate] [--socks5 SOCKS] [--at_mark] [--keep_indentation] filename

positional arguments:
- filename            The file to be converted.

options:
- -h, --help          show this help message and exit
- --start START       Specifies the starting line number for processing. Use 1 to begin from the first line.
- --end END           Sets the line number at which to stop processing, without including this line itself. Use 1 to indicate the first line.
- --overwrite         Enables modification of the original input file. If not set, the output will be saved to a new file with a '_converted' suffix.
- --nobackup          Prevents the creation of a backup file. This option is only applicable when --overwrite is enabled.
- --translate         Appends a Google Translate translation below each original line.
- --socks5 SOCKS5     Configures a SOCKS5 proxy for Google Translate, requiring the proxy's port number.
- --at_mark           Processes only the lines that begin with the '@' symbol.
- --keep_indentation  Retains the original line's indentation in the output.

  # 用法
- [--start 开始的行数] 从哪一行开始，该行会被在执行时处理，首行为1，可以直接看VS Code的行号
- [--end 不需要处理的部分开始的行数] 就是字面意思，该行不会被处理，也是从1开始计数，同上
- [--overwrite] 是否覆盖原始的输入文件，如果你给了这个选项，那么原始的输入就会直接被覆盖，至于备份文件就看下面的--nobackup部分。如果没有的话，默认生成一个_converted为文件名后缀的新文件
- [--nobackup] 这个选项只有在上面 --overwrite 启用时才会生效。如果没有该选项，在覆盖文件前，会将原始的即将被覆盖的输入文件进行一个备份，备份文件以_backup结尾。如果启用该选项，则不进行备份
- [--translate] 生成参考翻译，使用Google Translate，启用时会消耗一些时间，测试发现速度还算令人满意。由于你懂的原因，使用该功能需要配合下面的选项
- [--socks5 SOCKS5协议的代理端口] 这个你就看你自己的工具是多少了
- [--at_mark] 启用该选项，@符号开头的行会被处理
- [--keep_indentation] 启用该选项，会保留原始文件的缩进格式，具体办法就是将注释行的分号替换为空格
