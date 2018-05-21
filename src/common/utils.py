from passlib.hash import pbkdf2_sha512
import re
import requests


class Utils(object):

    @staticmethod
    def hash_password(password):
        """
        Hashes the password using pbkdf2_sha512
        :param password: The sha512 password from the login/register form
        :return: A sha512->pbkdf2_sha512 encrypted password
        """

        return pbkdf2_sha512.encrypt(password)


    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checks that the password the user sent matches that of the database.
        The database password is encrypted more than the user's password at this stage.
        :param password: sha512-hashed password
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return: True if password match, False otherwise
        """
        return pbkdf2_sha512.verify(password, hashed_password)

    @staticmethod
    def email_is_valid(email):
        email_address_matche = re.compile('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        return True if email_address_matche.match(email) else False

    @staticmethod
    def send_message(api_url, key, sender, receiver, subject, message):
        return requests.post(
            api_url,
            auth=("api", key),
            data={"from": sender,
                  "to": receiver,
                  "subject": subject,
                  "text": message})

    # You can see a record of this email in your logs: https://app.mailgun.com/app/logs .

    # You can send up to 300 emails/day from this sandbox server.
    # Next, you should add your own domain so you can send 10,000 emails/month for free.
