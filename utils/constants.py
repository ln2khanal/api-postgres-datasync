# Base url
API_BASE_URL = "http://apiserver.example.com/api"

# Api url templates
PATIENT_URL = f"{API_BASE_URL}/client/query"
PRESCRIPTION_URL = f"{API_BASE_URL}/script/query"
STOCK_URL = f"{API_BASE_URL}/stock/query"
LOGIN_URL = f"{API_BASE_URL}/login/user"
ORDER_PUSH_URL = f"{API_BASE_URL}/storequeue/post"

# status success code
SUCCESS_STATUS_CODE = 200

# only the known mappings will be utilized.
# The rest of the fields will be stored in the notes field.
# This is to ensure that the API clients are not broken.
SUPPORTED_TABLE_MAPPINGS = {
    "patient": {
        "active": "verification_status",
        "clientNo": "patient_code",
        "firstName": "first_name",
        "surname": "last_name",
        "email": "email",
        "phoneNumber": "phone",
        "sex": "sex",
        "dateOfBirth": "dob",
        "lastModified": "updated_at",
        "created": "created_at",
        "homeAddress": "address1",
        "homePostCode": "zip_code",
        "homeSuburb": "address2",
    },
    "prescriptions": {
        "prescription": "prescription",
    },
}

TEMPORARY_DATA_DIR = "/app/data"
