# rex.zhu

import os
from CrazyEye import log

print(os.path.dirname(__file__))



l=log.LogHandler("tst.log")


l.loginfo("我也是测试的")

l.logdebug("我也是debug测试的")