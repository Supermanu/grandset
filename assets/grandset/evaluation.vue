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
                            label="Évaluation du groupe"
                            label-cols-sm="4"
                            label-align-sm="center"
                            label-class="font-weight-bold"
                            description="Évaluer l'ensemble du groupe.
                                Si nécessaire, vous pouvez évaluer individuellement ci-dessous."
                        >
                            <div v-if="useCompetencies">
                                <b-form-group
                                    v-for="comp in activity.competence"
                                    :key="comp.id"
                                    :label="comp.name"
                                    label-cols-md="4"
                                    label-align-md="right"
                                >
                                    <b-input-group>
                                        <b-form-input
                                            v-model="groupEval[comp.id]"
                                            type="range"
                                            min="0"
                                            max="2"
                                            @input="updateIndividual(groupEval[comp.id], comp.id)"
                                        />
                                        <b-input-group-append
                                            class="w-50"
                                        >
                                            <b-input-group-text
                                                :class="colorCompletion(groupEval[comp.id])"
                                            >
                                                {{ labelCompetence(groupEval[comp.id]) }}
                                                <b-icon
                                                    v-if="groupEval[comp.id] === '2'"
                                                    icon="check"
                                                    variant="success"
                                                />
                                            </b-input-group-text>
                                        </b-input-group-append>
                                    </b-input-group>
                                </b-form-group>
                            </div>
                            <div v-else>
                                <b-input-group
                                    :append="'/ ' + $store.state.settings.max_points"
                                >
                                    <b-form-input
                                        v-model="groupEval"
                                        type="number"
                                        step="0.01"
                                        min="0"
                                        :max="$store.state.settings.max_points"
                                        @input="updateIndividual"
                                    />
                                </b-input-group>
                            </div>
                        </b-form-group>
                        <b-card bg-variant="light">
                            <b-form-group
                                label-cols-lg="3"
                                :label="group.group_name"
                                label-size="lg"
                                label-class="font-weight-bold pt-0"
                                class="mb-0"
                            >
                                <b-form-group 
                                    v-for="(student, index) in group.students"
                                    :key="student.matricule"
                                    label-cols-sm="3"
                                    label-align-sm="right"
                                >
                                    <slot name="label">
                                        <b-form-checkbox
                                            switch
                                            class="mr-n2"
                                            v-model="individualEval[index]"
                                        >
                                            {{ group.students_display[index] }}
                                        </b-form-checkbox>
                                    </slot>
                                    <div v-if="useCompetencies">
                                        <b-form-group
                                            v-for="comp in activity.competence"
                                            :key="comp.id"
                                            :label="comp.name"
                                            label-cols-md="4"
                                            label-align-md="right"
                                        >
                                            <b-input-group>
                                                <b-form-input
                                                    v-model="evaluation[index][comp.id]"
                                                    type="range"
                                                    min="0"
                                                    max="2"
                                                    :disabled="!individualEval[index]"
                                                />
                                                <b-input-group-append
                                                    class="w-50"
                                                >
                                                    <b-input-group-text
                                                        :class="colorCompletion(evaluation[index][comp.id])"
                                                    >
                                                        {{ labelCompetence(evaluation[index][comp.id]) }}
                                                        <b-icon
                                                            v-if="evaluation[index][comp.id] === '2'"
                                                            icon="check"
                                                            variant="success"
                                                        />
                                                    </b-input-group-text>
                                                </b-input-group-append>
                                            </b-input-group>
                                        </b-form-group>
                                    </div>
                                    <div v-else>
                                        <b-input-group
                                            :append="'/ ' + $store.state.settings.max_points"
                                        >
                                            <b-form-input
                                                type="number"
                                                step="0.01"
                                                min="0"
                                                :max="$store.state.settings.max_points"
                                                v-model="evaluation[index]"
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

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};
const compEvalLabel = ["Non maîtrisé", "Partiellement maîtrisé", "Maîtrisé"];
export default {
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
            activityEvaluation: [],
            loading: true,
            individualEval: [],
            evaluation: [],
            groupEval: null,
        };
    },
    methods: {
        colorCompletion: function (compVal) {
            switch (compVal) {
            case "1":
                return "half-completed";
            case "2":
                return "completed";

            default:
                return "";
            }
        },
        labelCompetence: function (compVal) {
            return compEvalLabel[compVal];
        },
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
                        student: this.group.students_id[index],
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
                        student: this.group.students_id[index],
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
    },
    mounted: function () {
        if (this.activityLogId === "-1") return;

        const activityLogProm = axios.get(`/grandset/api/activity_log/${this.activityLogId}/`);
        const groupProm = axios.get(`/grandset/api/group/${this.groupId}/`);
        const previousEval = axios.get(`/grandset/api/activity_evaluation/?activity_log=${this.activityLogId}`);
        Promise.all([activityLogProm, groupProm, previousEval])
            .then(resps => {
                this.activityLog = resps[0].data;
                this.group = resps[1].data;
                const hasPreviousEval = resps[2].data.count > 0;
                this.individualEval = this.group.students.map(() => hasPreviousEval);

                axios.get(`/grandset/api/activity/${this.activityLog.activity}/`)
                    .then(resp => {
                        this.activity = resp.data;
                        this.useCompetencies = this.activity.competence.length > 0;
                        const evalKey = this.useCompetencies ? "competence_evaluation" : "evaluation";
                        if (this.useCompetencies) {
                            this.groupEval = this.activity.competence_id.reduce((a,b) => (a[b] = "0", a),{});
                        }
                        this.evaluation = this.group.students.map(student => {
                            if (hasPreviousEval) {
                                return resps[2].data.results.find(ev => ev.student === student.matricule)[evalKey];
                            }
                            return this.groupEval;
                        });
                        if (hasPreviousEval) {
                            this.activityEvaluation = this.group.students.map(student => {
                                return resps[2].data.results.find(ev => ev.student === student.matricule);
                            });
                        }
                        this.loading = false;
                    });
            })
            .catch(err => {
                console.log(err);
            });
    },
};
</script>

<style>
.half-completed {
    background-color: lightyellow;
}

.completed {
    background-color: lightgreen;
}
</style>
