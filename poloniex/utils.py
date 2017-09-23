import logging
import time


log = logging.getLogger(__name__)


class retry_on_status_code(object):
    def __init__(self, status_codes, max_retries=5, backoff_factor=0.5):
        if type(status_codes) is int:
            status_codes = [status_codes]

        self.status_codes = status_codes
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def should_retry(self, resp):
        return resp.status_code in self.status_codes

    def __call__(self, func):
        def with_retries(*args, **kwargs):
            retries = 0
            backoff = self.backoff_factor

            while True:
                resp = func(*args, **kwargs)
                if not self.should_retry(resp) or retries >= self.max_retries:
                    break

                retries += 1
                log.debug('Received status code %d -- Retrying in %f seconds...',
                          resp.status_code, backoff)
                time.sleep(backoff)
                backoff *= 2

            return resp
        return with_retries
