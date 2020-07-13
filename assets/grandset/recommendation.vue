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
            <b-overlay
                :show="loading"
                rounded="sm"
            >
                <b-row>
                    <b-col>
                        <h2>Recommandation</h2>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        <b-form-group>
                            <multiselect
                                :internal-search="false"
                                :options="studentOptions"
                                @search-change="getStudent"
                                placeholder="Rechercher un élève à recommander"
                                select-label=""
                                selected-label="Sélectionné"
                                deselect-label="Cliquer dessus pour enlever"
                                v-model="student"
                                multiple
                                label="display"
                                track-by="matricule"
                                :show-no-options="false"
                            >
                                <span slot="noResult">Aucun élève trouvé.</span>
                                <span slot="noOptions" />
                            </multiselect>
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col v-if="grandSet">
                        <b-card
                            v-for="(act, actIndex) in grandSet.activities"
                            :key="act.id"
                            class="mb-1"
                        >
                            <b-btn
                                :pressed.sync="recActivities[actIndex]"
                                variant="outline-warning"
                            >
                                <b-icon
                                    icon="star"
                                    variant="outline-warning"
                                />
                            </b-btn>
                            {{ act.activity_name }}
                            <b-collapse
                                v-model="recActivities[actIndex]"
                                class="mt-2"
                            >
                                <b-form-group
                                    label="Compétences"
                                    v-if="act.competence.length > 0"
                                    label-cols-sm="4"
                                    label-class="font-weight-bold"
                                >
                                    <div class="pt-2">
                                        <b-form-group
                                            v-for="comp in act.competence"
                                            :key="comp.id"
                                        >
                                            <b-form-checkbox>
                                                {{ comp.name }}
                                            </b-form-checkbox>
                                        </b-form-group>
                                    </div>
                                </b-form-group>
                                <b-form-group
                                    label="Commentaire"
                                >
                                    <b-input type="text" />
                                </b-form-group>
                            </b-collapse>
                        </b-card>
                    </b-col>
                </b-row>
                <b-row class="mt-1">
                    <b-col>
                        <b-btn variant="primary">
                            Recommander
                        </b-btn>
                    </b-col>
                </b-row>
            </b-overlay>
        </b-container>
    </div>
</template>

<script>
import axios from "axios";

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.min.css";

import {getPeopleByName} from "assets/common/search.js";

export default {
    props: {
        grandSetSeriesId: {
            default: "-1",
            type: String
        }
    },
    data: function () {
        return {
            student: [],
            studentOptions: [],
            grandSet: null,
            loading: true,
            recActivities: [],
            test: false,
            searchId: -1,
        };
    },
    methods: {
        getStudent: function (searchQuery) {
            this.searchId += 1;
            let currentSearch = this.searchId;

            const teachings = this.$store.state.settings.teachings.filter(
                // eslint-disable-next-line no-undef
                value => user_properties.teaching.includes(value));
            getPeopleByName(searchQuery, teachings, "student")
                .then( (resp) => {
                // Avoid that a previous search overwrites a faster following search results.
                    if (this.searchId !== currentSearch)
                        return;
                    this.studentOptions = resp.data;
                // this.searching = false;
                })
                .catch( (err) => {
                    alert(err);
                // this.searching = false;
                });
        },
    },
    mounted: function () {
        if (this.grandSetSeriesId === "-1") return;

        axios.get(`/grandset/api/grandset_series/${this.grandSetSeriesId}`)
            .then(resp => {
                this.grandSet = resp.data;
                this.recActivities = resp.data.activities.map(() => false);
                this.loading = false;
            });
    },
    components: {
        Multiselect
    }
};
</script>
