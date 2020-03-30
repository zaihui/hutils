.. hutils documentation master file, created by
   sphinx-quickstart on Thu Sep  6 19:03:31 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

HUtils, a charming util-library
===============================

本项目包含了一些 Web 后端项目中比较好用的基类函数，
包括了类型转换、入参获取、验证函数和各种方便的小工具函数。

具体的方法请参见下方详情。

.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. module:: hutils


Classes
-------

Tuple Enum
^^^^^^^^^^
.. autoclass:: TupleEnum
   :members:

Empty Context Manager
^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: EmptyContextManager
   :members:


Data Types
----------

Bytes to String
^^^^^^^^^^^^^^^
.. autofunction:: bytes_to_str

JSON Encoder
^^^^^^^^^^^^
.. autoclass:: JSONEncoder

Format JSON
^^^^^^^^^^^
.. autofunction:: format_json

Get Dict Data
^^^^^^^^^^^^^
.. autofunction:: get_data

Merge Dicts
^^^^^^^^^^^
.. autofunction:: merge_dicts

Normalize Decimal
^^^^^^^^^^^^^^^^^
.. autofunction:: normalize

Quantize Decimal
^^^^^^^^^^^^^^^^
.. autofunction:: quantize


Decorators
----------

Object Cache
^^^^^^^^^^^^
.. autofunction:: obj_cache

Ignore Error
^^^^^^^^^^^^
.. autofunction:: ignore_error

Catches Error
^^^^^^^^^^^^^
.. autofunction:: catches

Mutes Error
^^^^^^^^^^^
.. autofunction:: mutes


Schemas
-------

Get Offset/Limit
^^^^^^^^^^^^^^^^
.. autofunction:: get_offset_and_limit

Get Start/End Time
^^^^^^^^^^^^^^^^^^
.. autofunction:: get_start_and_end_time


Shortcuts
---------

Combine Datetime
^^^^^^^^^^^^^^^^
.. autofunction:: datetime_combine

Get UID
^^^^^^^
.. autofunction:: get_uid

Get First of List
^^^^^^^^^^^^^^^^^
.. autofunction:: list_first

Get Index of List
^^^^^^^^^^^^^^^^^
.. autofunction:: list_get

Mock Lambda
^^^^^^^^^^^
.. autofunction:: mock_lambda


Validators
----------

Validate Chinese Phone
^^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: is_chinese_phone

Validate Integer
^^^^^^^^^^^^^^^^
.. autofunction:: is_int

Validate UUID
^^^^^^^^^^^^^
.. autofunction:: is_uuid
