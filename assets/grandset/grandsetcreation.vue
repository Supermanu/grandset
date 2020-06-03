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
                    <h3>
                        Préparer
                        {{ series ? "une série" : "un" }}
                        Grand Set
                    </h3>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <b-form-row>
                        <b-col>
                            <b-form-group
                                label="Nom de la série"
                            >
                                <b-form-input
                                    type="text"
                                    v-model="name"
                                />
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                    <b-form-row>
                        <b-col>
                            <b-form-group
                                label="Date début"
                            >
                                <b-form-input
                                    type="date"
                                    v-model="date_start"
                                />
                            </b-form-group>
                        </b-col>
                        <b-col>
                            <b-form-group
                                label="Date fin"
                            >
                                <b-form-input
                                    type="date"
                                    v-model="date_end"
                                />
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                </b-col>
            </b-row>
            <b-row
                v-if="ready && series"
                class="mb-4"
            >
                <b-col>
                    <h5>Grand Sets de la série</h5>
                    <b-card
                        no-body
                        v-for="gs in grandSets"
                        :key="gs.id"
                    >
                        <b-card-text class="p-1">
                            <b-row>
                                <b-col>
                                    <strong>{{ gs.date }}</strong>
                                </b-col>
                                <b-col class="text-right">
                                    <b-btn
                                        :to="`/grand_set/${gs.id}`"
                                        size="sm"
                                        variant="outline-primary"
                                    >
                                        Vers le grand set
                                        <b-icon
                                            icon="chevron-right"
                                        />
                                    </b-btn>
                                </b-col>
                            </b-row>
                        </b-card-text>
                    </b-card>
                </b-col>
            </b-row>
            <b-row v-if="ready">
                <b-col>
                    <activity-selection
                        v-model="activities"
                    />
                </b-col>
            </b-row>
            <b-row v-if="ready">
                <b-col>
                    <group-selection
                        v-model="groups"
                    />
                </b-col>
            </b-row>
        </b-container>
    </div>
</template>

<script>
import axios from "axios";

import ActivitySelection from "./activityselection.vue";
import GroupSelection from "./groupselection.vue";

export default {
    props: {
        series: {
            type: Boolean,
            default: true
        },
        objectId: {
            type: String,
            default: "-1"
        },
    },
    data() {
        return {
            name: "",
            date_start: null,
            date_end: null,
            activities: [],
            groups: [],
            grandSets: [],
            ready: false,
        };
    },
    components: {
        ActivitySelection,
        GroupSelection,
    },
    mounted () {
        if (this.series) {
            if (this.objectId) {
                axios.get(`/grandset/api/grandset_series/${this.objectId}`)
                    .then(resp => {
                        this.activities = resp.data.activities;
                        this.groups = resp.data.groups;
                        this.grandSets = resp.data.grand_sets;
                        this.ready = true;
                    });
            } else {
                this.ready = true;
            }
        }
    },
};
</script>
