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
                    <b-btn :to="`/grand_set/${grandSetId}/`">
                        Retour au {{ store.settings.grand_set_name }}
                    </b-btn>
                </b-col>
            </b-row>
            <b-row v-if="activity">
                <b-col>
                    <h2>{{ activity.activity_name }}</h2>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <p v-if="logs.length === 0">
                        Aucun groupe dans l'activité.
                    </p>
                    <b-card
                        v-for="(log, index) in logs"
                        :key="log.id"
                    >
                        <b-card-title>{{ log.group ? log.group.group_name : `${log.student.last_name} ${log.student.first_name}` }}</b-card-title>
                        <b-row>
                            <b-col md="7">
                                <b-card-text v-if="log.group">
                                    <span
                                        v-for="(stud, idx) in log.group.students_display"
                                        :key="idx"
                                        :class="log.missing_student.find(ms => ms === log.group.students_id[idx]) ? 'text-strike' : ''"
                                    >
                                        {{ stud }}
                                    </span>
                                </b-card-text>
                            </b-col>
                            <b-col
                                md="5"
                                class="text-right"
                            >
                                <div v-if="log.status === 'ON'">
                                    <b-btn
                                        variant="outline-primary"
                                    >
                                        <b-icon icon="graph-up" />
                                        Historique
                                    </b-btn>
                                    <b-btn
                                        variant="outline-success"
                                        :to="`/evaluation/${log.id}/${log.group ? log.group.id : '-1'}/${log.student ? log.student.matricule : '-1'}/`"
                                    >
                                        <b-icon icon="list-check" />
                                        Évaluer
                                    </b-btn>
                                    <b-btn
                                        variant="secondary"
                                        @click="changeStatus(index, 'OUT')"
                                    >
                                        <b-icon icon="box-arrow-right" />
                                        Départ
                                    </b-btn>
                                </div>
                                <div v-else>
                                    <b-btn
                                        variant="info"
                                        @click="changeStatus(index, 'ON')"
                                    >
                                        <b-icon
                                            icon="box-arrow-in-right"
                                            animation="fade"
                                        />
                                        Marquer présent
                                    </b-btn>
                                </div>
                            </b-col>
                        </b-row>
                    </b-card>
                </b-col>
            </b-row>
        </b-container>
    </div>
</template>

<script>
import axios from "axios";

import { grandsetStore } from "./stores/index.js";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    props: {
        activityId: {
            type: String,
            default: "-1",
        },
        grandSetId: {
            type: String,
            default: "-1",
        }
    },
    data: function () {
        return {
            activity: null,
            logs: [],
            store: grandsetStore(),
        };
    },
    mounted: function () {
        axios.get(`/grandset/api/activity/${this.activityId}/`)
            .then(resp => {
                this.activity = resp.data;
            });
        axios.get(`/grandset/api/activity_log/?grand_set=${this.grandSetId}&activity=${this.activityId}&status=IN&status=ON&status=IN`)
            .then(resp => {
                const logs = resp.data.results;
                const promiseGroup = logs.map(l => {
                    if (l.group) return axios.get(`/grandset/api/group/${l.group}`);
                    return axios.get(`/annuaire/api/student/${l.student}`);
                });

                Promise.all(promiseGroup)
                    .then(resps => {
                        this.logs = logs.map((l, i) => {
                            if (l.group) l.group = resps[i].data;
                            if (l.student) l.student = resps[i].data;
                            return l;
                        });
                        this.logs.sort((a, b) => a.status > b.status);
                    });

            });
    },
    methods: {
        displayStudents: function (log) {
            return log.group.students_display.filter((s, i) => !log.missing_student.includes(log.group.students_id[i])).join(", ");
        },
        changeStatus: function (logIndex, newStatus) {
            const group = this.logs[logIndex].group;

            if (!this.store.settings.return_to_hq && newStatus === "OUT") {
                this.$router.push(`/activitychange/${this.grandSetId}/${group ? group.id : "-1"}/${this.logs[logIndex].id}/`);
                return;
            }

            axios.patch(`/grandset/api/activity_log/${this.logs[logIndex].id}/`, {status: newStatus}, token)
                .then(resp => {
                    let newLog = resp.data;
                    newLog.group = group;

                    if (newStatus == "ON") {
                        this.logs.splice(logIndex, 1, newLog);
                        this.logs.sort((a, b) => a.status > b.status);
                    } else if (newStatus == "OUT") {
                        this.$root.$bvToast.toast(
                            `${group ? group.group_name : this.logs[logIndex].student.last_name} n'est plus dans l'activité ${this.activity.activity_name}`,
                            {
                                variant: "warning",
                                noCloseButton: true,
                            }
                        );
                        this.logs.splice(logIndex, 1);
                    }
                });
        }
    }
};
</script>
