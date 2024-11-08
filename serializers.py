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

from rest_framework import serializers

from core.models import ResponsibleModel, StudentModel
from core.serializers import ResponsibleSerializer, StudentSerializer
from . import models


class GrandSetSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GrandSetSettingsModel
        fields = "__all__"


class CompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompetenceModel
        fields = "__all__"


class ActivitySerializer(serializers.ModelSerializer):
    responsibles = ResponsibleSerializer(read_only=True, many=True)
    responsibles_id = serializers.PrimaryKeyRelatedField(
        queryset=ResponsibleModel.objects.all(),
        source="responsibles",
        required=False,
        allow_null=True,
        many=True,
    )

    competence = CompetenceSerializer(read_only=True, many=True)
    competence_id = serializers.PrimaryKeyRelatedField(
        queryset=models.CompetenceModel.objects.all(),
        source="competence",
        required=False,
        allow_null=True,
        many=True,
    )

    class Meta:
        model = models.ActivityModel
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    students = StudentSerializer(read_only=True, many=True)
    students_id = serializers.PrimaryKeyRelatedField(
        queryset=StudentModel.objects.all(),
        source="students",
        required=False,
        allow_null=True,
        many=True,
    )
    students_display = serializers.SerializerMethodField()

    class Meta:
        model = models.GroupModel
        fields = "__all__"

    def get_students_display(self, obj):
        return [s.fullname_classe for s in obj.students.all()]


class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ActivityLogModel
        fields = "__all__"


class ActivityEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ActivityEvaluationModel
        fields = "__all__"


class GrandSetSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GrandSetSeriesModel
        fields = "__all__"


class GrandSetSerializer(serializers.ModelSerializer):
    # activities = ActivitySerializer(read_only=True, many=True)
    # activities_id = serializers.PrimaryKeyRelatedField(
    #     queryset=models.ActivityModel.objects.all(),
    #     source='activities',
    #     required=False,
    #     allow_null=True,
    #     many=True
    # )

    grand_set_series = GrandSetSeriesSerializer(read_only=True)
    grand_set_series_id = serializers.PrimaryKeyRelatedField(
        queryset=models.GrandSetSeriesModel.objects.all(),
        source="grand_set_series",
        required=False,
        allow_null=True,
    )

    class Meta:
        model = models.GrandSetModel
        fields = "__all__"
