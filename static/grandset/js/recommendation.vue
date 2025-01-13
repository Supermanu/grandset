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
            <BOverlay
                :show="loading"
                rounded="sm"
            >
                <BRow>
                    <BCol>
                        <h2>Recommandation</h2>
                    </BCol>
                </BRow>
                <BRow>
                    <BCol>
                        <BFormGroup>
                            <multiselect
                                v-model="student"
                                :internal-search="false"
                                :options="studentOptions"
                                placeholder="Rechercher un élève à recommander"
                                select-label=""
                                selected-label="Sélectionné"
                                deselect-label="Cliquer dessus pour enlever"
                                multiple
                                label="display"
                                track-by="matricule"
                                :show-no-options="false"
                                @search-change="getStudent"
                            >
                                <template #noResult>
                                    Aucun élève trouvé.
                                </template>
                                <template #noOptions />
                            </multiselect>
                        </BFormGroup>
                    </BCol>
                </BRow>
                <BRow>
                    <BCol v-if="grandSet">
                        <BCard
                            v-for="(act, actIndex) in grandSet.activities"
                            :key="act.id"
                            class="mb-1"
                        >
                            <BButton
                                v-model:pressed="recActivities[actIndex]"
                                variant="outline-warning"
                            >
                                <IBiStar variant="outline-warning" />
                            </BButton>
                            {{ act.activity_name }}
                            <BCollapse
                                v-model="recActivities[actIndex]"
                                class="mt-2"
                            >
                                <BFormGroup
                                    v-if="act.competence.length > 0"
                                    label="Compétences"
                                    label-cols-sm="4"
                                    label-class="font-weight-bold"
                                >
                                    <div class="pt-2">
                                        <BFormGroup
                                            v-for="comp in act.competence"
                                            :key="comp.id"
                                        >
                                            <BFormCheckbox>
                                                {{ comp.name }}
                                            </BFormCheckbox>
                                        </BFormGroup>
                                    </div>
                                </BFormGroup>
                                <BFormGroup
                                    label="Commentaire"
                                >
                                    <BFormInput type="text" />
                                </BFormGroup>
                            </BCollapse>
                        </BCard>
                    </BCol>
                </BRow>
                <BRow class="mt-1">
                    <BCol>
                        <BButton variant="primary">
                            Recommander
                        </BButton>
                    </BCol>
                </BRow>
            </BOverlay>
        </BContainer>
    </div>
</template>

<script>
import axios from "axios";

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

import { grandsetStore } from "./stores/index.js";

import {getPeopleByName} from "@s:core/js/common/search.js";

export default {
    components: {
        Multiselect
    },
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
            store: grandsetStore(),
        };
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
    methods: {
        getStudent: function (searchQuery) {
            this.searchId += 1;
            let currentSearch = this.searchId;

            const teachings = this.store.settings.teachings.filter(
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
    }
};
</script>
