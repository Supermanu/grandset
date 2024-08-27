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
    <b-overlay :show="loading">
        <b-row>
            <b-col>
                <h5>Groupes disponibles</h5>
                <b-input-group>
                    <b-form-input
                        v-model="search"
                        placeholder="Rechercher un groupe"
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
                <b-list-group
                    v-if="!loading"
                    class="pt-1"
                >
                    <b-list-group-item
                        v-for="(group, index) in filteredGroups"
                        :key="group.id"
                        class="d-flex justify-content-between"
                    >
                        <span class="mr-1">
                            <b-btn
                                size="sm"
                                variant="danger"
                                @click="deleteGroup(index)"
                            >
                                <b-icon icon="trash" />
                            </b-btn>
                        </span>
                        <span v-if="isNaN(group)">
                            {{ group.group_name }}:
                            <small>
                                {{ group.students_display.join(", ") }}
                            </small>
                        </span>
                        <span>
                            <b-btn
                                size="sm"
                                variant="primary"
                                @click="addGroup(index)"
                            >
                                <b-icon icon="arrow-right" />
                            </b-btn>
                        </span>
                    </b-list-group-item>
                </b-list-group>
            </b-col>
            <b-col>
                <h5>Groupes sélectionnés</h5>
                <div class="text-right">
                    <b-btn
                        v-b-modal.creation-group-modal
                        variant="outline-success"
                    >
                        <b-icon icon="plus" />
                        Créer un groupe
                    </b-btn>
                </div>
                <b-list-group
                    v-if="!loading"
                    class="pt-1"
                >
                    <b-list-group-item
                        v-for="(group, index) in modelValue"
                        :key="group.id"
                        class="d-flex justify-content-between"
                    >
                        <span>
                            <b-btn
                                size="sm"
                                variant="primary"
                                @click="removeGroup(index)"
                            >
                                <b-icon icon="arrow-left" />
                            </b-btn>
                        </span>
                        <span
                            v-if="isNaN(group)"
                            class="p-1"
                        > 
                            {{ group.group_name }}:
                            <small>
                                {{ group.students_display.join(", ") }}
                            </small>
                        </span>
                        <b-btn
                            size="sm"
                            variant="outline-secondary"
                            @click="openModal(group)"
                        >
                            <b-icon icon="pencil-square" />
                        </b-btn>
                    </b-list-group-item>
                </b-list-group>
            </b-col>
        </b-row>
        <b-modal
            id="creation-group-modal"
            size="lg"
            cancel-title="Annuler"
            :ok-title="'id' in newGroup ? 'Modifier' : 'Ajouter'"
            @ok="submit"
            @hidden="resetNewGroup"
        >
            <b-form-row>
                <b-col>
                    <b-form-group
                        label="Nom du groupe"
                        :state="inputStates.group_name"
                    >
                        <b-input
                            v-model="newGroup.group_name"
                            type="text"
                        />
                        <template #invalid-feedback>
                            {{ errorMsg("group_name") }}
                        </template>
                    </b-form-group>
                    <b-form-group
                        label="Étudiants"
                        :state="inputStates.students"
                    >
                        <multiselect
                            id="student"
                            v-model="newGroup.students"
                            :internal-search="false"
                            :options="studentOptions"
                            placeholder="Un ou plusieurs étudiants"
                            select-label=""
                            selected-label="Sélectionné"
                            deselect-label="Cliquer dessus pour enlever"
                            label="display"
                            track-by="matricule"
                            :show-no-options="false"
                            multiple
                            @search-change="getStudent"
                        >
                            <template #noResult>
                                Aucun étudiant trouvé.
                            </template>
                            <template #noOptions />
                        </multiselect>
                        <template #invalid-feedback>
                            {{ errorMsg('students') }}
                        </template>
                    </b-form-group>
                </b-col>
            </b-form-row>
        </b-modal>
    </b-overlay>
</template>

<script>
import axios from "axios";

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

import {getPeopleByName} from "@s:core/js/common/search.js";
import { grandsetStore } from "./stores/index.js";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    components: {
        Multiselect
    },
    props: {
        /** The selected groups */
        modelValue: {
            type: Array,
            default: () => []
        },
        series: {
            type: Boolean,
            default: true,
        },
    },
    data: function () {
        return {
            availGroup: [],
            search: "",
            newGroup: {
                group_name: "",
                students: [],
            },
            studentOptions: [],
            searchId: -1,
            errors: {},
            /** List of input error states. */
            inputStates: {
                group_name: null,
                students: null,
            },
            store: grandsetStore(),
            loading: true,
        };
    },
    computed: {
        filteredGroups: function () {
            if (this.search === "") return this.availGroup;

            return this.availGroup.filter(a => {
                console.log(a);
                const isInGroupName = a.group_name.toLowerCase().includes(this.search.toLowerCase());
                const isInStudentsName = a.students_display.join("").toLowerCase().includes(this.search.toLowerCase());
                return isInGroupName || isInStudentsName;
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
    },
    mounted () {
        if (this.series) {
            // Load all groups available.
            axios.get("/grandset/api/group/")
                .then(resp => {
                    const selectedGroups = resp.data.results.filter(r => this.modelValue.includes(r.id));
                    this.availGroup = resp.data.results.filter(r => !this.modelValue.includes(r.id));
                    this.$emit("update:modelValue", selectedGroups);
                    this.$emit("update:state");
                    this.loading = false;
                });
        }
    },
    methods: {
        openModal: function (group) {
            const modalGroup = Object.assign({}, group);
            this.newGroup = modalGroup;
            this.$bvModal.show("creation-group-modal");
        },
        getStudent: function (searchQuery) {
            this.searchId += 1;
            let currentSearch = this.searchId;

            const teachings = this.store.settings.teachings.filter(
                // eslint-disable-next-line no-undef
                value => user_properties.teaching.includes(value));
            getPeopleByName(searchQuery, teachings, "student")
                .then((resp) => {
                // Avoid that a previous search overwrites a faster following search results.
                    if (this.searchId !== currentSearch)
                        return;
                    this.studentOptions = resp.data.map(option => {
                        if (this.modelValue.find(group => group.students_id.includes(option.matricule))) {
                            option.$isDisabled = true;
                        }
                        return option;
                    });
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
        addGroup(groupToAdd) {
            const group = this.availGroup.splice(groupToAdd, 1);
            this.$emit("update:modelValue", this.modelValue.concat(group));
            this.$emit("update:state");
        },
        removeGroup(groupToRemove) {
            this.availGroup.unshift(this.modelValue[groupToRemove]);
            this.$emit("update:modelValue", this.modelValue.filter((v, i) => i != groupToRemove));
            this.$emit("update:state");
        },
        deleteGroup(groupToDelete) {
            const group = this.availGroup.splice(groupToDelete, 1);
            axios.delete(`/grandset/api/group/${group[0].id}/`, token);
        },
        submit: function (evt) {
            evt.preventDefault();

            const data = Object.assign({}, this.newGroup);
            data.students_id = data.students.map(r => r.matricule);

            const isModif = "id" in this.newGroup;
            let url = "/grandset/api/group/";
            if (isModif) url += `${this.newGroup.id}/`;
            const send = isModif ? axios.put : axios.post;

            send(url, data, token).then(resp => {
                if (!isModif) {
                    this.$emit("update:modelValue", this.modelValue.concat(resp.data));
                    this.$emit("update:state");
                } else {
                    const updatedGroups = this.modelValue.map(a => {
                        if (a.id == resp.data.id) a = resp.data;
                        return a;
                    });
                    this.$emit("update:modelValue", updatedGroups);
                }
                this.$nextTick(() => {
                    this.$bvModal.hide("creation-group-modal");
                });
            })
                .catch(err => {
                    this.errors = err.response.data;
                });
        },
        resetNewGroup: function () {
            Object.assign(this.$data.newGroup, this.$options.data().newGroup);
            if ("id" in this.newGroup) delete this.newGroup.id;
        }
    }
};
</script>
