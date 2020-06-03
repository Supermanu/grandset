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
        <b-row>
            <b-col>
                <h5>Activités disponibles</h5>
                <b-input-group>
                    <b-form-input
                        placeholder="Rechercher une activité"
                        v-model="search"
                    />

                    <template v-slot:append>
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
                    <template v-slot:prepend>
                        <b-input-group-text>
                            <b-icon icon="search" />
                        </b-input-group-text>
                    </template>
                </b-input-group>
                <b-list-group class="pt-1">
                    <b-list-group-item
                        button
                        v-for="(activity, index) in filteredActivities"
                        :key="activity.id"
                        @click="addActivity(index)"
                    >
                        {{ activity.activity_name }}
                    </b-list-group-item>
                </b-list-group>
            </b-col>
            <b-col>
                <h5>Activités sélectionnées</h5>
                <div class="text-right">
                    <b-btn
                        variant="outline-success"
                        v-b-modal.creation-modal
                    >
                        <b-icon icon="plus" />
                        Créer une activité
                    </b-btn>
                </div>
                <b-list-group class="pt-1">
                    <b-list-group-item
                        button
                        v-for="(activity, index) in value"
                        :key="activity.id"
                        @click="removeActivity(index)"
                    >
                        {{ activity.activity_name }}
                    </b-list-group-item>
                </b-list-group>
            </b-col>
        </b-row>
        <b-modal
            id="creation-modal"
            size="lg"
            cancel-title="Annuler"
            :ok-title="'id' in newActivity ? 'Modifier' : 'Ajouter'"
            @hidden="resetNewActivity"
        >
            <b-form-row>
                <b-col>
                    <b-form-group
                        label="Nom de l'activité"
                    >
                        <b-input
                            type="text"
                            v-model="newActivity.activity_name"
                        />
                    </b-form-group>
                    <b-form-group
                        label="Nombre maximum de participants"
                        description="Le nombre de groupe maximum que l'activité peut acceuillir."
                    >
                        <b-input-group>
                            <b-input-group-prepend>
                                <b-input-group-text>
                                    <b-icon icon="people" />
                                </b-input-group-text>
                            </b-input-group-prepend>

                            <b-form-input
                                type="number"
                                min="1"
                                step="1"
                                v-model="newActivity.max_participant"
                            />
                        </b-input-group>
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
                                type="number"
                                min="1"
                                step="1"
                                v-model="newActivity.recommended_participation"
                            />
                        </b-input-group>
                    </b-form-group>
                    <b-form-group
                        label="Temps moyen de l'activité"
                        description="Le temps moyen qu'un groupe met pour faire l'activité."
                    >
                        <b-input-group>
                            <b-input-group-prepend>
                                <b-input-group-text>
                                    <b-icon icon="clock" />
                                </b-input-group-text>
                            </b-input-group-prepend>
                            <b-form-input
                                type="number"
                                min="15"
                                step="5"
                                v-model="newActivity.average_time"
                            />
                            <b-input-group-append>
                                <b-input-group-text>
                                    minutes
                                </b-input-group-text>
                            </b-input-group-append>
                        </b-input-group>
                    </b-form-group>
                    <b-form-group
                        label="Description"
                    >
                        <quill-editor
                            v-model="newActivity.description"
                            :options="editorOptions"
                        />
                    </b-form-group>
                </b-col>
            </b-form-row>
        </b-modal>
    </div>
</template>

<script>
import axios from "axios";

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.min.css";

import {quillEditor} from "vue-quill-editor";
import "quill/dist/quill.core.css";
import "quill/dist/quill.snow.css";

export default {
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
        value: {
            type: Array,
            default: () => [],
        },
    },
    data() {
        return {
            availActivities: [],
            search: "",
            newActivity: {
                activity_name: "",
                description: "",
                max_participant: 5,
                recommended_participation: 8,
                average_time: 20,
            },
            editorOptions: {
                modules: {
                    toolbar: [
                        ["bold", "italic", "underline", "strike"],
                        ["blockquote"],
                        [{ "list": "ordered"}, { "list": "bullet" }],
                        [{ "indent": "-1"}, { "indent": "+1" }],
                        [{ "align": [] }],
                        ["clean"]
                    ]
                },
                placeholder: ""
            },
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
    methods: {
        addActivity(index) {
            const activity = this.availActivities.splice(index, 1);
            this.$emit("input", this.value.concat(activity));
        },
        removeActivity(index) {
            this.availActivities.unshift(this.value[index]);
            this.$emit("input", this.value.filter((v, i) => i != index));
        },
        resetNewActivity() {
            Object.assign(this.$data.newActivity, this.$options.data().newActivity);
        }
    },
    mounted () {
        if (this.series) {
            // Load all activities available.
            axios.get("/grandset/api/activity/")
                .then(resp => {
                    const selectedActivities = this.value.map(a => a.id);
                    this.availActivities = resp.data.results.filter(a => !selectedActivities.includes(a.id));
                });
        }
    },
    components: {
        quillEditor,
        Multiselect
    },
};
</script>
