# -*- coding: utf-8 -*-
#
# this module provides django database related methods
import json

from django.db import models
from django.db.models import Case, FilteredRelation, IntegerField, Q, Sum, When

import hutils


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

    # noinspection PyUnresolvedReferences
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


class QuerySetMixin:
    """ 减少代码重复，一个地方写，两个地方用 :) """

    def filter_related(self, name: str, *, include_all=False, **conditions) -> 'HQuerySet':
        """ 利用 FilteredRelation 优化 Query 的方法
        官方文档参见: https://docs.djangoproject.com/en/2.1/ref/models/querysets/#filteredrelation-objects

        还有一种写法是 Manager.from_queryset, 不过那样就没有 Pycharm Django 的补全和提示了，很不好
        https://docs.djangoproject.com/en/2.1/topics/db/managers/#calling-custom-queryset-methods-from-the-manager

        Examples::

            queryset = account.followers.filter(tags__name='rap', tags__deactivated_at__isnull=True)

        Equals to::

            queryset = account.followers.filter_related('tags', name='rap')

        :param name: Django related name
        :param include_all: True to include deactivated instances
        :param conditions: real filters
        """
        filtered_name = f'filtered_{name}'
        key, value = conditions.popitem()
        condition = {f'{filtered_name}__{key}': value}
        if not include_all:
            conditions.setdefault('deactivated_at__isnull', True)
        conditions = {f'{name}__{k}': v for k, v in conditions.items()}
        return self._queryset.annotate(**{filtered_name: FilteredRelation(name, condition=Q(**conditions))}) \
            .filter(**condition)

    def filter_if_in(self, data: dict, **fields: str) -> 'HQuerySet':
        """ 根据传不传值决定要不要筛选的方法

        Examples::

            queryset = queryset.filter_if_in(validated_data, name__contains='name')

        Equals to::

            if 'name' in validated_data:
                queryset = queryset.filter(name__contains=validated_data['name'])

        - 经常前端会传一些 name(required=False) 的数据
        - 以前的话，要 if 'name' in validated_data: queryset = queryset.filter(name=validated_data['name'])
        - 代码里可能会充斥大量这样的冗余判断
        - 所以我们加个小语法糖
        """
        queryset = self._queryset
        for condition, key in fields.items():
            if key in data:
                queryset = queryset.filter(**{condition: data[key]})
        return queryset

    def annotate_sum(self, key: str, **queries):
        """ 实现 Sum/Case/When 的一套快捷方式

        Examples::

            queryset.annotate_sum('is_followed', followers__followee=account)

        Equals to::

            queryset.annotate(is_followed=Sum(Case(When(followers__followee=account, then=1), default=0)))
        """
        queryset = self._queryset
        queries.setdefault('then', 1)
        return queryset.annotate(**{key: Sum(Case(When(**queries), default=0, output_field=IntegerField()))})

    @property
    def _queryset(self) -> 'HQuerySet':
        if isinstance(self, models.Manager):
            return self.get_queryset()
        # noinspection PyTypeChecker
        return self


class HQuerySet(models.QuerySet, QuerySetMixin):
    """ HUtils Query Set """


class HManager(models.Manager, QuerySetMixin):
    """ HUtils Manager """

    def get_queryset(self):
        return HQuerySet(self.model, using=self._db, hints=self._hints)
