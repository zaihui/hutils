# -*- coding: utf-8 -*-
#
# this module provides django database related methods
import json

from django.db import models, transaction

import hutils


def flat_transaction(using: str = None, savepoint: bool = True):
    """ 不嵌套的事务。not nested django transaction

    Examples::

        with flat_transaction():
            with flat_transaction():
                ...
    """
    connection = transaction.get_connection()
    if connection.in_atomic_block:
        context_manager = hutils.EmptyContextManager()
        if callable(using):
            context_manager = context_manager(using)
        return context_manager
    else:
        return transaction.atomic(using, savepoint)


class DynamicField(object):
    """ 动态域，伪 JSONField。a replacement for JSONField.

    Examples::

        class User(models.Model):
            json_data = models.CharField(max_length=1023, default='{}')
            data = DynamicField.make_field('json_data')
            is_developer = DynamicField.make_property('data', 'is_developer', bool, False)
            editor = DynamicField.make_property('data', 'editor', str, 'vim')
    """

    def __init__(self, model: models.Model, field: str):
        """
        :param model: the django model
        :param field: the database field name to store json data
        """
        self._memory_data = {}  # in-memory json data
        self._model = model
        self._field = field
        self._field_value = getattr(self._model, self._field, None)
        if not self._field_value:
            self._set_model_field()
        self._memory_data = json.loads(self._field_value)

    def _set_model_field(self):
        """ set model's json field value """
        self._field_value = hutils.format_json(self._memory_data)
        setattr(self._model, self._field, self._field_value)

    def __setattr__(self, key, value):
        if key.startswith('_'):
            return super(DynamicField, self).__setattr__(key, value)
        if value is None:  # None is default value, don't save
            self._memory_data.pop(key, None)
        else:
            self._memory_data[key] = value
        self._set_model_field()

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __getattr__(self, attr):
        if attr.startswith('_'):
            return super(DynamicField, self).__getattribute__(attr)
        return self._memory_data.get(attr, None)

    def __getitem__(self, item):
        return self.__getattr__(item)

    @classmethod
    def make_field(cls, field_name):
        def _wrap(obj) -> DynamicField:
            private_field_name = '_{}'.format('field_name')
            if not hasattr(obj, private_field_name):
                setattr(obj, private_field_name, cls(obj, field_name))
            return getattr(obj, private_field_name)

        return property(_wrap)

    @classmethod
    def make_property(cls, field_name, property_name, type_wrapper=None, default=None):
        """
        :type field_name: str
        :type property_name: str
        :type type_wrapper: (...) -> T
        :type default: T
        :rtype: T
        """

        def _wrap(value):
            if type_wrapper is not None:
                if value is not None:
                    value = type_wrapper(value)
                else:
                    value = type_wrapper()
            return value

        return property(
            lambda obj: _wrap(getattr(getattr(obj, field_name), property_name, default)),
            lambda obj, value: setattr(getattr(obj, field_name), property_name, _wrap(value)),
        )


class ModelMixin(object):
    """ 集合了一些 Model 的方法。collects some model helper methods.

    Examples::

        class User(models.Model, ModelMixin):
            name = models.CharField()
            age = models.IntegerField()
        User.increase(age=1)
        User.modify(name='kevin')
    """

    def modify(self, extra_updates=(), refresh=False, **fields):
        """ 只修改指定域。specify fields to update.

        Examples::

            user.modify(age=18, extra_updates=('first_name', 'last_name'))
        """
        for field, value in fields.items():
            setattr(self, field, value)
        update_fields = list(extra_updates) + list(fields.keys())
        self.save(update_fields=update_fields)
        if refresh:
            self.refresh_from_db(fields=update_fields)

    def increase(self, extra_updates=(), **fields):
        """ 利用 F() 来修改指定域。increase fields value using F().

        Examples::

            user.increase(points=10)
        """
        fields = {field: models.F(field) + amount for field, amount in fields.items()}
        self.modify(extra_updates=extra_updates, refresh=True, **fields)
