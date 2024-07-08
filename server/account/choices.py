USER_GENDER_MALE = 'male'
USER_GENDER_FEMALE = 'female'

USER_GENDER_CHOICES = (
    (USER_GENDER_MALE, 'آقا'),
    (USER_GENDER_FEMALE, 'خانم'),
)

USER_ROLE_ADMIN = 'admin'
USER_ROLE_MANAGER = 'manager'
USER_ROLE_DOCTOR = 'doctor'
USER_ROLE_PATIENT = 'patient'

USER_ROLE_CHOICES = (
    (USER_ROLE_ADMIN, 'ادمین'),
    (USER_ROLE_MANAGER, 'مدیر'),
    (USER_ROLE_DOCTOR, 'دکتر'),
    (USER_ROLE_PATIENT, 'بیمار'),
)
