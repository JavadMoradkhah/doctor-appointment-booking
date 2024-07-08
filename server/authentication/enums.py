from enum import Enum
from account import choices


class UrlTargetRole(Enum):
    PATIENT = choices.USER_ROLE_PATIENT
    DOCTOR = choices.USER_ROLE_DOCTOR
    MANAGER = choices.USER_ROLE_MANAGER
