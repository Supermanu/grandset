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
        <BContainer>
            <BRow>
                <BCol>
                    <h3>
                        Préparer
                        {{ series ? "une série" : "un" }}
                        {{ store.settings.grand_set_name }}
                    </h3>
                </BCol>
            </BRow>
            <BRow class="sticky-top p-2 first-line">
                <BCol>
                    <BButton to="/grand_set_series/">
                        Retour aux séries
                    </BButton>
                    <BButton
                        v-if="!series && objectId !== '-1'"
                        variant="secondary"
                        :to="`/grand_set/${objectId}/`"
                    >
                        Vers le Grand Set
                    </BButton>
                </BCol>
                <BCol
                    cols="2"
                    align-self="end"
                >
                    <BButton
                        variant="primary"
                        :disabled="!hasChanged"
                        @click="submit"
                    >
                        Sauver
                    </BButton>
                </BCol>
            </BRow>
            <BRow>
                <BCol>
                    <BFormRow v-if="series">
                        <BCol>
                            <BFormGroup
                                label="Nom de la série"
                                :state="inputStates.name"
                            >
                                <BFormInput
                                    v-model="name"
                                    type="text"
                                    @update="hasChanged = true"
                                />
                                <template #invalid-feedback>
                                    {{ errorMsg("name") }}
                                </template>
                            </BFormGroup>
                        </BCol>
                    </BFormRow>
                    <BFormRow v-if="series">
                        <BCol>
                            <BFormGroup
                                label="Date début"
                                :state="inputStates.date_start"
                            >
                                <BFormInput
                                    v-model="date_start"
                                    type="date"
                                    @update="hasChanged = true"
                                />
                                <template #invalid-feedback>
                                    {{ errorMsg("date_start") }}
                                </template>
                            </BFormGroup>
                        </BCol>
                        <BCol>
                            <BFormGroup
                                label="Date fin"
                                :state="inputStates.date_end"
                            >
                                <BFormInput
                                    v-model="date_end"
                                    type="date"
                                    @update="hasChanged = true"
                                />
                                <template #invalid-feedback>
                                    {{ errorMsg("date_end") }}
                                </template>
                            </BFormGroup>
                        </BCol>
                    </BFormRow>
                    <BFormRow v-else>
                        <BCol>
                            <BFormGroup
                                label="Date début"
                                :state="inputStates.date"
                            >
                                <BFormInput
                                    v-model="date"
                                    type="date"
                                    @update="hasChanged = true"
                                />
                                <template #invalid-feedback>
                                    {{ errorMsg("date") }}
                                </template>
                            </BFormGroup>
                        </BCol>
                    </BFormRow>
                </BCol>
            </BRow>
            <div
                v-if="ready && series"
                class="mb-4"
            >
                <BRow>
                    <BCol>
                        <h5>{{ store.settings.grand_set_name }} de la série</h5>
                    </BCol>
                </BRow>
                <BRow
                    class="mb-2"
                >
                    <BCol>
                        <BButton
                            :to="`/grand_set_creation/${objectId}/-1/`"
                            variant="success"
                            :disabled="objectId === '-1'"
                        >
                            <IBiPlus />
                            <span v-if="objectId !== '-1'">
                                Ajouter un {{ store.settings.grand_set_name }}
                            </span>
                            <span v-else>
                                Enregistrer avant d'ajouter un {{ store.settings.grand_set_name }}
                            </span>
                        </BButton>
                    </BCol>
                </BRow>
                <BRow>
                    <BCol>
                        <BCard
                            v-for="gs in grandSets"
                            :key="gs.id"
                            no-body
                        >
                            <BCardText class="p-1">
                                <BRow>
                                    <BCol>
                                        <strong>{{ gs.date }}</strong>
                                    </BCol>
                                    <BCol class="text-right">
                                        <BButton
                                            :to="`/grand_set/${gs.id}/`"
                                            size="sm"
                                            variant="outline-primary"
                                        >
                                            Voir
                                            <IBiChevronRight />
                                        </BButton>
                                    </BCol>
                                </BRow>
                            </BCardText>
                        </BCard>
                    </BCol>
                </BRow>
            </div>
            <BRow
                v-if="ready"
                class="mb-4"
            >
                <BCol>
                    <activity-selection
                        v-if="ready"
                        :model-value="activities"
                        :series="series"
                        @update:model-value="newValue => activities = newValue"
                        @update:state="hasChanged = true"
                    />
                </BCol>
            </BRow>
            <BRow v-if="series">
                <BCol>
                    <group-selection
                        v-if="ready"
                        :model-value="groups"
                        @update:model-value="newValue => groups = newValue"
                        @update:state="hasChanged = true"
                    />
                </BCol>
            </BRow>
        </BContainer>
    </div>
</template>

<script>
import axios from "axios";

import ActivitySelection from "./activityselection.vue";
import GroupSelection from "./groupselection.vue";

import { grandsetStore } from "./stores/index.js";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

export default {
    components: {
        ActivitySelection,
        GroupSelection,
    },
    beforeRouteLeave(to, from, next) {
        if (this.hasChanged && this.objectId !== "-1") {
            if (!confirm("Des données n'ont pas été enregistrées, êtes-vous sûr de vouloir quitter la page ?")) {
                next(false);
            }
        }
        next();
    },
    props: {
        series: {
            type: Boolean,
            default: true,
        },
        objectId: {
            type: String,
            default: "-1",
        },
        grandSetSeriesId: {
            type: String,
            default: "-1",
        },
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
            store: grandsetStore(),
        };
    },
    watch: {
        /**
         * Handle returned errors states.
         *
         * @param {Object} newErrors Errors states with error message.
         */
        errors: function (newErrors) {
            Object.keys(this.inputStates).forEach((key) => {
                if (key in newErrors) {
                    this.inputStates[key] = newErrors[key].length == 0;
                } else {
                    this.inputStates[key] = null;
                }
            });
        },
        series: function () {
            this.initComponent();
        },
    },
    mounted: function () {
        this.initComponent();
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
            const data = this.series
                ? {
                    name: this.name,
                    date_start: this.date_start,
                    date_end: this.date_end,
                    activities: this.activities.map(a => a.id),
                    groups: this.groups.map(g => g.id),
                }
                : {
                    date: this.date,
                    activities: this.activities.map(a => a.id),
                    grand_set_series_id: this.grandSetSeriesId,
                };

            const isNewObj = this.objectId === "-1";
            let url = "/grandset/api/grandset";
            url = this.series ? url + "_series/" : url + "/";
            if (!isNewObj) url += `${this.objectId}/`;

            const send = isNewObj ? axios.post : axios.put;
            send(url, data, token)
                .then((resp) => {
                    if (isNewObj && !this.series) {
                        const path = `/grand_set/${resp.data.id}/`;
                        this.$router.push(path).then(() => {
                            this.show({
                                body: "Les données ont bien été sauvegardées",
                                variant: "success",
                                noCloseButton: true,
                            });
                        });
                    } else if (isNewObj) {
                        const path = `/grand_set_series_creation/${resp.data.id}/`;
                        this.$router.push(path).then(() => {
                            this.show({
                                body: "Les données ont bien été sauvegardées",
                                variant: "success",
                                noCloseButton: true,
                            });
                        });
                    } else {
                        this.show({
                            body: "Les données ont bien été sauvegardées",
                            variant: "success",
                            noCloseButton: true,
                        });
                    }
                    this.hasChanged = false;
                })
                .catch((err) => {
                    this.errors = err.response.data;
                });
        },
        initComponent: function () {
            if (this.series) {
                if (Number(this.objectId) > 0) {
                    Promise.all([
                        axios.get(`/grandset/api/grandset_series/${this.objectId}`),
                        axios.get(`/grandset/api/grandset/?grand_set_series=${this.objectId}&ordering=-date`),
                    ])
                        .then((resps) => {
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
                console.log(this.objectId);
                if (this.objectId !== "-1") {
                    console.log("grandset one shot");
                    axios.get(`/grandset/api/grandset/${this.objectId}/`)
                        .then((resp) => {
                            this.date = resp.data.date;
                            this.activities = resp.data.activities;
                            console.log("oh", this.activities);
                            this.grandSetSeries = resp.data.grand_set_series;

                            this.ready = true;
                        });
                } else {
                    console.log("series…");
                    axios.get(`/grandset/api/grandset_series/${this.grandSetSeriesId}/`)
                        .then((resp) => {
                            this.grandSetSeries = resp.data;
                            this.activities = this.grandSetSeries.activities;
                            console.log(this.activities);
                            this.ready = true;
                        });
                }
            }
        },
    },
};
</script>

<style>
.first-line {
    background-color: rgba(255, 255, 255, 0.877);
    border-bottom: 2px rgb(180, 180, 180) solid;
}
</style>
