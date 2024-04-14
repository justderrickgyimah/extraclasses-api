class ErrorMessageConstants:
    RESPONSE_ERROR_MESSAGE = (
        "An error occurred while processing your request. Please try again later."
    )
    ERROR_MESSAGE = "Unexpected Error Occurred: {}"
    SERVER_ERROR_MESSAGE = (
        "Unexpected Error Occurred in service: {service}: {exception}"
    )


    # Generic
    DATA_FETCH_ERROR = "Error occurred while fetching data from {}."
    UNAUTHORISED_ACCESS = "Unauthorised access to the resource."
    RESOURCE_NOT_FOUND = "Resource not found."
    CONFLICT_ERROR = "Conflict occurred while processing the request. Please refresh and try again."
    
    
    # User
    USER_NOT_FOUND = "User not found."
    USER_ALREADY_EXISTS = "User already exists."
    USER_CREATION_FAILED = "User creation failed."
    USER_UPDATE_FAILED = "User update failed."
    USER_DELETE_FAILED = "User deletion failed."
    USER_READ_FAILED = "User read failed."
    USER_READ_ALL_FAILED = "Failed to read all users."