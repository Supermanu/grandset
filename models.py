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

from datetime import timedelta

from django.db import models
from django.contrib.postgres.fields import JSONField

from core.models import StudentModel, ResponsibleModel, TeachingModel


class GrandSetSettingsModel(models.Model):
    teachings = models.ManyToManyField(TeachingModel)
    return_to_hq = models.BooleanField(default=True)
    max_points = models.PositiveIntegerField(default=20)


class CompetenceModel(models.Model):
    name = models.CharField(max_length=100)


class ActivityModel(models.Model):
    """
    An activity of the GrandSet.
    """

    activity_name = models.CharField(max_length=100)
    max_participant = models.PositiveIntegerField(default=10)
    recommended_participation = models.PositiveIntegerField(default=8)
    average_time = models.DurationField(default=timedelta(minutes=20))
    description = models.TextField(blank=True)
    responsibles = models.ManyToManyField(ResponsibleModel, blank=True)
    competence = models.ManyToManyField(CompetenceModel, blank=True)
    datetime_creation = models.DateTimeField(auto_now_add=True)
    datetime_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.activity_name


class GroupModel(models.Model):
    """
    A set of students that goes from activity to activity.
    """

    group_name = models.CharField(max_length=100)
    students = models.ManyToManyField(StudentModel)
    datetime_creation = models.DateTimeField(auto_now_add=True)
    datetime_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.group_name


class GrandSetSeriesModel(models.Model):
    """
    A Grand Set series that follows a set of Grand Set. It records
    the groups involved as well as the activities that do not
    necessarily occur at every Grand Set.
    """

    name = models.CharField(max_length=100)
    date_start = models.DateField()
    date_end = models.DateField(null=True, blank=True)
    groups = models.ManyToManyField(GroupModel)
    activities = models.ManyToManyField(ActivityModel)
    datetime_creation = models.DateTimeField(auto_now_add=True)
    datetime_update = models.DateTimeField(auto_now=True)


class GrandSetModel(models.Model):
    """
    A Grand Set event.
    """

    date = models.DateField()
    activities = models.ManyToManyField(ActivityModel)
    grand_set_series = models.ForeignKey(GrandSetSeriesModel, on_delete=models.CASCADE, null=True)
    datetime_creation = models.DateTimeField(auto_now_add=True)
    datetime_update = models.DateTimeField(auto_now=True)


class ActivityLogModel(models.Model):
    """
    An ongoing activity.
    """
    ON_THE_WAY = "IN"
    ON_GOING = "ON"
    LEAVING = "OUT"
    DONE = "DON"
    STATUS_CHOICES = [
        (ON_THE_WAY, "En route"),
        (ON_GOING, "Actif"),
        (LEAVING, "Sorti"),
        (DONE, "Fini")
    ]

    activity = models.ForeignKey(ActivityModel, on_delete=models.CASCADE)
    grand_set = models.ForeignKey(GrandSetModel, on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(
        GroupModel,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    student = models.ForeignKey(
        StudentModel,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=3,
        default=ON_THE_WAY
    )
    datetime_creation = models.DateTimeField(auto_now_add=True)
    datetime_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s - %s : %s (%s)" % (
            self.datetime_update,
            self.group.group_name if self.group else self.student,
            self.activity.activity_name,
            self.status
        )


class ActivityEvaluationModel(models.Model):
    """
    Evaluation of a student for an ongoing activity.
    """
    activity_log = models.ForeignKey(ActivityLogModel, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentModel, on_delete=models.CASCADE)
    evaluation = models.DecimalField(max_digits=8, decimal_places=5, null=True, blank=True)
    competence_evaluation = JSONField(default=dict)
    datetime_creation = models.DateTimeField(auto_now_add=True)
    datetime_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s (%s) : %s" % (str(self.activity_log.activity), str(self.student), self.evaluation)
