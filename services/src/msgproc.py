from msgprocObj import msgprocObj

import sys
import os

if sys.version_info[0] < 3:
  raise Exception("Must be using Python 3.6")
if sys.version_info[0] == 3:
  if sys.version_info[1] < 6:
    raise Exception("Must be using at least Python 3.6")

# Command line paramaters are a list of destinations to subscribe to
#  only certain destinations are supported and if an unsupported one is added an error is raised
#  if the same destination is supplied twice an error is raised

msgprocObj.init(env=os.environ, args=sys.argv)

msgprocObj.run()

