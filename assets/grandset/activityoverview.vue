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
        <b-overlay
            :show="loading"
            rounded="sm"
        >
            <b-card
                class="mb-4"
                footer-bg-variant="transparent"
                no-body
                style="min-width: 320px;"
            >
                <template v-slot:header>
                    <strong>{{ activity.activity_name }}</strong>
                    <div class="float-right ml-4">
                        <b-btn
                            size="sm"
                            variant="outline-primary"
                            :to="`/activitymanagement/${$route.params.grandSetId}/${activity.id}/`"
                        >
                            <b-icon icon="eye-fill" />
                        </b-btn>
                        <b-btn
                            size="sm"
                            variant="danger"
                        >
                            <b-icon icon="trash" />
                        </b-btn>
                    </div>
                </template>
                <b-list-group
                    v-if="groups.length > 0"
                    flush
                >
                    <b-list-group-item
                        v-for="group in groups"
                        :key="group.id"
                        v-b-toggle="'students-' + group.id"
                    >
                        {{ group.group_name }} <em>{{ groupStatus(group) }}</em>
                        <b-btn
                            class="float-right ml-2"
                            variant="outline-primary"
                            size="sm"
                            :to="`/activitychange/${group.activityLog}/`"
                            v-b-toggle.sidebar
                        >
                            <b-icon icon="arrow-left-right" />
                        </b-btn>
                        <br>
                        <b-collapse 
                            :id="'students-' + group.id"
                            :accordion="'activity-' + activity.id"
                        >
                            <small
                                v-for="student in group.students_display"
                                :key="student.matricule"
                                class="text-muted"
                            >
                                {{ student }}
                                <br>
                            </small>
                            <small>Mis à jour à {{ lastUpdate(group) }}</small>
                        </b-collapse>
                    </b-list-group-item>
                </b-list-group>
                <b-card-body v-else>Aucun groupe dans cette activité</b-card-body>
                <template v-slot:footer>
                    <b-btn
                        class="float-right"
                        variant="outline-secondary"
                    >
                        <b-icon icon="plus" />
                        Ajouter groupe
                    </b-btn>
                </template>
            </b-card>
        </b-overlay>
    </div>
</template>

<script>
import axios from "axios";

import Moment from "moment";
Moment.locale("fr");


export default {
    props: {
        activity: {
            type: Object,
            default: () => {},
        }
    },
    data: function () {
        return {
            groups: [],
            loading: true,
        };
    },
    methods: {
        lastUpdate: function (group) {
            return Moment(group.datetime_update).format("HH:mm");
        },
        groupStatus: function (group) {
            switch (group.status) {
            case "ON":
                return "";
            case "IN":
                return "⮞ En route vers l'activité";
            case "OUT":
                return "⮞ Sorti de l'activité";
            default:
                return "";
            }
        }
    },
    mounted: function () {
        axios.get(`/grandset/api/activity_log/?activity=${this.activity.id}&grand_set=${this.$route.params.grandSetId}&ordering=-datetime_update`)
            .then(resp => {
                const ongoingLogs = resp.data.results.filter(aL => aL.status != "DON");
                const groupsId = ongoingLogs.map(aL => aL.group);
                Promise.all(groupsId.map(gI => axios.get(`/grandset/api/group/${gI}`)))
                    .then(values => {
                        this.groups = values.map((r, i) => {
                            let group = r.data;
                            group.status = ongoingLogs[i].status;
                            group.activityLog = ongoingLogs[i].id;
                            group.datetime_update = ongoingLogs[i].datetime_update;
                            group.datetime_creation = ongoingLogs[i].datetime_creation;
                            return group;
                        });
                        this.loading = false;
                    });
                if (groupsId.length == 0) this.loading = false;
            })
            .catch(err => {
                console.log(err);
                this.loading = false;
            });
    }
};
</script>
