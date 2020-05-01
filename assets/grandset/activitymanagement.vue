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
                <b-btn :to="`/grand_set/${grandSetId}/`">
                    Retour au Grand Set
                </b-btn>
            </b-row>
            <b-row v-if="activity">
                <h2>{{ activity.activity_name }}</h2>
            </b-row>
            <b-row>
                <b-col>
                    <b-card
                        v-for="(log, index) in logs"
                        :key="log.id"
                    >
                        <b-card-title>{{ log.group.group_name }}</b-card-title>
                        <b-row>
                            <b-col md="7">
                                <b-card-text>
                                    {{ log.group.students_display.join(", ") }}
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
                                        @click="changeStatus(index, 'ON')"
                                        variant="info"
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
            logs: []
        };
    },
    methods: {
        changeStatus: function (logIndex, newStatus) {
            const group = this.logs[logIndex].group;
            axios.patch(`/grandset/api/activity_log/${this.logs[logIndex].id}/`, {status: newStatus}, token)
                .then(resp => {
                    let newLog = resp.data;
                    newLog.group = group;

                    if (newStatus == "ON") {
                        this.logs.splice(logIndex, 1, newLog);
                        this.logs.sort((a, b) => a.status > b.status);
                    } else if (newStatus == "OUT") {
                        this.$root.$bvToast.toast(
                            `${group.group_name} n'est plus dans l'activité ${this.activity.activity_name}`,
                            {
                                variant: "warning",
                                noCloseButton: true,
                            }
                        );
                        this.logs.splice(logIndex, 1);
                    }
                });
        }
    },
    mounted: function () {
        axios.get(`/grandset/api/activity/${this.activityId}/`)
            .then(resp => {
                this.activity = resp.data;
            });
        axios.get(`/grandset/api/activity_log/?grand_set=${this.grandSetId}&activity=${this.activityId}&status=IN&status=ON&status=IN`)
            .then(resp => {
                const logs = resp.data.results;
                const promiseGroup = logs.map(l => axios.get(`/grandset/api/group/${l.group}`));

                Promise.all(promiseGroup)
                    .then(resps => {
                        this.logs = logs.map((l, i) => {
                            l.group = resps[i].data;
                            return l;
                        });
                        this.logs.sort((a, b) => a.status > b.status);
                    });

            });
    }
};
</script>
