import re


class RegistrationValidator:
    """
    Clasă care validează datele unui formular de înregistrare.

    Reguli:
    - username: string, 3-20 caractere, începe cu literă, conține doar litere/cifre/underscore,
      nu este deja folosit
    - email: format simplu valid (@, domeniu de exemplu .ro/.com)
    - parola: 6-20 caractere, literă mare, literă mică, cifră, caracter special,
      fără spații, nu este parolă comună
    - varsta: întreg între 18 și 123 
    - accepted_terms: trebuie să fie True
    """

    USERNAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")
    EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
    SPECIAL_CHARACTERS = set("!@#$%^&*()-_=+[]{};:,.?/")

    DEFAULT_COMMON_PASSWORDS = {
        "123456",
        "admin",
        "12345678",
        "123456789",
        "password",
        "Aa123456",
        "1234567890",
        "Pass@123",
        "admin123",
        "1234567",
        "qwerty123",
        "ParolaCeaMaiTare123!",
        "Parola",
        "Parola123"
    }

    def __init__(self, existing_usernames=None, common_passwords=None):
        if existing_usernames is None:
            existing_usernames = set()

        if common_passwords is None:
            common_passwords = self.DEFAULT_COMMON_PASSWORDS

        self.existing_usernames = {
            username.lower() for username in existing_usernames
        }

        self.common_passwords = {
            password.lower() for password in common_passwords
        }

    def is_username_taken(self, username):
        if not isinstance(username, str):
            return False

        return username.lower() in self.existing_usernames

    def get_username_errors(self, username):
        errors = []

        if not isinstance(username, str):
            return ["Username ul trebuie sa fie de forma string"]

        if len(username) < 3:
            errors.append("Username ul trebuie sa aiba cel putin 3 caractere")

        if len(username) > 20:
            errors.append("Username ul poate sa aiba cel mult 20 de caractere")

        if not self.USERNAME_PATTERN.match(username):
            errors.append(
                "Username ul trebuie sa inceapa cu o litera si sa contina numai litere, cifre sau underscore"
            )

        if self.is_username_taken(username):
            errors.append("Username ul este deja luat")

        return errors

    def validate_username(self, username):
        return len(self.get_username_errors(username)) == 0

    def get_email_errors(self, email):
        errors = []

        if not isinstance(email, str):
            return ["Email ul trebuie sa fie de forma string"]

        if " " in email:
            errors.append("Email ul nu poate sa contina spatii")

        if not self.EMAIL_PATTERN.match(email):
            errors.append("Formatul email ului este invalid")

        return errors

    def validate_email(self, email):
        return len(self.get_email_errors(email)) == 0

    def is_common_password(self, password):
        if not isinstance(password, str):
            return False

        return password.lower() in self.common_passwords

    def get_password_errors(self, password):
        errors = []

        if not isinstance(password, str):
            return ["Parola trebuie sa fie de forma string"]

        if len(password) < 6:
            errors.append("Parola trebuie sa aiba cel putin 6 caractere")

        if len(password) > 20:
            errors.append("Parola poate sa aiba cel mult 20 de caractere")

        if any(character.isspace() for character in password):
            errors.append("Parola nu poate sa contina spatii")

        if not any(character.islower() for character in password):
            errors.append("Parola trebuie sa contina cel putin o litera mica")

        if not any(character.isupper() for character in password):
            errors.append("Parola trebuie sa contina cel putin o litera mare")

        if not any(character.isdigit() for character in password):
            errors.append("Parola trebuie sa contina cel putin o cifra")

        if not any(character in self.SPECIAL_CHARACTERS for character in password):
            errors.append("Parola trebuie sa contina cel putin un caracter special")

        if self.is_common_password(password):
            errors.append("Parola este prea comuna")

        return errors

    def validate_password(self, password):
        return len(self.get_password_errors(password)) == 0

    def password_strength_score(self, password):
        """
        Returnează un scor între 0 și 5.

        0 = parolă foarte slabă / input invalid
        5 = parolă puternică
        """

        if not isinstance(password, str):
            return 0

        score = 0

        if len(password) >= 8:
            score += 1

        if len(password) >= 12:
            score += 1

        if any(character.islower() for character in password) and any(
            character.isupper() for character in password
        ):
            score += 1

        if any(character.isdigit() for character in password):
            score += 1

        if any(character in self.SPECIAL_CHARACTERS for character in password):
            score += 1

        if self.is_common_password(password):
            score = min(score, 1)

        return score

    def password_strength_label(self, password):
        score = self.password_strength_score(password)

        if score <= 1:
            return "slaba"

        if score <= 3:
            return "medie"

        return "puternica"

    def get_age_errors(self, age):
        errors = []

        if isinstance(age, bool) or not isinstance(age, int):
            return ["Varsta trebuie sa fie un numar intreg"]

        if age < 18:
            errors.append("Varsta minima este de 18")

        if age > 123:
            errors.append("Varsta maxima este de 123")

        return errors

    def validate_age(self, age):
        return len(self.get_age_errors(age)) == 0

    def validate_terms(self, accepted_terms):
        return accepted_terms is True

    def get_registration_errors(
        self, username, email, password, age, accepted_terms
    ):
        errors = {}

        username_errors = self.get_username_errors(username)
        if username_errors:
            errors["username"] = username_errors

        email_errors = self.get_email_errors(email)
        if email_errors:
            errors["email"] = email_errors

        password_errors = self.get_password_errors(password)
        if password_errors:
            errors["password"] = password_errors

        age_errors = self.get_age_errors(age)
        if age_errors:
            errors["age"] = age_errors

        if not self.validate_terms(accepted_terms):
            errors["accepted_terms"] = ["Termeni trebuie sa fie acceptati"]

        return errors

    def validate_registration(
        self, username, email, password, age, accepted_terms
    ):
        return len(
            self.get_registration_errors(
                username, email, password, age, accepted_terms
            )
        ) == 0