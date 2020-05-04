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
                    <b-input-group>
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
            </b-row>
            <b-row>
                <b-col>
                    <b-card-group columns>
                        <activity-overview
                            v-for="activity in filteredActivities"
                            :key="activity.id"
                            :activity="activity"
                            :grand-set="grandSet"
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
        grandSet: {
            type: String,
            default: "-1",
        }
    },
    data: function () {
        return {
            grandset: null,
            activities: [],
            search: "",
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
    mounted: function () {
        // eslint-disable-next-line no-undef
        this.grandset = last_grandset;
        if (this.grandset) {
            const promiseActivities = this.grandset.activities.map(activity => {
                return axios.get(`/grandset/api/activity/${activity}/`);
            });

            Promise.all(promiseActivities)
                .then(resps => {
                    this.activities = resps.map(r => r.data);
                });
        }
        
    },
    components: {
        ActivityOverview
    }
};
</script>
