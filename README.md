honestpreview
-------------
A simple preview site for Honest Appalachia. Visitors can sign up on our mailing list to receive updates by email.

TODO
----
Unsubscribe is working - just have to make some "you've unsubscribed" and "something went wrong" templates.
General fixes:
1. Fix the in-browser e-mail sanity check - it stopped working for some reason
2. Improve the e-mail regex
3. Go through and add error checking/do rigorous testing. Unit tests?
4. Write up notes on blog before you forget everything.

Dependencies
------------
Django 1.3
django-grappelli
tinymce and django_extensions currently included, not required (or even in use right now)
markdown
postman
