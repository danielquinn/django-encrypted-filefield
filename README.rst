django-encrypted-filefield
==========================

Encrypt uploaded files, store them wherever you like and stream them back
unencrypted.


Why This Exists
---------------

It's increasingly common to use products like S3 to host static files, but
sometimes those static files aren't exactly meant for public eyes.  You might
push some bit of personal information into S3 and then anyone with the URL will
be able to see it.

Sure, the URL may be really hard to guess, but I'm not a fan of "security
through obscurity" so I wrote this to encrypt stuff I push to S3.  Now, only
encrypted blobs are available publicly, but internally, behind a
``MyPermissionRequiredMixin``, the images and documents are loaded magically
and transparently.


How's It Work?
--------------

``EncryptedFileField`` is a thin wrapper around Django's native ``FileField``
that transparently encrypts whatever the user has uploaded and passes off the
now encrypted data to whatever storage engine you've specified.  It also
overrides the ``.url`` value to return a reference to your own view, which does
the decryption for you on the way back to the user.

So where you may have once had this:

.. code:: python

    # my_app/models.py

    class MyModel(models.Model):

        name = models.CharField(max_length=128)
        attachment = models.FileField(upload_to="attachments")
        image = models.ImageField(
            upload_to="images",
            width_field="image_width",
            height_field="image_height"
        )
        image_width = models.PositiveIntegerField()
        image_height = models.PositiveIntegerField()

All you have to do is change the file fields and you've got encrypted files

.. code:: python

    # my_app/models.py

    from django_encrypted_filefield.fields import (
        EncryptedFileField,
        EncryptedImageField
    )

    class MyModel(models.Model):

        name = models.CharField(max_length=128)
        attachment = EncryptedFileField(upload_to="attachments")
        image = EncryptedImageField(
            upload_to="images",
            width_field="image_width",
            height_field="image_height"
        )
        image_width = models.PositiveIntegerField()
        image_height = models.PositiveIntegerField()


    # my_app/views.py

    from django.contrib.auth.mixins import AuthMixin
    from django_encrypted_filefield.views import FetchView


    class MyPermissionRequiredMixin(AuthMixin)
        """
        Your own rules live here
        """
        pass


    class MyFetchView(MyPermissionRequiredMixin, FetchView):
        pass


.. code:: python

    # my_app/urls.py

    from django_encrypted_filefield.constants import FETCH_URL_NAME
    from myapp.views import MyFetchView

    urlpatterns = [
        # ...
        url(
            r"^my-fetch-url/(?P<path>.+)",  # up to you, but path is required
            MyFetchView.as_view(),          # your view, your permissions
            name=FETCH_URL_NAME
        ),
        # ...
    ]


How Do I Configure It?
----------------------

Configuration of the package requires setting three values in either the
environment (recommended) or in your ``settings.py``.  These values are:

* ``DEFF_SALT``: The salt value use for generating the synchronous encryption
* ``DEFF_PASSWORD``: The password value for the same thing
* ``DEFF_FETCH_URL_NAME``: The named URL you intend to use to download the
  files as they're decrypted on-the-fly.

Outside of that, follow the above and you should be good to go.


How Do I Run the Tests?
-----------------------

As this project depends on the setting of three environment variables, you have
to set these for the tests.  Also, the tests are expecting these values, so
don't change them:

.. code:: bash

    $ DEFF_SALT="salt" DEFF_PASSWORD="password" DEFF_FETCH_URL_NAME="fetch" ./manage.py test


Is There a Demo?
----------------

There is!  Just check out the code and run the mini django app in the ``demo``
directory:

.. code:: bash

    $ git clone git@github.com:danielquinn/django-encrypted-filefield.git
    $ cd django-encrypted-filefield/demo
    $ export DEFF_SALT="salt"
    $ export DEFF_PASSWORD="password"
    $ export DEFF_FETCH_URL_NAME="fetch"
    $ ./manage migrate
    $ ./manage.py runserver

...then open http://localhost:8000 and submit two files via the form.  In this
case we're using Django's default_storage, but the same logic should apply to
all storage engines.


Stuff That Doesn't Work
-----------------------

Since the file changes just before it's saved, you can't apply a validator
that acts on the contents of the file.  For example, if you've got a validator
that uses mime-magic to determine the file type, it will always return
``text/plain`` which, unless that's what you're checking for, will break your
validation.  To make things more interesting, Django appears to apply
validation on field values *on every save*, not just when the field has
changed, so even if the validator were to work on the first run, whenever you
would update the object in the admin, your validator will barf in this case.


What's the Status of the Project?
---------------------------------

Stable.  I'm actively using it in a production environment now and have been
for some time without issue.  This isn't a guarantee that it'll work for
everyone in every case of course, but it's enough for me to use that word :-)
