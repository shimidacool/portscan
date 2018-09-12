#!/usr/bin/python
# -*- coding: UTF-8 -*-

import string   # 必须调用 maketrans 函数。

intab = "aeiou"
outtab = "12345"
trantab = string.maketrans(intab, outtab)

str = "this is string example....wow!!!";
print str.translate(trantab);
