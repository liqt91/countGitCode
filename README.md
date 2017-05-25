# countGitCode
按提交者统计git仓库的代码行数，支持忽略文件及文件夹

本质上是git log这个命令，但是看文档该命令只支持文件夹／文件白名单。所以仿照.gitignore文件的形式建立黑名单，将不需要统计的文件或者文件夹填入.gitlogignore文件中即可。


.gitlogignore文件格式

__#*为通配符__


__#项目根目录下的文件夹，不需要/开头，需要/结尾__

.git/

.idea/

\_\_pycache\_\_/

logs/

static/


__#非项目根目录下的文件夹，需要/开头，需要/结尾__

/database*/


__#项目根目录下的文件，不需要/开头，不需要/结尾__

test.py

.gitignore

.gitlogignore

.DS_Store

.python-version


__#非项目根目录下的文件，需要/开头，不需要/结尾__

/bootstrap.css


__#特定后缀的文件，不需要/开头，不需要/结尾__

*.js

*.sql
