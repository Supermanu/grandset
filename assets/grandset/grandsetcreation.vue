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
            <b-row class="sticky-top p-2 first-line">
                <b-col>
                    <b-btn to="/grand_set_series/">
                        Retour aux séries
                    </b-btn>
                    <b-btn
                        v-if="!series && objectId !== '-1'"
                        variant="secondary"
                        :to="`/grand_set/${objectId}/`"
                    >
                        Vers le Grand Set
                    </b-btn>
                </b-col>
                <b-col
                    cols="2"
                    align-self="end"
                >
                    <b-btn
                        @click="submit"
                        variant="primary"
                        :disabled="!hasChanged"
                    >
                        Sauver
                    </b-btn>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <b-form-row v-if="series">
                        <b-col>
                            <b-form-group
                                label="Nom de la série"
                                :state="inputStates.name"
                            >
                                <b-form-input
                                    type="text"
                                    v-model="name"
                                    @update="hasChanged = true"
                                />
                                <span slot="invalid-feedback">{{ errorMsg("name") }}</span>
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                    <b-form-row v-if="series">
                        <b-col>
                            <b-form-group
                                label="Date début"
                                :state="inputStates.date_start"
                            >
                                <b-form-input
                                    type="date"
                                    v-model="date_start"
                                    @update="hasChanged = true"
                                />
                                <span slot="invalid-feedback">{{ errorMsg("date_start") }}</span>
                            </b-form-group>
                        </b-col>
                        <b-col>
                            <b-form-group
                                label="Date fin"
                                :state="inputStates.date_end"
                            >
                                <b-form-input
                                    type="date"
                                    v-model="date_end"
                                    @update="hasChanged = true"
                                />
                                <span slot="invalid-feedback">{{ errorMsg("date_end") }}</span>
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                    <b-form-row v-else>
                        <b-col>
                            <b-form-group
                                label="Date début"
                                :state="inputStates.date"
                            >
                                <b-form-input
                                    type="date"
                                    v-model="date"
                                    @update="hasChanged = true"
                                />
                                <span slot="invalid-feedback">{{ errorMsg("date") }}</span>
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                </b-col>
            </b-row>
            <div
                v-if="ready && series"
                class="mb-4"
            >
                <b-row>
                    <b-col>
                        <h5>Grand Sets de la série</h5>
                    </b-col>
                </b-row>
                <b-row
                    class="mb-2"
                >
                    <b-col>
                        <b-btn
                            :to="`/grand_set_creation/${objectId}/-1/`"
                            variant="success"
                            :disabled="objectId === '-1'"
                        >
                            <b-icon
                                icon="plus"
                            />
                            <span v-if="objectId !== '-1'">
                                Ajouter un grand set
                            </span>
                            <span v-else>
                                Enregistrer avant d'ajouter un grand set
                            </span>
                        </b-btn>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
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
                                            :to="`/grand_set/${gs.id}/`"
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
            </div>
            <b-row
                v-if="ready"
                class="mb-4"
            >
                <b-col>
                    <activity-selection
                        v-model="activities"
                        @update="hasChanged = true"
                    />
                </b-col>
            </b-row>
            <b-row v-if="ready && series">
                <b-col>
                    <group-selection
                        v-model="groups"
                        @update="hasChanged = true"
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

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

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
        grandSetSeriesId: {
            type: String,
            default: "-1"
        }
    },
    data: function () {
        return {
            name: "",
            date: null,
            date_start: null,
            date_end: null,
            activities: [],
            groups: [],
            grandSets: [],
            grandSetSeries: null,
            ready: false,
            hasChanged: false,
            inputStates: {
                name: null,
                date: null,
                date_start: null,
                date_end: null,
                activities: null,
                groups: null,
            },
            errors: {},
        };
    },
    components: {
        ActivitySelection,
        GroupSelection,
    },
    watch: {
        /**
         * Handle returned errors states.
         * 
         * @param {Object} newErrors Errors states with error message.
         */
        errors: function (newErrors) {
            Object.keys(this.inputStates).forEach(key => {
                if (key in newErrors) {
                    this.inputStates[key] = newErrors[key].length == 0;
                } else {
                    this.inputStates[key] = null;
                }
            });
        },
        series: function () {
            this.initComponent();
        }
    },
    methods: {
        /** 
         * Assign text error if any.
         * 
         * @param {String} err Field name.
         */
        errorMsg(err) {
            if (err in this.errors) {
                return this.errors[err][0];
            } else {
                return "";
            }
        },
        /** Submit Grand Set Serie data to the server. */
        submit: function () {
            const data = this.series ? {
                name: this.name,
                date_start: this.date_start,
                date_end: this.date_end,
                activities_id: this.activities.map(a => a.id),
                groups_id: this.groups.map(g => g.id),
            } :
                {
                    date: this.date,
                    activities_id: this.activities.map(a => a.id),
                    grand_set_series_id: this.grandSetSeriesId
                };

            const isNewObj = this.objectId === "-1";
            let url = "/grandset/api/grandset";
            url = this.series ? url + "_series/" : url + "/";
            if (!isNewObj) url += `${this.objectId}/`;

            const send = isNewObj ? axios.post : axios.put;
            send(url, data, token)
                .then(resp => {
                    if (isNewObj && !this.series) {
                        const path = `/grand_set/${resp.data.id}/`;
                        this.$router.push(path, () => {
                            this.$root.$bvToast.toast("Les données ont bien été sauvegardées", {
                                variant: "success",
                                noCloseButton: true,
                            });
                        });
                    } else if (isNewObj) {
                        const path = `/grand_set_series_creation/${resp.data.id}/`;
                        this.$router.push(path, () => {
                            this.$root.$bvToast.toast("Les données ont bien été sauvegardées", {
                                variant: "success",
                                noCloseButton: true,
                            });
                        });
                    } else {
                        this.$root.$bvToast.toast("Les données ont bien été sauvegardées", {
                            variant: "success",
                            noCloseButton: true,
                        });
                    }
                    this.hasChanged = false;
                })
                .catch(err => {
                    this.errors = err.response.data;
                });
        },
        initComponent: function () {
            if (this.series) {
                if (this.objectId) {
                    Promise.all([
                        axios.get(`/grandset/api/grandset_series/${this.objectId}`),
                        axios.get(`/grandset/api/grandset/?grand_set_series=${this.objectId}`)
                    ])
                        .then(resps => {
                            this.name = resps[0].data.name;
                            this.date_start = resps[0].data.date_start;
                            this.date_end = resps[0].data.date_end;
                            this.activities = resps[0].data.activities;
                            this.groups = resps[0].data.groups;
                            this.grandSets = resps[1].data.results;
                            this.ready = true;
                        });
                } else {
                    this.ready = true;
                }
            } else {
                if (this.objectId !== "-1") {
                    axios.get(`/grandset/api/grandset/${this.objectId}/`)
                        .then(resp => {
                            this.date = resp.data.date;
                            this.activities = resp.data.activities;
                            this.groups = resp.data.groups;
                            this.grandSetSeries = resp.data.grand_set_series;

                            this.ready = true;
                        });
                } else {
                    axios.get(`/grandset/api/grandset_series/${this.grandSetSeriesId}/`)
                        .then(resp => {
                            this.grandSetSeries = resp.data;
                            this.activities = this.grandSetSeries.activities;
                            this.ready = true;
                        });
                }
            }
        }
    },
    mounted: function () {
        this.initComponent();
    },
    beforeRouteLeave (to, from, next) {
        if (this.hasChanged && this.objectId !== "-1") {
            if (!confirm("Des données n'ont pas été enregistrées, êtes-vous sûr de vouloir quitter la page ?")) {
                next(false);
            }
        }
        next();
    }
};
</script>

<style>
.first-line {
    background-color: rgba(255, 255, 255, 0.877);
    border-bottom: 2px rgb(180, 180, 180) solid;
}
</style>
