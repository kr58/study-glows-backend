class SendSMS:
    # mobile and type are required paramter
    def __init__(self, mobile='', type='', *args, **kwargs):
        self.configure()
        self.mobile = mobile
        self.type = type
        self.args = args
        self.kwargs = kwargs

    def configure(self):
        # TODO: configure the credentials
        pass

    # call this method to send sms
    def send(self):
        if self.mobile == '':
            return False
        if self.type == 'otp':
            otp = self.kwargs.get('OTP')
            if otp:
                return self.OTP(otp)
            return False
        return False

    def send_sms(self, message):
        # TODO: send sms
        print(message)
        return False

    def OTP(self, otp):
        message = f'{otp} is your Study Glow OTP. Do not share it with anyone. Thanks'
        return self.send_sms(message)

