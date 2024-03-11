class UserExists(Exception):
    def __int__(self, message: str):
        self.message = message
        super().__int__(self.message)
