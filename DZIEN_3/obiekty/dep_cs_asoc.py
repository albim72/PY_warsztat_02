class Logger:
    def log(self, msg: str) -> None:
        print(msg)


class Service:
    def __init__(self, logger: Logger):
        self.logger = logger   # ASOCJACJA

    def process(self) -> None:
        self.logger.log("Processing...")


def process_once(logger: Logger) -> None:
    logger.log("Processing once")  # ZALEŻNOŚĆ

logger = Logger()
service = Service(logger)
service.process()
process_once(logger)

