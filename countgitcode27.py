# -*- coding: utf-8 -*-
from sys import argv, version
if version < "3":
    from io import open
    from commands import getstatusoutput as runcommand
else:
    from subprocess import getoutput as runcommand
import os
import re
import pypandoc
import datetime



def getRelativePathOfPermittedFilesOrDirs(path):
    # print('current work path:', path)
    length = len(path)
    filesordirs = list()
    for parent, dirnames, filenames in os.walk(path):
        for dirname in dirnames:
            # print(os.path.join(parent[length+1:],dirname))
            # print(dirname)
            # filesordirs.append(os.path.join(parent[length+1:],dirname) + '/')
            pass
        for filename in filenames:
            # print(os.path.join(parent[length+1:],filename))
            filesordirs.append(os.path.join(parent[length+1:],filename))
    # print(filesordirs)
    return filesordirs


def readIgnorelist(file=".gitlogignore"):
    ignoredFileOrDirs = list()
    try:
        with open(file,"rb+") as f:
            while True:
                line = f.readline()
                if line == '':
                    # print("end of file")
                    break
                if line == '\n':
                    # print("blank line")
                    continue
                if line.startswith('#'):
                    # print("comment line")
                    continue
                line = line.replace('*','[^./]*').replace('\\','\\\\')[0:-1]
                # print(line)
                ignoredFileOrDirs.append(line)
                # yield line
            # print(ignoredFileOrDirs)
            return ignoredFileOrDirs
    except IOError as err:
        print("未找到.gitlogignore文件")


def toWord():
    pass


def countGitCode(since=0,until=0):
    paths = list()
    unpermittedPath = list()
    RelativePathOfPermittedFilesOrDirs = getRelativePathOfPermittedFilesOrDirs(os.getcwd())
    ignoredFileOrDirs = readIgnorelist()
    for fd in RelativePathOfPermittedFilesOrDirs:
        flag = True
        for ig in ignoredFileOrDirs:
            # print("filedir:",fd)
            # print("reexp:",ig)
            # print("re.search():",re.search(ig,fd))
            if re.search(ig,fd):
                unpermittedPath.append(fd)
                flag = False
                break
        if flag:
            paths.append(fd)
    # print("unpermittedPath:", unpermittedPath)
    paths = " ".join(paths)
    # paths = " ".join(getRelativePathOfPermittedFilesOrDirs(os.getcwd()))
    command_getauthors = "git log --pretty='%aN' | sort | uniq"
    authors = runcommand(command_getauthors)
    if isinstance(authors,tuple):
        authors = authors[1]
    authors = authors.split('\n')
    template_command_since_until = "git log --author='{0}' --pretty=tformat: --since={1} --until={2}.0am --shortstat -- {3}"
    template_command_since = "git log --author='{0}' --pretty=tformat: --since={1} --shortstat -- {2}"
    template_command = "git log --author='{0}' --shortstat -- {1}"
    template_output = "用户:{0},插入{1}行,删除{2}行,共计新增{3}行"
    template_markdown = """
            |    开始时间{0}    | 结束时间{1}           | Cool  |
            | ------------- |:-------------:| -----:|
            | col 3 is      | right-aligned | $1600 |
            | col 2 is      | centered      |   $12 |
            | zebra stripes | are neat      |    $1 |
            """
    template_html="""<html><head></head><body>{0}</body></html>"""
    template_html_table = """<table border="solid 1px"><tr>
                        <th>开始时间</th><th>{0}</th><th>结束时间</th><th>{1}</th></tr>
                        <tr><th>用户</th><th>插入</th><th>删除</th><th>新增</th></tr>"""
    template_html_table_singleline = """<tr><th>{0}</th><th>{1}</th><th>{2}</th><th>{3}</th></tr>"""
    for author in authors:
        if since == 0 and until == 0:
            command_getcounts = template_command.format(author, paths)
        elif until == 0:
            command_getcounts = template_command_since.format(author, since, paths)
        else:
            command_getcounts = template_command_since_until.format(author, since, until, paths)
        print(command_getcounts)
        insertionsAndDeletions = runcommand(command_getcounts)
        if isinstance(insertionsAndDeletions,tuple):
            insertionsAndDeletions = insertionsAndDeletions[1]
        print(insertionsAndDeletions)
        insertions = re.findall(r", (\d*) insertion[s]?\(\+\)",insertionsAndDeletions)
        total_insertation = sum([int(i) for i in insertions])
        deletions = re.findall(r", (\d*) deletion[s]?\(\-\)",insertionsAndDeletions)
        # print(deletions)
        total_deletion = sum([int(i) for i in deletions])
        different = total_insertation - total_deletion
        # print(template_output.format(author, total_insertation, total_deletion, different))
        html_table_singleline = template_html_table_singleline.format(author, total_insertation, total_deletion, different)
        # print(html_table_singleline)
        template_html_table += html_table_singleline
    table = template_html_table.format(since, until) + "</table>"
    html = template_html.format(table)
    # print(html)
    project_name = re.split(r"[\\/]",os.getcwd())[-1]
    print("project_name:",project_name)
    pypandoc.convert(html, "docx",
                     outputfile= project_name + "-linesCount-" + str(datetime.datetime.now().strftime("%y%m%d%H%M%S")) + ".docx", format="html")

if __name__ == "__main__":
    if len(argv)>3:
        print("too many args.")
        exit()
    elif len(argv) == 1:
        countGitCode()
    elif len(argv) == 2:
        countGitCode(argv[1])
    elif len(argv) == 3:
        countGitCode(argv[1],  argv[2])
