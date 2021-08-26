class AppException(Exception):

    def __init__(self, exception_code, errors=''):
        # Call the base class constructor with the parameters it needs
        super().__init__(str(exception_code) + errors)
        self.exception = exception_code
        self.errors = errors

    def get_code(self):
        return self.exception.get_code()

    def get_message(self):
        return self.exception.get_message()
