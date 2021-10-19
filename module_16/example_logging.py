import logging

MAGIC_NUMBER = 42
logging.basicConfig(
    level=logging.INFO,
    # format='%(name)s %(levelname)s %(asctime)s %(message)s',
)
log = logging.getLogger(__name__)
# log = logging.getLogger('my_log')

log.log(logging.INFO, 'INFO LOG')
log.info('info log')
log.debug(f'Debug log {MAGIC_NUMBER}')
log.warning('Magic number is not 42 %s', MAGIC_NUMBER == 42)
log.error('Error')
log.critical('PANIC')


def main():
    try:
        return MAGIC_NUMBER/0
    except ZeroDivisionError:
        log.exception('MAIN exception')
    return 0


if __name__ == '__main__':
    main()
