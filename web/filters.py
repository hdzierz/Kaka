# -*- coding: utf-8 -*-

import django_filters
from seafood.models import Fish


class FishFilter(django_filters.FilterSet):
    class Meta:
        model = Fish
        fields = ['xreflsid']
        order_by = ['xreflsid']
