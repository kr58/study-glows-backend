from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
import pyotp
import base64


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.email_verified)
        )


def generate_totp(user_id, interval=5):
    secret_key = base64.b32encode(str(user_id).encode())
    min = interval * 60
    totp = pyotp.TOTP(secret_key, interval=min)
    return totp.now()


account_activation_token = AccountActivationTokenGenerator()
