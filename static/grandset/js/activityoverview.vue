<!-- This file is part of Happyschool. -->
<!--  -->
<!-- Happyschool is the legal property of its developers, whose names -->
<!-- can be found in the AUTHORS file distributed with this source -->
<!-- distribution. -->
<!--  -->
<!-- Happyschool is free software: you can redistribute it and/or modify -->
<!-- it under the terms of the GNU Affero General Public License as published by -->
<!-- the Free Software Foundation, either version 3 of the License, or -->
<!-- (at your option) any later version. -->
<!--  -->
<!-- Happyschool is distributed in the hope that it will be useful, -->
<!-- but WITHOUT ANY WARRANTY; without even the implied warranty of -->
<!-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the -->
<!-- GNU Affero General Public License for more details. -->
<!--  -->
<!-- You should have received a copy of the GNU Affero General Public License -->
<!-- along with Happyschool.  If not, see <http://www.gnu.org/licenses/>. -->

<template>
    <div>
        <BOverlay
            :show="loading"
            rounded="sm"
        >
            <BCard
                class="mb-4 card"
                footer-bg-variant="transparent"
                no-body
            >
                <template #header>
                    <div class="opposite">
                        <strong>{{ activity ? activity.activity_name : "Groupes sans activité" }} ({{ groups.length }})</strong>
                        <span>
                            <BButton
                                v-if="activity"
                                size="sm"
                                variant="outline-primary"
                                :to="`/activitymanagement/${$route.params.grandSetId}/${activity.id}/`"
                            >
                                <IBiEyeFill />
                            </BButton>
                        </span>
                    </div>
                </template>
                <BListGroup
                    v-if="groups.length > 0 && !hide"
                    flush
                >
                    <BListGroupItem
                        v-for="group in groups"
                        :key="group.activityLog"
                        class="d-flex justify-content-between align-items-center text-end"
                    >
                        <span v-if="group.matricule">
                            {{ group.last_name }} {{ group.first_name }}
                        </span>
                        <span v-else>
                            {{ group.group_name }}
                        </span>
                        <span>
                            <em>
                                <IBiChevronDoubleRight
                                    v-if="group.status === 'IN'"
                                />
                                <IBiChevronBarRight
                                    v-if="group.status === 'OUT'"
                                />
                                {{ groupStatus(group) }}
                            </em>
                            <BButtonGroup>
                                <BButton
                                    class="float-right ml-2"
                                    variant="outline-primary"
                                    size="sm"
                                    @click="activityChange(group)"
                                >
                                    <IBiArrowLeftRight />
                                </BButton>
                                <BButton
                                    v-b-toggle="'students-' + group.activityLog"
                                    class="float-right ml-2"
                                    size="sm"
                                    variant="outline-secondary"
                                >
                                    <IBiThreeDotsVertical />
                                </BButton>
                            </BButtonGroup>
                            <br>
                            <BCollapse
                                :id="'students-' + group.activityLog"
                                :accordion="activity ? 'activity-' + activity.id : 'nullactivity'"
                            >
                                <span v-if="group.id">
                                    <small
                                        v-for="(student, idx) in group.students_display"
                                        :key="group.students_id[idx]"
                                        :class="'text-muted ' + studentMissing(group.students_id[idx], group)"
                                    >
                                        {{ student }}
                                        <BLink
                                            @click="activityChange(group, group.students_id[idx])"
                                        >
                                            <IBiArrowLeftRight />
                                        </BLink>
                                        <br>
                                    </small>
                                </span>
                                <small>Mis à jour à {{ lastUpdate(group) }}</small>
                            </BCollapse>
                        </span>
                    </BListGroupItem>
                </BListGroup>
                <BCardBody v-else-if="hide">
                    <BButton
                        block
                        @click="hide=!hide"
                    >
                        Montrer tous les groupes
                    </BButton>
                </BCardBody>
                <BCardBody v-else>
                    Aucun groupe dans cette activité
                </BCardBody>
            </BCard>
        </BOverlay>
    </div>
</template>

<script>
import axios from "axios";

import { DateTime } from "luxon";

export default {
    props: {
        activity: {
            type: Object,
            default: () => {},
        },
    },
    data: function () {
        return {
            groups: [],
            loading: true,
            hide: false,
        };
    },
    mounted: function () {
        if (this.activity) {
            axios.get(`/grandset/api/activity_log/?activity=${this.activity.id}&grand_set=${this.$route.params.grandSetId}&ordering=-datetime_update`)
                .then((resp) => {
                    const ongoingLogs = resp.data.results.filter(aL => aL.status != "DON");
                    const objects = ongoingLogs.map((aL) => {
                        const objectType = aL.group ? "group" : "student";
                        const objectId = aL.group ? aL.group : aL.student;
                        return { objectId: objectId, objectType: objectType };
                    });
                    Promise.all(objects.map((o) => {
                        if (o.objectType == "group") {
                            return axios.get(`/grandset/api/group/${o.objectId}/`);
                        } else if (o.objectType == "student") {
                            return axios.get(`/annuaire/api/student/${o.objectId}/`);
                        }
                    }))
                        .then((values) => {
                            this.groups = values.map((r, i) => {
                                let group = r.data;
                                group.status = ongoingLogs[i].status;
                                group.activityLog = ongoingLogs[i].id;
                                group.missing_student = ongoingLogs[i].missing_student;
                                group.datetime_update = ongoingLogs[i].datetime_update;
                                group.datetime_creation = ongoingLogs[i].datetime_creation;
                                return group;
                            });
                            this.loading = false;
                        });
                    // Nobody in that activity.
                    if (objects.length == 0) this.loading = false;
                })
                .catch((err) => {
                    console.log(err);
                    this.loading = false;
                });
        } else {
            this.hide = true;
            // Show groups without activity.
            axios.get(`/grandset/api/group_without_activity/${this.$route.params.grandSetId}/`)
                .then((resp) => {
                    this.groups = resp.data;
                    this.loading = false;
                })
                .catch((err) => {
                    console.log(err);
                    this.loading = false;
                });
        }
    },
    methods: {
        studentMissing: function (studentId, group) {
            if ("missing_student" in group && group.missing_student.find(s => s === studentId)) return "text-strike";
            return "";
        },
        activityChange: function (group, student = "-1") {
            console.log(group);
            console.log(student);
            const grandSetId = this.$route.params.grandSetId;
            const studentId = group.matricule ? group.matricule : student;
            const groupId = group.id && studentId === "-1" ? group.id : "-1";
            const activityLogId = this.activity ? group.activityLog : "-1";
            this.$router.push(`/activitychange/${grandSetId}/${groupId}/${studentId}/${activityLogId}`);
        },
        lastUpdate: function (group) {
            return DateTime.fromISO(group.datetime_update).toFormat("HH:mm");
        },
        groupStatus: function (group) {
            switch (group.status) {
                case "ON":
                    return "";
                case "IN":
                    return "En route vers l'activité";
                case "OUT":
                    return "Sorti de l'activité";
                default:
                    return "";
            }
        },
        hasGroupOrStudent: function (query) {
            const filteredGroups = this.groups.filter((g) => {
                const isInGroupName = g.group_name.toLowerCase().includes(query.toLowerCase());
                const isInStudentsName = g.students_display.join("").toLowerCase().includes(query.toLowerCase());
                return isInGroupName || isInStudentsName;
            });
            return filteredGroups.length > 0;
        },
    },
};
</script>

<style>
.opposite {
    display: flex;
    justify-content: space-between;
}

.text-strike {
  text-decoration: line-through;
}
</style>
