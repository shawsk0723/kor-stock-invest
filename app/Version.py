"""
Version
"""

#
# change if can't be compatible with previoud version
#
Major = 1

#
# change if new function is added
#
Minor = 0

#
# increase if bug is fixed
#
Patch = 0

def getVersion():
    version = f'Ver{Major}.{Minor}.{Patch}'
    return version



"""
Test 
"""

def testVersion():
    print('*** print version ***')
    print(getVersion())

if __name__ == "__main__":
    testVersion()
