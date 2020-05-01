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
                <b-btn @click="$router.go(-1)">
                    Retour
                </b-btn>
            </b-row>
            <b-row>
                <b-col
                    sm="12"
                    md="6"
                    v-if="group"
                >
                    <h3>{{ group.group_name }}</h3>
                    <ul>
                        <li
                            v-for="student in group.students_display"
                            :key="student"
                        >
                            {{ student }}
                        </li>
                    </ul>
                </b-col>
                <b-col>
                    <b-list-group>
                        <b-list-group-item
                            v-for="activity in activities"
                            :key="activity.id"
                            button
                            class="d-flex justify-content-between align-items-center"
                            @click="changeActivity(activity)"
                            :disabled="activity.id == activityLog.activity"
                        >
                            {{ activity.activity_name }}
                            <span>
                                <b-badge
                                    variant="primary"
                                    pill
                                >
                                    Fait : {{ activity.done }}
                                </b-badge>
                                <b-badge
                                    variant="primary"
                                    pill
                                >
                                    Participants : {{ activity.participant }}
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
                        ⇒ {{ log.activity.activity_name }} {{ lastUpdate(log.datetime_update) }}.
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

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    props: {
        activityLogId: {
            type: String,
            default: "-1"
        },
    },
    data: function () {
        return {
            activityLog: null,
            group: null,
            activities: [],
            logs: []
        };
    },
    methods: {
        lastUpdate: function (lastUpdate) {
            return String(Moment(lastUpdate).calendar()).toLowerCase();
        },
        changeActivity: function (activity) {
            let app = this;
            axios.patch(
                `/grandset/api/activity_log/${this.activityLogId}/`,
                {status: "DON"},
                token
            )
                .then(() => {
                    const newLog = {
                        grand_set: app.activityLog.grand_set,
                        group: app.activityLog.group,
                        activity: activity.id,
                    };
                    axios.post("/grandset/api/activity_log/", newLog, token)
                        .then(() => {
                            app.$router.push(`/grand_set/${app.activityLog.grand_set}`, () => {
                                app.$root.$bvToast.toast(
                                    `${app.group.group_name} est maintenant dans l'activité ${activity.activity_name}`,
                                    {
                                        variant: "success",
                                        noCloseButton: true,
                                    }
                                );
                            });
                        });
                });
        }
    },
    mounted: function () {
        // Get full activityLog object.
        axios.get(`/grandset/api/activity_log/${this.activityLogId}/`)
            .then(actLogResp => {
                this.activityLog = actLogResp.data;

                // Get full group object.
                axios.get(`/grandset/api/group/${this.activityLog.group}`)
                    .then(respGroup => {
                        this.group = respGroup.data;
                    });

                // Get activities of the current GrandSet.
                axios.get(`/grandset/api/grandset/${this.activityLog.grand_set}/`)
                    .then(respGrandSet => {
                        const promiseActivities = respGrandSet.data.activities.map(activity => {
                            return axios.get(`/grandset/api/activity/${activity}/`);
                        });

                        Promise.all(promiseActivities)
                            .then(resps => {
                                const activities = resps.map(r => r.data);

                                axios.get(`/grandset/api/activity_stat/${this.activityLog.grand_set}/${this.activityLog.group}/`)
                                    .then(respStat => {
                                        const activityCount = JSON.parse(respStat.data);
                                        activities.forEach(activity => {
                                            const actCount = activityCount.find(aC => aC.activity == activity.id);
                                            if (actCount) {
                                                activity.done = "count_group" in actCount ? actCount.count_group : 0;
                                                activity.participant = "count_participant" in actCount ? actCount.count_participant : 0;
                                            } else {
                                                activity.done = 0;
                                            }
                                        });
                                        this.activities = activities;
                                    });

                                // Get activity history for the current group.
                                axios.get(`/grandset/api/activity_log/?group=${this.activityLog.group}&ordering=-datetime_update`)
                                    .then(respLogs => {
                                        this.logs = respLogs.data.results.filter(log => {
                                            return activities.find(a => a.id == log.activity)
                                                && this.activityLog.grand_set == log.grand_set;
                                        }).map(log => {
                                            log.activity = activities.find(a => a.id == log.activity);
                                            return log;
                                        });
                                    });
                            });
                    });
            });
    },
};
</script>
