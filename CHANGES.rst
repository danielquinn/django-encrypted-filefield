Changelog
#########

0.3.0
=====

* Dropped support for Django <=2.2 and Python <=3.6
* Fixed `#12`_ (thanks `Pascal Chambon`_ for the report).  This introduces tags
  to the start up checks so you can now skip them if you're doing something
  that negates the need for the warnings/errors they generate.
* We now use `poetry`_ 'cause it's some excellent software.


0.2.2
=====

* Added a dependency on six as it was removed from Django 3.x+.


0.2.1
=====

* Fixed a hard dependency on python-magic==0.4.12 which appears to have been
  removed from PyPI.


0.2.0
=====

* Updated to play nice with Django 2.0 thanks to pull-request `#9`_ from
  `spaceriqui`_.
* At this stage Only Django 1.11+ will be supported, though it may still work
  with older versions as far back as 1.8.


0.1.0
=====

* Initial release


.. _poetry: https://python-poetry.org/

.. _spaceriqui: https://github.com/spaceriqui
.. _Pascal Chambon: https://github.com/pakal

.. _#9: https://github.com/danielquinn/django-encrypted-filefield/pull/9
.. _#12: https://github.com/danielquinn/django-encrypted-filefield/issues/12

