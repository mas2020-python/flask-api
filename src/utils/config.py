import logging


class APIServer:
    def __init__(self):
        self.config: dict = {}
        # Get the logger specified in the file
        self.logger = logging.getLogger("sampleLogger")

    # def send_error_back(self, resp, e: Exception, status=falcon.HTTP_400):
    #     self.logger.error(f"Houston, we have a problem: {e.__str__()}")
    #     resp.body = json.dumps(e.__str__(), indent=4, sort_keys=True)
    #     resp.status = status


# Global constants
API_SRV = APIServer()
