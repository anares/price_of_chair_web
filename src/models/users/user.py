import uuid
from src.common.database import Database
from src.common.myutils import MyUtils
import src.models.users.errors as UserErrors
from src.models.alerts.alert import Alert
import src.models.users.constants as UserConstants


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies that an e-mail/password combo (as sent by the site forms) is valid or not.
        :param email: The user email
        :param password: A sha512 hashed password
        :return:True if valid, False otherwise
        """
        user_data = Database.find_one(UserConstants.COLLECTION, {'email': email})  # Password in sha512 -> pbkdf2_sha512
        if user_data is None:
            # Tell the user that their e-mail doesn't exist
            raise UserErrors.UserNotExistsError("Your user does not exist")
        if not MyUtils.check_hashed_password(password, user_data['password']):
            # Tell the user that their password is wrong
            raise UserErrors.IncorrectPasswordError("The password for this user is wrong")
        return True


    @staticmethod
    def register_user(email, password):
        """
        This method registers an user, using email and password
        The password already comes as hashed as sha512.
        :param email: user's e-mail
        :param password: sha512-hashed password
        :return True, if regstered successfully, or False otherwise (exception can also be rised)
        """
        user_data = Database.find_one(UserConstants.COLLECTION, {'email':email})
        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError('The user with this e-mail is already registered')
        if not MyUtils.email_is_valid(email):
            raise UserErrors.InvalidEmailError('The e-mail does not have a valid format')

        User(email, MyUtils.hash_password(password)).save_to_db()
        return True

    def save_to_db(self):
        Database.insert(UserConstants.COLLECTION, self.json())

    def json(self):
        return {
            '_id' : self._id,
            'email' : self.email,
            'password' : self.password
        }

    @classmethod
    def find_by_email(cls, email):
        return cls(**Database.find_one(UserConstants.COLLECTION, {'email': email}))

    def get_alerts(self):
        return Alert.find_by_user_email(self.email)