from enum import Enum


class AppExceptionCode(Enum):
    '''
    This is the code exception
    '''

    FILE_NOT_FOUND = 1001, 'File Not Found. '
    FOLDER_NOT_FOUND = 1002, 'Folder Not Found. '
    IO_ACCESS_DENIED = 1003, 'Cannot Access Folder/File. '
    EMPTY_PARAMETERS = 1004, 'Empty Parameters. '

    FAILED_QUERY_PROCESS = 2001, 'Unable to process query. '
    CANNOT_DELETE = 2002, 'Cannot perform delete. '
    CANNOT_SAVE = 2003, 'Cannot Save Data. '
    CANNOT_UPDATE = 2004, 'Cannot Update data. '
    NOT_FOUND_ERROR = 2005, 'Data is not Found. '

    POLICY_VIOLATION = 3001, 'Cannot Process, Constraints reached. '
    FILE_NOT_ALLOWED = 3002, 'File Type is not allowed. '
    ILLEGAL_ARGUMENT = 3003, 'Illegal Argument. '

    INVALID_FORMAT = 4001, 'Format Invalid, unable to process any further. '
    UNKNOWN_VALUE = 4002, 'Unknown Value. '

    def __str__(self):
        return 'AppError-' + str(self.value[0]) + ': ' + self.value[1]

    def get_message(self):
        return str(self.value[1])

    def get_code(self):
        return str(self.value[0])

