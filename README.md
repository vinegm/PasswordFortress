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

By clicking in the pencil a user can edit the information of a account

![image](https://github.com/vinegm/PasswordFortress/assets/117782568/b9f9eceb-cef3-43ab-9687-f59711ecdb1d)

The trash button delete a account, and the eye in the bottom left of each account shows/hides the given account password

![image](https://github.com/vinegm/PasswordFortress/assets/117782568/209c2ca2-7bff-4879-a75b-cc8758900c42)

<h3>Deleting a user</h3>

When trying to delete a user with the trash on the top right, it will as for the user's password as confirmation and then delete the user and accounts linked to him from the database

![image](https://github.com/vinegm/PasswordFortress/assets/117782568/0dde3f54-8948-4a96-acd5-cfb5ecae0873)

<h3>Changing Password</h3>

When trying to change the password of the user it will ask for the old password and new, and a confirmation of the new, it will generate a new cryptographic key and re-cryptograph all the accounts logins and passwords

<h2>Thank You!!</h2>

Thanks for taking a look at my project, if you find a security issue with it, fell free to make a PR, I'll appreciate it!
