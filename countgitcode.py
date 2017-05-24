import sys
import os
import subprocess
import re


def argvVerification(argv):
    print("since:" + argv[1] + ",until:" + argv[2])


def getRelativePathOfPermittedFilesOrDirs(path):
    print('current work path:', path)
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


def readIgnorelist():
    ignoredFileOrDirs = list()
    with open(".gitlogignore","r+",encoding="utf-8") as f:
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
            line = line.replace('*','[^/]*').replace('\\','\\\\')[0:-1]
            # print(line)
            ignoredFileOrDirs.append(line)
    # print(ignoredFileOrDirs)
    return ignoredFileOrDirs


def countGitCode(since,until):
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
    print("unpermittedPath:", unpermittedPath)
    paths = " ".join(paths)
    # paths = " ".join(getRelativePathOfPermittedFilesOrDirs(os.getcwd()))
    command_getauthors = "git log --pretty='%aN' | sort | uniq"
    authors = subprocess.getoutput(command_getauthors)
    authors = authors.split('\n')
    template_command = "git log --author='{0}' --pretty=tformat: --since={1} --until={2}.0am --shortstat -- {3}"
    template_output = "用户:{0},插入{1}行,删除{2}行,共计新增{3}行"
    for author in authors:
        command_getcounts = template_command.format(author,since,until,paths)
        print(command_getcounts)
        insertionsAndDeletions = subprocess.getoutput(command_getcounts)
        print(insertionsAndDeletions)
        insertions = re.findall(r", (\d*) insertion[s]?\(\+\)",insertionsAndDeletions)
        total_insertation = sum([int(i) for i in insertions])
        deletions = re.findall(r", (\d*) deletion[s]?\(\-\)",insertionsAndDeletions)
        print(deletions)
        total_deletion = sum([int(i) for i in deletions])
        different = total_insertation - total_deletion
        print(template_output.format(author, total_insertation, total_deletion, different))


if __name__ == "__main__":
    argvVerification(sys.argv)
    countGitCode(sys.argv[1],sys.argv[2])
