"""
AppLogger

Author
- 코드장인
- https://blog.naver.com/shawgibal
"""


from logging.config import dictConfig
import logging



dictConfig({
    'version': 1,
    'formatters': {
        'standard': {
            'format': '[%(levelname)s] %(message)s - [pid:%(process)d - %(asctime)s - %(name)s]',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'mode': 'w',
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file'],
    }
})

def LOG(message):
    logging.debug(message)


"""
test
"""
def testLOG():
    [LOG(f'test log {i}~') for i in range(10)]

if __name__ == '__main__':
    testLOG()