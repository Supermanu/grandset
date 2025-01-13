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
    <BContainer>
        <BRow
            v-if="grandSet"
            class="justify-content-md-center m-2"
        >
            <BCol md="4">
                <h3>{{ date }} : {{ grandSet.grand_set_series.name }}</h3>
            </BCol>
            <BCol md="5">
                <BInputGroup class="mb-2">
                    <BFormInput
                        v-model="search"
                        placeholder="Une activité, un groupe ou un élève"
                    />

                    <template #append>
                        <BInputGroupText>
                            <IBiSearch />
                        </BInputGroupText>
                    </template>
                </BInputGroup>
            </BCol>
            <BCol
                md="2"
                align-h="end"
            >
                <BDropdown
                    variant="outline-secondary"
                    block
                    no-caret
                >
                    <template #button-content>
                        <IBiList />
                        Options
                    </template>
                    <BDropdownItem
                        :to="`/grand_set_creation/${grandSet.grand_set_series.id}/${grandSetId}/`"
                    >
                        Gestion des activités
                    </BDropdownItem>
                    <BDropdownItem
                        :to="`/grand_set_series_creation/${grandSet.grand_set_series.id}/`"
                    >
                        Gestion de la série
                    </BDropdownItem>
                    <BDropdownItem
                        :to="`/grand_set_series/`"
                    >
                        Liste des séries
                    </BDropdownItem>
                </BDropdown>
            </BCol>
        </BRow>
        <BRow v-if="grandSet">
            <BCol>
                <BCardGroup columns>
                    <activity-overview />
                    <activity-overview
                        v-for="activity in filteredActivities"
                        :key="activity.id"
                        ref="activities"
                        :activity="activity"
                    />
                </BCardGroup>
            </BCol>
        </BRow>
    </BContainer>
</template>

<script>
import axios from "axios";
import Moment from "moment";
Moment.locale("fr");

import ActivityOverview from "./activityoverview.vue";

export default {
    components: {
        ActivityOverview
    },
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
        Promise.all([
            axios.get(`/grandset/api/grandset/${this.grandSetId}/`),
            axios.get("/grandset/api/activity/")
        ]).then(resps => {
            resps[0].data.activities = resps[1].data.results;
            this.grandSet = resps[0].data;

        });
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
