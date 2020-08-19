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


from django.urls import path

from rest_framework.routers import DefaultRouter

from . import views
app_name = 'grandset'

urlpatterns = [
    path("", views.GrandSetView.as_view(), name="grandset"),
    path("api/activity_stat/<int:grand_set>/group/<int:group>/", views.ActivityStatAPI.as_view()),
    path("api/activity_stat/<int:grand_set>/student/<int:student>/", views.ActivityStatAPI.as_view()),
    path("api/group_without_activity/<int:grand_set>/", views.GroupWithoutActivityAPI.as_view()),
]

router = DefaultRouter()
router.register(r'api/group', viewset=views.GroupViewSet)
router.register(r'api/activity', viewset=views.ActivityViewSet)
router.register(r'api/activity_log', viewset=views.ActivityLogViewSet)
router.register(r'api/activity_evaluation', viewset=views.ActivityEvaluationViewSet)
router.register(r'api/grandset', viewset=views.GrandSetViewSet)
router.register(r'api/grandset_series', viewset=views.GrandSetSeriesViewSet)

urlpatterns += router.urls
