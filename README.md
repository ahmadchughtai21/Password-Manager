# Password Manager

This is a Django-based web application for managing passwords. It provides features to generate, save, view, delete, and update passwords securely. The application is designed to use encryption for storing passwords and includes functionalities for setting up a master password and managing saved credentials.

## Features

- **Sign Up / Log In**: Secure authentication using a master password.
- **Password Generation**: Create strong, customizable passwords.
- **Save Passwords**: Store passwords securely with encryption.
- **View Passwords**: Display saved passwords (decrypted on the fly).
- **Delete Passwords**: Remove passwords from storage.
- **Change Master Password**: Update the master password for accessing the app.

## Technology Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS (Tailwind CSS)


## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ahmadchughtai21/Password-Manager.git
   cd password-management-app
   ```

2. **Set Up Virtual Environment**

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
      pip install -r requirements.txt
   ```
   
4. **Run Server**

   ```bash
      python manage.py runserver
   ```
   Open your web browser and navigate to http://127.0.0.1:8000 to start using the application.
   

## Usage

- **Sign Up**: Create an account by setting up a master password.
- **Log In**: Access your account using the master password.
- **Generate Password**: Use the form to generate a secure password based on specified criteria.
- **Save Password**: Store your passwords along with the associated website and username.
- **View Passwords**: View a list of saved passwords. Passwords are decrypted when displayed.
- **Delete Password**: Remove passwords from your list.
- **Change Master Password**: Update your master password.

## Notes

- Passwords are encrypted before saving to ensure security.
- Tailwind CSS is used for styling to create a responsive and modern UI.


