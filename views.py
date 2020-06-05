# This file is part of HappySchool.
#
# HappySchool is the legal property of its developers, whose names
# can be found in the AUTHORS file distributed with this source
# distribution.
#
# HappySchool is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HappySchool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with HappySchool.  If not, see <http://www.gnu.org/licenses/>.

import json

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from django_filters import rest_framework as filters

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count

from core.views import get_app_settings, PageNumberSizePagination
from core.utilities import get_menu

from . import models, serializers


def get_menu_entry(active_app: str, user) -> dict:
    if not user.has_perm('grandset.view_grandsetmodel'):
        return {}
    return {
            "app": "grandset",
            "display": "Grand Set",
            "url": "/grandset",
            "active": active_app == "grandset"
    }


def get_settings():
    return get_app_settings(models.GrandSetSettingsModel)


class GrandSetView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    TemplateView
):
    template_name = "grandset/grandset.html"
    permission_required = ('grandset.view_grandsetmodel',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['menu'] = json.dumps(get_menu(self.request.user, "grandset"))
        context['settings'] = json.dumps((serializers.GrandSetSettingsSerializer(get_settings()).data))

        last_grandset = models.GrandSetModel.objects.order_by("-date").first()
        if not last_grandset:
            context["last_grandset"] = json.dumps(last_grandset)
        else:
            context["last_grandset"] = json.dumps(serializers.GrandSetSerializer(last_grandset).data)

        return context


class BaseViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    pagination_class = PageNumberSizePagination
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]


class GroupViewSet(BaseViewSet):
    queryset = models.GroupModel.objects.all()
    serializer_class = serializers.GroupSerializer


class ActivityViewSet(BaseViewSet):
    queryset = models.ActivityModel.objects.all()
    serializer_class = serializers.ActivitySerializer


class ActivityLogFilters(filters.FilterSet):
    status = filters.MultipleChoiceFilter(choices=models.ActivityLogModel.STATUS_CHOICES)

    class Meta:
        model = models.ActivityLogModel
        fields = ["activity", "grand_set", "group", "status"]


class ActivityLogViewSet(BaseViewSet):
    queryset = models.ActivityLogModel.objects.all()
    serializer_class = serializers.ActivityLogSerializer
    filter_class = ActivityLogFilters
    ordering_fields = ["datetime_update"]


class ActivityEvaluationViewSet(BaseViewSet):
    queryset = models.ActivityEvaluationModel.objects.all()
    serializer_class = serializers.ActivityEvaluationSerializer
    filterset_fields = ['student', 'activity_log']


class GrandSetViewSet(BaseViewSet):
    queryset = models.GrandSetModel.objects.all()
    serializer_class = serializers.GrandSetSerializer


class GrandSetSeriesViewSet(BaseViewSet):
    queryset = models.GrandSetSeriesModel.objects.all()
    serializer_class = serializers.GrandSetSeriesSerializer


class ActivityStatAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, grand_set, group, format=None):
        current_grand_set = models.GrandSetModel.objects.get(id=grand_set)
        grand_set_series = models.GrandSetSeriesModel.objects.get(grand_sets=current_grand_set)
        grand_sets = grand_set_series.grand_sets.all()

        group_logs = models.ActivityLogModel.objects.filter(
            grand_set__in=grand_sets.all(),
            activity__in=current_grand_set.activities.all(),
            status="DON",
            group__id=group
        )

        group_logs_count = list(
            group_logs.values("activity").annotate(count_group=Count("activity"))
        )

        activity_participant = models.ActivityLogModel.objects.filter(
            grand_set=current_grand_set,
            status__in=["IN", "ON"]
        )

        activity_participant_count = list(
            activity_participant.values("activity").annotate(count_participant=Count("group"))
        )

        activities = activity_participant_count
        for g in group_logs_count:
            activity_index = next(
                (index for (index, d) in enumerate(activities) if d["activity"] == g["activity"]),
                None
            )
            if activity_index:
                activities[activity_index]["count_group"] = g["count_group"]
            else:
                activities.append(g)

        return Response(json.dumps(activities))


class GroupWithoutActivityAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, grand_set, format=None):
        print(grand_set)
        running_groups = models.ActivityLogModel.objects \
            .filter(grand_set=grand_set) \
            .values_list("group", flat=True)
        groups = models.GroupModel.objects.exclude(pk__in=running_groups)
        return Response(serializers.GroupSerializer(groups, many=True).data)
