import os


def config():
    return {
        "EMAIL_SERVICE_CLIENT_ID": os.getenv("EMAIL_SERVICE_CLIENT_ID", ""),
        "EMAIL_SERVICE_CLIENT_SECRET": os.getenv("EMAIL_SERVICE_CLIENT_SECRET", ""),
        "CHES_AUTH_URL": os.getenv("CHES_AUTH_URL", ""),
        "CHES_EMAIL_URL": os.getenv("CHES_EMAIL_URL", ""),
        "SENDER_EMAIL": os.getenv("SENDER_EMAIL", "ZEVProgramsDoNotReply@gov.bc.ca"),
        "SENDER_NAME": "CleanBC Go Electric",
        "SEND_EMAIL": os.getenv("SEND_EMAIL", "False") == "True",
    }


ZEV_PROGRAMS_EMAIL = "ZEVPrograms@gov.bc.ca"
UNDISCLOSED_RECIPIENTS_EMAIL = "Undisclosed recipients<donotreply@gov.bc.ca>"
