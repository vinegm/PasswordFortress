<h1>PasswordFortress</h1>

PasswordFortress is a desktop password manager made with python, it aims at being secure while simple.

<h2>Installation</h2>

If you wish to run PasswordFortress trough the .exe, you may only keep the "assets" folder and use it as you like, if you want to use it with the .py just download the necessary libraries.

<h2>Used Libraries</h2>

<table>
  <tr>
    <th>Library</th>
    <th>Used For</th>
  </tr>
  <tr>
    <td>Tkinter</td>
    <td>Creating the GUI</td>
  </tr>
  <tr>
    <td>PIL</td>
    <td>Image processing</td>
  </tr>
  <tr>
    <td>Sqlite3</td>
    <td>Storage of data</td>
  </tr>
  <tr>
   <td>bcrypt</td>
   <td>Hashing and KDF</td>
  </tr>
  <tr>
   <td>base64</td>
   <td>Encoding the key</td>
  </tr>
  <tr>
    <td>cryptography.fernet</td>
    <td>Encryption of data</td>
  </tr>
  <tr>
   <td>random/string</td>
   <td>Generating passwords</td>
  </tr>
  <tr>
   <td>re</td>
   <td>Testing password strength</td>
  </tr>
  <tr>
   <td>io</td>
   <td>Buffer for converting images</td>
  </tr>
  <tr>
   <td>datetime</td>
   <td>Getting times</td>
  </tr>
</table>

<h1>The App</h1>

<h2>Login</h2>

This is the login frame, from here you can log in a existing user or register a new one, on loggin in we derive a cryptographic key from the unhashed user password

![image](https://github.com/vinegm/PasswordFortress/assets/117782568/3aca09e2-fd3a-4702-936f-658951cf5d61)

<h2>Register</h2>

In the registration frame you can register a new user to the local database, the password of the user is hashed before being stored for security

![image](https://github.com/vinegm/PasswordFortress/assets/117782568/4dad8b02-4ffa-4767-8158-c9ec21ba18d8)

<h4>Strength Bar:</h4>

the user can see how good his password is with the strength bar, it checks for:

<li>A length of 12 characters;</li>
<li>At least one lower case;</li>
<li>At least one upper case;</li>
<li>At least one digit;</li>
<li>At least one special character.</li>

<h2>Profile</h2>

In the profile frame the current user can:

<li>Change the user password;</li>
<li>Delete the user;</li>
<li>Add a new account;</li>
<li>Change the information of a existing account;</li>
<li>Logoff from the current user.</li>
<br>

***REMOVED***

<h3>Adding and Editing Accounts</h3>

When clicking the plus button on the bottom of the window, a popup comes up asking for information of the account, there you may add a logo, plataform, login and password, the login and password will be encrypted with the derivated key from the login password

![image](https://github.com/vinegm/PasswordFortress/assets/117782568/bbd1d94d-2356-457e-9421-d8d0acdc4150)

If you wish to, you can also generate a password when adding a account

![image](https://github.com/vinegm/PasswordFortress/assets/117782568/2ce5f0ef-78ab-469a-aa9b-958e8d094a93)
