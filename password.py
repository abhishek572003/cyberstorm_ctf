# Import necessary modules
import os
import django
from django.conf import settings
from django.contrib.auth.hashers import make_password


# Set up Django environment
def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cyberstorm.settings')  # Replace with your project name
    django.setup()


def generate_password_hash(password):
    # Generate the hashed password
    hashed_password = make_password(password)
    return hashed_password


if __name__ == "__main__":
    # Set up Django
    setup_django()

    # Password to hash
    password = "PirateKing123!"

    # Generate the hash
    hashed_password = generate_password_hash(password)
    dbHash = "pbkdf2_sha256$720000$oWa5RXigepH1tVGxUwR6YR$z2jeXRLWZ6+VXmORuW31H4UIogOl+3+tilgmJaOUVE0="

    # Print the generated hash
    print("Generated Hash:", hashed_password)
    print("DB Hash", dbHash)
    print("Generated Hash == DB Hash", hashed_password == dbHash)