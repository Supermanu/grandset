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
                    <h2>Évalution des élèves</h2>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <b-btn @click="$router.go(-1)">
                        Retour
                    </b-btn>
                </b-col>
            </b-row>
            <b-overlay
                :show="loading"
                rounded="sm"
            >
                <b-row
                    v-if="!loading"
                    class="mt-4"
                >
                    <b-col>
                        <b-form-group
                            :label="`Évaluation de ${group ? group.group_name : student.display}`"
                            label-cols-sm="4"
                            label-align-sm="center"
                            label-class="font-weight-bold"
                            :description="group ? `Évaluer l'ensemble du groupe.
                                Si nécessaire, vous pouvez évaluer individuellement ci-dessous.`: ''"
                        >
                            <div v-if="useCompetencies">
                                <competence-evaluation
                                    v-for="comp in activity.competence"
                                    :key="comp.id"
                                    v-model="generalEval[comp.id]"
                                    :comp-name="comp.name"
                                    label-cols-md="4"
                                    label-align-md="right"
                                    @input="updateIndividual(generalEval[comp.id], comp.id)"
                                />
                            </div>
                            <div v-else>
                                <b-input-group
                                    :append="'/ ' + store.settings.max_points"
                                >
                                    <b-form-input
                                        v-model="generalEval"
                                        type="number"
                                        step="0.01"
                                        min="0"
                                        :max="store.settings.max_points"
                                        @input="updateIndividual"
                                    />
                                </b-input-group>
                            </div>
                        </b-form-group>
                        <b-card
                            v-if="group"
                            bg-variant="light"
                        >
                            <b-form-group
                                label-cols-lg="3"
                                :label="group.group_name"
                                label-size="lg"
                                label-class="font-weight-bold pt-0"
                                class="mb-0"
                            >
                                <b-form-group 
                                    v-for="(stud, index) in students"
                                    :key="stud.matricule"
                                    label-cols-sm="3"
                                    label-align-sm="right"
                                >
                                    <slot name="label">
                                        <b-form-checkbox
                                            v-model="individualEval[index]"
                                            switch
                                            class="mr-n2"
                                        >
                                            {{ students[index].display }}
                                        </b-form-checkbox>
                                    </slot>
                                    <div v-if="useCompetencies">
                                        <competence-evaluation
                                            v-for="comp in activity.competence"
                                            :key="comp.id"
                                            v-model="evaluation[index][comp.id]"
                                            :comp-name="comp.name"
                                            label-cols-md="4"
                                            label-align-md="right"
                                            :disabled="!individualEval[index]"
                                        />
                                    </div>
                                    <div v-else>
                                        <b-input-group
                                            :append="'/ ' + store.settings.max_points"
                                        >
                                            <b-form-input
                                                v-model="evaluation[index]"
                                                type="number"
                                                step="0.01"
                                                min="0"
                                                :max="store.settings.max_points"
                                                :readonly="!individualEval[index]"
                                            />
                                        </b-input-group>
                                    </div>
                                </b-form-group>
                            </b-form-group>
                        </b-card>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col class="text-right mt-2">
                        <b-btn
                            variant="primary"
                            @click="sendData"
                        >
                            Soumettre
                        </b-btn>
                    </b-col>
                </b-row>
            </b-overlay>
        </b-container>
    </div>
</template>

<script>
import axios from "axios";

import CompetenceEvaluation from "./compeval.vue";

import { grandsetStore } from "./stores/index.js";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    components: {
        CompetenceEvaluation
    },
    props: {
        activityLogId: {
            type: String,
            default: "-1"
        },
        groupId: {
            type: String,
            default: "-1"
        },
        studentId: {
            type: String,
            default: "-1"
        }
    },
    data: function () {
        return {
            useCompetencies: false,
            activityLog: null,
            activity: null,
            group: null,
            student: null,
            activityEvaluation: [],
            loading: true,
            individualEval: [],
            evaluation: [],
            generalEval: null,
            store: grandsetStore(),
        };
    },
    computed: {
        students: function () {
            if (!this.group) return [];

            return this.group.students.filter(s => !this.activityLog.missing_student.includes(s.matricule));
        }
    },
    mounted: function () {
        if (this.activityLogId === "-1") return;

        const isGroup = this.groupId !== "-1";
        const dataProm = [
            axios.get(`/grandset/api/activity_log/${this.activityLogId}/`),
            axios.get(`/grandset/api/activity_evaluation/?activity_log=${this.activityLogId}`)
        ];
        if (isGroup) {
            dataProm.push(axios.get(`/grandset/api/group/${this.groupId}/`));
        } else {
            dataProm.push(axios.get(`/annuaire/api/student/${this.studentId}/`));
        }

        Promise.all(dataProm)
            .then(resps => {
                this.activityLog = resps[0].data;

                const hasPreviousEval = resps[1].data.count > 0;
                const students = isGroup ?
                    resps[2].data.students.filter(s => !this.activityLog.missing_student.includes(s.matricule))
                    : [this.student];
                this.individualEval = students
                    .filter(s => !this.activityLog.missing_student.includes(s.matricule))
                    .map(() => hasPreviousEval);

                axios.get(`/grandset/api/activity/${this.activityLog.activity}/`)
                    .then(resp => {
                        this.activity = resp.data;
                        this.useCompetencies = this.activity.competence.length > 0;
                        const evalKey = this.useCompetencies ? "competence_evaluation" : "evaluation";
                        if (this.useCompetencies) {
                            this.generalEval = this.activity.competence_id.reduce((a,b) => (a[b] = 0, a),{});
                        }
                        this.evaluation = students.map(student => {
                            if (hasPreviousEval) {
                                return resps[1].data.results.find(ev => ev.student === student.matricule)[evalKey];
                            }
                            return Object.assign({}, this.generalEval);
                        });

                        if (hasPreviousEval) {
                            this.activityEvaluation = students.map(student => {
                                return resps[1].data.results.find(ev => ev.student === student.matricule);
                            });
                            if (!isGroup) this.generalEval = this.evaluation[0];
                        }
                        if (isGroup) {
                            this.group = resps[2].data;
                        } else {
                            this.student = resps[2].data;
                        }
                        this.loading = false;
                    });
            })
            .catch(err => {
                console.log(err);
            });
    },
    methods: {
        updateIndividual: function (value, compet=null) {
            this.individualEval.forEach((toNotUpdate, index) => {
                if (toNotUpdate) return;

                if (this.useCompetencies) {
                    this.evaluation[index][compet] = value;
                } else {
                    this.evaluation[index] = value;
                }
            });
        },
        sendData: function () {
            let evalPromises = [];
            if (this.activityEvaluation.length) {
                evalPromises = this.activityEvaluation.map((aEv, index) => {
                    let data = {
                        activity_log: this.activityLogId,
                        student: this.group ?
                            this.group.students_id.filter(s => !this.activityLog.missing_student.includes(s))[index]
                            : this.student.matricule,
                    };
                    if (this.useCompetencies) {
                        data.competence_evaluation = this.evaluation[index];
                    } else {
                        data.evaluation = this.evaluation[index];
                    }
                    return axios.put(`/grandset/api/activity_evaluation/${aEv.id}/`, data, token);
                });
            } else {
                evalPromises = this.evaluation.map((ev, index) => {
                    let data = {
                        activity_log: this.activityLogId,
                        student: this.group ?
                            this.group.students_id.filter(s => !this.activityLog.missing_student.includes(s))[index]
                            : this.student.matricule,
                    };
                    if (this.useCompetencies) {
                        data.competence_evaluation = ev;
                    } else {
                        data.evaluation = ev;
                    }
                    return axios.post("/grandset/api/activity_evaluation/", data, token);
                });
            }

            Promise.all(evalPromises)
                .then(() => {
                    this.$router.push(`/activitymanagement/${this.activityLog.grand_set}/${this.activityLog.activity}/`, () => {
                        this.$root.$bvToast.toast(
                            "Les données ont bien été enregistrées.",
                            {
                                variant: "success",
                                noCloseButton: true,
                            }
                        );
                    });
                });
        }
    }
};
</script>
