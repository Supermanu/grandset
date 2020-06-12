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
            <b-row class="justify-content-md-center m-2">
                <b-col md="8">
                    <b-input-group class="mb-2">
                        <b-form-input
                            placeholder="Rechercher une activité"
                            v-model="search"
                        />

                        <template v-slot:append>
                            <b-input-group-text>
                                <b-icon icon="search" />
                            </b-input-group-text>
                        </template>
                    </b-input-group>
                </b-col>
                <b-col
                    md="3"
                    align-h="end"
                >
                    <b-dropdown
                        variant="outline-secondary"
                        block
                        no-caret
                    >
                        <template v-slot:button-content>
                            <b-icon icon="list" />
                            Gestion
                        </template>
                        <b-dropdown-item href="#">Gestion du Grand Set</b-dropdown-item>
                        <b-dropdown-item :to="`/grand_set_series/${grandSetSerieId}/`">Gestion de la série</b-dropdown-item>
                    </b-dropdown>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <b-card-group columns>
                        <activity-overview />
                        <activity-overview
                            v-for="activity in filteredActivities"
                            :key="activity.id"
                            :activity="activity"
                            ref="activities"
                        />
                    </b-card-group>
                </b-col>
            </b-row>
        </b-container>
    </div>
</template>

<script>
import axios from "axios";

import Vue from "vue";
import { BootstrapVue, IconsPlugin } from "bootstrap-vue";
import "bootstrap-vue/dist/bootstrap-vue.css";

import ActivityOverview from "./activityoverview.vue";

Vue.use(BootstrapVue);
Vue.use(IconsPlugin);

export default {
    props: {
        grandSetId: {
            type: String,
            default: "-1",
        }
    },
    data: function () {
        return {
            grandSet: null,
            activities: [],
            search: "",
            grandSetSerieId: "-1",
        };
    },
    computed: {
        filteredActivities: function () {
            if (this.search === "") return this.activities;

            return this.activities.filter(a => {
                return a.activity_name.toLowerCase().includes(this.search.toLowerCase());
            });
        },
    },
    methods: {
        /** Get activities objects from the Grand Set. */
        getActivities: function () {
            const promiseActivities = this.grandSet.activities.map(activity => {
                return axios.get(`/grandset/api/activity/${activity}/`);
            });

            Promise.all(promiseActivities)
                .then(resps => {
                    this.activities = resps.map(r => r.data);
                });
        },
        /** Get Grand Set serie id. */
        getGrandSetSerie: function () {
            axios.get(`/grandset/api/grandset_series/?grand_set=${this.grandSetId}`)
                .then(resp => {
                    if (!resp.data.results) return;

                    this.grandSetSerieId = resp.data.results[0].id;
                });
        }
    },
    mounted: function () {
        console.log(this.grandSetId);
        // eslint-disable-next-line no-undef
        this.grandSet = last_grandset && last_grandset.id == this.grandSetId ? last_grandset : null;
        this.getGrandSetSerie();
        if (this.grandSet) {
            this.getActivities();
        } else {
            // First get grand set data.
            axios.get(`/grandset/api/grand_set/${this.grandSetId}/`)
                .then(resp => {
                    this.grandSet = resp.data;
                    this.getActivities();
                });
        }
        
    },
    components: {
        ActivityOverview
    }
};
</script>
