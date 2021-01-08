#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: superstrongz
@license: MIT Licence 
@contact: 857508399@qq.com
@site: http://www.superstrongz.com/
@software: PyCharm
@file: search_indexes.py
@time: ??
"""
from haystack import indexes
from job.models import Job


class JobIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # author = indexes.CharField(model_attr='author')
    # company = indexes.CharField(model_attr='company')

    def get_model(self):
        return Job

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
