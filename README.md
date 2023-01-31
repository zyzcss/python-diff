# python-diff
python实现jsdiff库中的diff lines算法

源算法见：
https://github.com/kpdecker/jsdiff/blob/master/src/diff/base.js

https://github.com/kpdecker/jsdiff/blob/master/src/diff/line.js

无修改和优化，仅转换为python版本
# jsdiff在线demo
  http://incaseofstairs.com/jsdiff/
# 使用说明
```
a = """A
B
C
A
B
B
A
"""
b = """C
B
A
B
A
C
"""
from pprint import pprint
pprint(Diff(a, b).run())
```
输出
```
[{'added': False, 'count': 1, 'removed': True, 'value': 'A\n'},
 {'added': True, 'count': 1, 'removed': False, 'value': 'C\n'},
 {'count': 1, 'value': 'B\n'},
 {'added': False, 'count': 1, 'removed': True, 'value': 'C\n'},
 {'count': 2, 'value': 'A\nB\n'},
 {'added': False, 'count': 1, 'removed': True, 'value': 'B\n'},
 {'count': 1, 'value': 'A\n'},
 {'added': True, 'count': 1, 'removed': False, 'value': 'C\n'}]
```
