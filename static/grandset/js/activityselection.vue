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
        <b-overlay :show="loading">
            <b-row>
                <b-col>
                    <h5>Activités disponibles</h5>
                    <b-input-group>
                        <b-form-input
                            v-model="search"
                            placeholder="Rechercher une activité"
                        />

                        <template #append>
                            <b-button
                                v-if="search"
                                size="sm"
                                variant="outline-danger"
                                @click="search = ''"
                            >
                                <small>
                                    <b-icon icon="backspace" />
                                </small>
                            </b-button>
                        </template>
                        <template #prepend>
                            <b-input-group-text>
                                <b-icon icon="search" />
                            </b-input-group-text>
                        </template>
                    </b-input-group>
                    <b-list-group class="pt-1">
                        <b-list-group-item
                            v-for="(activity, index) in filteredActivities"
                            :key="activity.id"
                            class="d-flex justify-content-between"
                        >
                            {{ activity.activity_name }}
                            <span>
                                <b-btn
                                    size="sm"
                                    variant="primary"
                                    @click="addActivity(index)"
                                >
                                    <b-icon icon="arrow-right" />
                                </b-btn>
                            </span>
                        </b-list-group-item>
                    </b-list-group>
                </b-col>
                <b-col>
                    <h5>Activités sélectionnées</h5>
                    <div class="text-right">
                        <b-btn
                            v-b-modal.creation-activity-modal
                            variant="outline-success"
                        >
                            <b-icon icon="plus" />
                            Créer une activité
                        </b-btn>
                    </div>
                    <b-list-group class="pt-1">
                        <b-list-group-item
                            v-for="(activity, index) in modelValue"
                            :key="activity.id"
                            class="d-flex justify-content-between"
                        >
                            <span>
                                <b-btn
                                    size="sm"
                                    variant="primary"
                                    @click="removeActivity(index)"
                                >
                                    <b-icon icon="arrow-left" />
                                </b-btn>
                            </span>
                            {{ activity.activity_name }}
                            <b-btn
                                size="sm"
                                variant="outline-secondary"
                                @click="openModal(activity)"
                            >
                                <b-icon icon="pencil-square" />
                            </b-btn>
                        </b-list-group-item>
                    </b-list-group>
                </b-col>
            </b-row>
        </b-overlay>
        <b-modal
            id="creation-activity-modal"
            size="lg"
            cancel-title="Annuler"
            :ok-title="'id' in newActivity ? 'Modifier' : 'Ajouter'"
            @ok="submit"
            @hidden="resetNewActivity"
        >
            <b-form-row>
                <b-col>
                    <b-form-group
                        label="Nom de l'activité"
                        :state="inputStates.activity_name"
                    >
                        <b-input
                            v-model="newActivity.activity_name"
                            type="text"
                        />
                        <template #invalid-feedback>
                            {{ errorMsg("activity_name") }}
                        </template>
                    </b-form-group>
                    <b-form-group
                        label="Nombre maximum de participants"
                        description="Le nombre de groupe maximum que l'activité peut acceuillir."
                        :state="inputStates.max_participant"
                    >
                        <b-input-group>
                            <b-input-group-prepend>
                                <b-input-group-text>
                                    <b-icon icon="people" />
                                </b-input-group-text>
                            </b-input-group-prepend>

                            <b-form-input
                                v-model="newActivity.max_participant"
                                type="number"
                                min="1"
                                step="1"
                            />
                        </b-input-group>
                        <template #invalid-feedback>
                            {{ errorMsg("max_participant") }}
                        </template>
                    </b-form-group>
                    <b-form-group
                        label="Nombre de participation recommandé"
                        description="Le nombre de participation que chaque groupe devrait faire."
                    >
                        <b-input-group>
                            <b-input-group-prepend>
                                <b-input-group-text>
                                    <b-icon icon="reply-all" />
                                </b-input-group-text>
                            </b-input-group-prepend>

                            <b-form-input
                                v-model="newActivity.recommended_participation"
                                type="number"
                                min="1"
                                step="1"
                            />
                        </b-input-group>
                        <template #invalid-feedback>
                            {{ errorMsg("recommended_participation") }}
                        </template>
                    </b-form-group>
                    <b-form-group
                        label="Temps moyen de l'activité"
                        description="Le temps moyen qu'un groupe met pour faire l'activité."
                        :state="inputStates.average_time"
                    >
                        <b-input-group>
                            <b-input-group-prepend>
                                <b-input-group-text>
                                    <b-icon icon="clock" />
                                </b-input-group-text>
                            </b-input-group-prepend>
                            <b-form-input
                                v-model="newActivity.average_time"
                                type="number"
                                min="15"
                                step="5"
                            />
                            <b-input-group-append>
                                <b-input-group-text>
                                    minutes
                                </b-input-group-text>
                            </b-input-group-append>
                        </b-input-group>
                        <template #invalid-feedback>
                            {{ errorMsg("average_time") }}
                        </template>
                    </b-form-group>
                    <b-form-group
                        label="Responsable(s)"
                        :state="inputStates.responsibles"
                    >
                        <multiselect
                            id="responsible"
                            v-model="newActivity.responsibles"
                            :internal-search="false"
                            :options="responsibleOptions"
                            placeholder="Un ou plusieurs responsables"
                            select-label=""
                            selected-label="Sélectionné"
                            deselect-label="Cliquer dessus pour enlever"
                            label="display"
                            track-by="matricule"
                            :show-no-options="false"
                            multiple
                            @search-change="getResponsible"
                        >
                            <template #noResult>
                                Aucun responsable trouvé.
                            </template>
                            <template #noOptions />
                        </multiselect>
                        <template #invalid-feedback>
                            {{ errorMsg('responsibles') }}
                        </template>
                    </b-form-group>
                    <b-form-group
                        label="Description"
                        :state="inputStates.description"
                    >
                        <text-editor
                            v-model="newActivity.description"
                        />
                        <template #invalid-feedback>
                            {{ errorMsg("description") }}
                        </template>
                    </b-form-group>
                </b-col>
            </b-form-row>
        </b-modal>
    </div>
</template>

<script>
import axios from "axios";

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

import TextEditor from "@s:core/js/common/text_editor.vue";

import { grandsetStore } from "./stores/index.js";

import {getPeopleByName} from "@s:core/js/common/search.js";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    components: {
        TextEditor,
        Multiselect
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
        /* The selected activities. */
        modelValue: {
            type: Array,
            default: () => [],
        },
    },
    data: function () {
        return {
            availActivities: [],
            search: "",
            newActivity: {
                activity_name: "",
                description: "",
                max_participant: 5,
                recommended_participation: 8,
                average_time: 20,
                responsibles: [],
            },
            responsibleOptions: [],
            searchId: -1,
            errors: {},
            /** List of input error states. */
            inputStates: {
                activity_name: null,
                description: null,
                max_participant: null,
                recommended_participation: null,
                average_time: null,
                responsibles: null,
            },
            loading: true,
            store: grandsetStore(),
        };
    },
    computed: {
        filteredActivities() {
            if (this.search === "") return this.availActivities;

            return this.availActivities.filter(a => {
                return a.activity_name.toLowerCase().includes(this.search.toLowerCase());
            });
        },
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
            this.initActivities();
        }
    },
    mounted () {
        this.initActivities();
    },
    methods: {
        initActivities: function () {
            // Load all activities available.
            axios.get("/grandset/api/activity/")
                .then(resp => {
                    const selectedActivities = resp.data.results.filter(r => this.modelValue.includes(r.id));
                    this.availActivities = resp.data.results.filter(a => !this.modelValue.includes(a.id));

                    this.$emit("update:modelValue", selectedActivities);
                    this.$emit("update");
                    this.loading = false;
                });
        },
        openModal: function (activity) {
            const modalActivity = Object.assign({}, activity);
            modalActivity.average_time = modalActivity.average_time.slice(3,5);
            this.newActivity = modalActivity;
            this.$bvModal.show("creation-activity-modal");
        },
        getResponsible: function (searchQuery) {
            this.searchId += 1;
            let currentSearch = this.searchId;

            const teachings = this.store.settings.teachings.filter(
                // eslint-disable-next-line no-undef
                value => user_properties.teaching.includes(value));
            getPeopleByName(searchQuery, teachings, "responsible")
                .then( (resp) => {
                // Avoid that a previous search overwrites a faster following search results.
                    if (this.searchId !== currentSearch)
                        return;
                    this.responsibleOptions = resp.data;
                // this.searching = false;
                })
                .catch( (err) => {
                    alert(err);
                // this.searching = false;
                });
        },
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
        submit: function (evt) {
            evt.preventDefault();

            const data = Object.assign({}, this.newActivity);
            data.responsibles_id = data.responsibles.map(r => r.pk);
            data.average_time = `${data.average_time}:00`;

            const isModif = "id" in this.newActivity;
            let url = "/grandset/api/activity/";
            if (isModif) url += `${this.newActivity.id}/`;
            const send = isModif ? axios.put : axios.post;

            send(url, data, token).then(resp => {
                if (!isModif) {
                    console.log(resp.data);
                    this.$emit("update:modelValue", this.modelValue.concat(resp.data));
                    this.$emit("update:state");
                } else {
                    const updatedActivities = this.modelValue.map(a => {
                        if (a.id == resp.data.id) a = resp.data;
                        return a;
                    });
                    this.$emit("update:modelValue", updatedActivities);
                }
                this.$nextTick(() => {
                    this.$bvModal.hide("creation-activity-modal");
                });
            })
                .catch(err => {
                    this.errors = err.response.data;
                });
        },
        addActivity: function (index) {
            const activity = this.availActivities.splice(index, 1);
            this.$emit("update:modelValue", this.modelValue.concat(activity));
            this.$emit("update:state");
        },
        removeActivity: function (index) {
            this.availActivities.unshift(this.modelValue[index]);
            this.$emit("update:modelValue", this.modelValue.filter((v, i) => i != index));
            this.$emit("update:state");
        },
        resetNewActivity: function () {
            Object.assign(this.$data.newActivity, this.$options.data().newActivity);
            if ("id" in this.newActivity) delete this.newActivity.id;
        }
    },
};
</script>
