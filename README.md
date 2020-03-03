This is a simple AWD Framework. You should rewrite the attack method in Payload class by yourself.
In your payload, you should upload a shell to a specified host,and return the shell path and password. That's all

# TO DO
1. ~~hot load when modified (finished)~~
2. ~~zoo.php to replace the simple.php => templates/zoo.php.temp~~
3. add unittest
4. trash flow, how to get the path automatic or       => modules/sitemap
5. ~~add keyboard event like ctrl+c to stop the current command execution (finished)~~
6. add wget or curl method to download shell from the ccserver, if "echo | base64 -d >> shell.php" method can not be used.
7. ~~make this framework compatitable to the POCSuite modules(Give UP)~~
8. make good use of all kinds of templates, not limited to zoo.php.temp(in modules/auxiliary/*)
9. add colorful cmd output (finished)~
10. add autocomplete integration  (finished)~


# Usage
```shell
pip install -r requirements.txt

python kittyrun.py
```
To maintain your shell, you should open a new window,and deep into modules/monitor and run `python zookeeper.py`

if you want to send flag to the awd platform,you should rewite the flag function which is in `modules/flag/flag.py`

This is framework is based on requests multitheads, which is blocked.
Considering to refactor it,with aiohttp asyncio, welcome to send issue,requirements. sevenqsh@gmail.com

----
Thank zhangxf55 for contribute a lot.