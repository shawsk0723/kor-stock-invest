"""
AppLogger

Author
- 코드장인
- https://blog.naver.com/shawgibal
"""


from logging.config import dictConfig
import logging

CONSOLE_PRINT = True

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(message)s',
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'default',
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['file']
    }
})

def LOG(message):
    logging.debug(message)
    if CONSOLE_PRINT:
        print(message)

"""
test
"""
def testLOG():
    [LOG(f'test log {i}~') for i in range(10)]

if __name__ == '__main__':
    testLOG()