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
from django.db.models import Count, Q

from core.views import get_app_settings, LargePageSizePagination
from core.models import StudentModel
from core.utilities import get_menu

from . import models, serializers


def get_menu_entry(active_app: str, user) -> dict:
    entry_name = get_settings().grand_set_name
    if not user.has_perm('grandset.view_grandsetmodel'):
        return {}
    return {
            "app": "grandset",
            "display": f"{entry_name}",
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
    pagination_class = LargePageSizePagination
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]


class GroupViewSet(BaseViewSet):
    queryset = models.GroupModel.objects.all()
    serializer_class = serializers.GroupSerializer


class ActivityViewSet(BaseViewSet):
    queryset = models.ActivityModel.objects.all()
    serializer_class = serializers.ActivitySerializer


class StudentFilter(filters.ModelChoiceFilter):
    def filter(self, qs, value):
        if value:
            return qs.filter(
                Q(student=value) | Q(group__students=value)
            ).exclude(missing_student=value)
        return qs


class ActivityLogFilters(filters.FilterSet):
    status = filters.MultipleChoiceFilter(choices=models.ActivityLogModel.STATUS_CHOICES)
    student = StudentFilter(queryset=StudentModel.objects.all())

    class Meta:
        model = models.ActivityLogModel
        fields = ["activity", "grand_set", "group", "status", "student"]


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
    filterset_fields = ["grand_set_series"]


class GrandSetSeriesViewSet(BaseViewSet):
    queryset = models.GrandSetSeriesModel.objects.all()
    serializer_class = serializers.GrandSetSeriesSerializer


class ActivityStatAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, grand_set, group=None, student=None, format=None):
        current_grand_set = models.GrandSetModel.objects.get(id=grand_set)
        grand_sets = current_grand_set.grand_set_series.grandsetmodel_set.all()

        if student:
            s = StudentModel.objects.get(matricule=int(student))
            group = models.GroupModel.objects.get(students=s).id
            filter_fields = Q(group__id=group) | Q(student=s)
        else:
            filter_fields = Q(group__id=group)

        targeted_logs = models.ActivityLogModel.objects.filter(
            Q(
                grand_set__in=grand_sets.all(),
                activity__in=current_grand_set.activities.all(),
                status="DON",
            )
            & filter_fields
        )
        if student:
            targeted_logs = targeted_logs.exclude(missing_student=s)

        # Count the number of done activities by activity for the student or the group.
        logs_count = list(
            targeted_logs.values("activity").annotate(count_log=Count("activity"))
        )

        # Get all logs from running activities or soon to be.
        activity_participant = models.ActivityLogModel.objects.filter(
            grand_set=current_grand_set,
            status__in=["IN", "ON"]
        )

        # Count the number of student from both groups and lonely students in running activities.
        activity_participant_count = list(
            activity_participant.values("activity").annotate(
                count_participant_from_group=Count("group__students"),
                count_participant_from_student=Count("student")
            )
        )

        activities = activity_participant_count
        for g in logs_count:
            # Find related activity.
            activity_index = next(
                (index for (index, d) in enumerate(activities) if d["activity"] == g["activity"]),
                None
            )
            if activity_index:
                activities[activity_index]["count_log"] = g["count_log"]
            else:
                activities.append(g)

        return Response(json.dumps(activities))


class GroupWithoutActivityAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, grand_set, format=None):
        running_groups = models.ActivityLogModel.objects \
            .filter(grand_set=grand_set) \
            .values_list("group", flat=True)
        grand_set_series_group = models.GrandSetModel.objects.get(id=grand_set).grand_set_series.groups.all()
        groups = grand_set_series_group.exclude(pk__in=running_groups)
        return Response(serializers.GroupSerializer(groups, many=True).data)
