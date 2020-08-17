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
                <b-col md="4">
                    <h3>{{ date }} : {{ grandSet.grand_set_series.name }}</h3>
                </b-col>
                <b-col md="5">
                    <b-input-group class="mb-2">
                        <b-form-input
                            placeholder="Une activité, un groupe ou un élève"
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
                    md="2"
                    align-h="end"
                >
                    <b-dropdown
                        variant="outline-secondary"
                        block
                        no-caret
                    >
                        <template v-slot:button-content>
                            <b-icon icon="list" />
                            Options
                        </template>
                        <b-dropdown-item
                            :to="`/grand_set_creation/${grandSet.grand_set_series.id}/${grandSetId}/`"
                        >
                            Gestion des activités
                        </b-dropdown-item>
                        <b-dropdown-item
                            :to="`/grand_set_series_creation/${grandSet.grand_set_series.id}/`"
                        >
                            Gestion de la série
                        </b-dropdown-item>
                        <b-dropdown-item
                            :to="`/grand_set_series/`"
                        >
                            Liste des séries
                        </b-dropdown-item>
                    </b-dropdown>
                </b-col>
            </b-row>
            <b-row v-if="grandSet">
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
import Moment from "moment";
Moment.locale("fr");

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
            search: "",
        };
    },
    computed: {
        filteredActivities: function () {
            if (this.search === "") return this.grandSet.activities;

            return this.grandSet.activities.filter(a => {
                const activityOverview = this.$refs.activities.find(aO => aO.activity.id === a.id);
                const groupAndStudSearch = activityOverview ? activityOverview.hasGroupOrStudent(this.search) : false;
                const hasActivity = a.activity_name.toLowerCase().includes(this.search.toLowerCase());
                return groupAndStudSearch || hasActivity;
                
            });
        },
        date: function () {
            if (!this.grandSet) return "";

            return Moment(this.grandSet.date).format("DD/MM/YY");
        }
    },
    mounted: function () {
        // eslint-disable-next-line no-undef
        this.grandSet = last_grandset && last_grandset.id == this.grandSetId ? last_grandset : null;
        if (!this.grandSet) {
            // First get grand set data.
            axios.get(`/grandset/api/grandset/${this.grandSetId}/`)
                .then(resp => {
                    this.grandSet = resp.data;
                });
        }
        
    },
    components: {
        ActivityOverview
    }
};
</script>

<style>
h3 {
    font-size: 1.1em;
    font-weight: bold;
    padding-top: 0.5em;
}
</style>
