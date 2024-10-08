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
        <b-container>
            <b-row>
                <b-col>
                    <b-btn @click="$router.go(-1)">
                        Retour
                    </b-btn>
                </b-col>
            </b-row>
            <b-row>
                <b-col
                    v-if="group || student"
                    sm="12"
                    md="5"
                >
                    <div v-if="group">
                        <h3>{{ group.group_name }}</h3>
                        <ul>
                            <li
                                v-for="(stud, idx) in group.students_display"
                                :key="stud"
                                :class="studentMissing(group.students_id[idx])"
                            >
                                {{ stud }}
                            </li>
                        </ul>
                    </div>
                    <div v-else>
                        <h3>{{ student.last_name }} {{ student.first_name }}</h3>
                    </div>
                </b-col>
                <b-col>
                    <b-list-group>
                        <b-list-group-item
                            v-for="activity in activities"
                            :key="activity.id"
                            button
                            class="d-flex justify-content-between align-items-center"
                            :disabled="activityLog ? activity.id == activityLog.activity : triggered"
                            @click="changeActivity(activity, $event)"
                        >
                            {{ activity.activity_name }}
                            <span>
                                <small>± {{ getMinutes(activity.average_time) }}min.</small> 
                                <b-badge
                                    variant="primary"
                                    pill
                                >
                                    Fait : {{ activity.done }}/{{ activity.recommended_participation }}
                                </b-badge>
                                <b-badge
                                    variant="primary"
                                    pill
                                >
                                    Participants : {{ activity.participant }}/{{ activity.max_participant }}
                                </b-badge>
                            </span>
                        </b-list-group-item>
                    </b-list-group>
                </b-col>
            </b-row>
            <b-row class="mt-4">
                <b-col>
                    <h4>Historique des activités</h4>
                    <p
                        v-for="log in logs"
                        :key="log.id"
                        class="border-bottom"
                    >
                        ⇒ <small>{{ lastUpdate(log.datetime_update) }}</small>
                        <strong>{{ log.activity.activity_name }}</strong>
                        <span v-if="student">({{ log.group ? "en groupe" : "seul(e)" }})</span>
                    </p>
                </b-col>
            </b-row>
        </b-container>
    </div>
</template>

<script>
import axios from "axios";

import Moment from "moment";
Moment.locale("fr");

import { grandsetStore } from "./stores/index.js";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    props: {
        activityLogId: {
            type: String,
            default: "-1"
        },
        grandSetId: {
            type: String,
            default: "-1",
        },
        groupId: {
            type: String,
            default: "-1",
        },
        studentId: {
            type: String,
            default: "-1",
        }
    },
    data: function () {
        return {
            activityLog: null,
            group: null,
            student: null,
            activities: [],
            logs: [],
            triggered: false,
            store: grandsetStore(),
        };
    },
    mounted: function () {
        // Get full activityLog object.
        if (this.activityLogId !== "-1") {
            axios.get(`/grandset/api/activity_log/${this.activityLogId}/`)
                .then(actLogResp => {
                    this.activityLog = actLogResp.data;
                });
        }

        // Get full group object.
        if (this.groupId !== "-1") {
            axios.get(`/grandset/api/group/${this.groupId}`)
                .then(respGroup => {
                    this.group = respGroup.data;
                });
        }

        // Get full student object.
        if (this.studentId !== "-1") {
            axios.get(`/annuaire/api/student/${this.studentId}/`)
                .then(resp => {
                    this.student = resp.data;
                });
        }

        // Get activities of the current GrandSet.
        axios.get(`/grandset/api/grandset/${this.grandSetId}/`)
            .then(respGrandSet => {
                const promiseActivities = respGrandSet.data.activities.map(activity => {
                    return axios.get(`/grandset/api/activity/${activity}/`);
                });

                Promise.all(promiseActivities)
                    .then(resps => {
                        const activities = resps.map(r => r.data);
                        let urlStat = `/grandset/api/activity_stat/${this.grandSetId}/`;
                        if (this.studentId !== "-1") {
                            urlStat += `student/${this.studentId}/`;
                        } else {
                            urlStat += `group/${this.groupId}/`;
                        }
                        axios.get(urlStat)
                            .then(respStat => {
                                const activityCount = JSON.parse(respStat.data);
                                activities.forEach(activity => {
                                    const actCount = activityCount.find(aC => aC.activity == activity.id);
                                    if (actCount) {
                                        activity.done = "count_log" in actCount ? actCount.count_log : 0;
                                        activity.participant = "count_participant_from_group" in actCount ? actCount.count_participant_from_group : 0;
                                        activity.participant += "count_participant_from_student" in actCount ? actCount.count_participant_from_student : 0;
                                    } else {
                                        activity.done = 0;
                                        activity.participant = 0;
                                    }
                                });
                                this.activities = activities;
                            });

                        // Get activity history for the current group.
                        const filters = this.group ? `group=${this.groupId}` : `student=${this.studentId}`;
                        axios.get(`/grandset/api/activity_log/?${filters}&ordering=-datetime_update`)
                            .then(respLogs => {
                                this.logs = respLogs.data.results.filter(log => {
                                    return activities.find(a => a.id == log.activity)
                                        && this.grandSetId == log.grand_set;
                                }).map(log => {
                                    log.activity = activities.find(a => a.id == log.activity);
                                    return log;
                                });
                            });
                    });
            });
    },
    methods: {
        studentMissing: function (studentId) {
            if (this.activityLog && this.activityLog.missing_student.find(s => s === studentId)) return "text-strike";
            return "";
        },
        getMinutes: function (minutes) {
            return parseInt(minutes.slice(0, 2)) * 60 + parseInt(minutes.slice(3, 5));
        },
        lastUpdate: function (lastUpdate) {
            return String(Moment(lastUpdate).calendar()).toLowerCase();
        },
        changeActivity: function (activity, event) {
            // Avoid double clicks
            if(!event.detail || event.detail === 1){
                setTimeout(() => {
                    if (this.triggered) return;

                    this.triggered = true;
                    if (this.activityLog) {
                        axios.patch(
                            `/grandset/api/activity_log/${this.activityLogId}/`,
                            {status: "DON"},
                            token
                        )
                            .then(() => {
                                this.createNewLog(activity);
                            });
                    } else {
                        this.createNewLog(activity);
                    }
                }, 100);
            }
        },
        createNewLog: function (activity) {
            const newLog = {
                grand_set: this.grandSetId,
                [this.group ? "group" : "student"]: this.group ? this.groupId : this.studentId,
                activity: activity.id,
            };
            if (this.store.settings.direct_from_hq) newLog.status = "ON";
            axios.post("/grandset/api/activity_log/", newLog, token)
                .then(() => {
                    this.triggered = false;
                    this.$router.push(`/grand_set/${this.grandSetId}`, () => {
                        this.$root.$bvToast.toast(
                            `${this.group ? this.group.group_name : this.student.display} est maintenant dans l'activité ${activity.activity_name}`,
                            {
                                variant: "success",
                                noCloseButton: true,
                            }
                        );
                    });
                });
        },
    },
};
</script>
