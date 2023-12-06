from abc import ABC

from rich.status import Status

from _internal.console import Logger


class Modules(ABC):

    def __init__(self, *modules):
        self.modules = modules

    def require(self):
        return []

    def name(self):
        raise NotImplementedError("the function `name` is not implemented")

    def main(self, logger: Logger, **kwargs):
        raise NotImplementedError("the function `run` is not implemented")

    def run(self, arguments_module):
        data = {}
        for module in self.modules:
            name = module.name()
            required_module = module.require()
            logger = Logger(str(module))
            module.init()
            extra_arguments = {}
            if len(required_module) > 0:
                for required in required_module:
                    if required not in data:
                        logger.error(f"required module {required} not found")
                        return
                    extra_arguments[required] = data[required]
            if name not in arguments_module.keys():
                arguments_module[name] = {}
            data[name] = module.main(logger, **arguments_module[name], **extra_arguments)
