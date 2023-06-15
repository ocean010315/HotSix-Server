from django.contrib.auth.base_user import AbstractBaseUser
import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user) + six.text_type(timestamp))
    
account_activation_token = AccountActivationTokenGenerator()