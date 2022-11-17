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
                    <h3>Séries de {{ $store.state.settings.grand_set_name }}</h3>
                </b-col>
            </b-row>
            <b-row class="mb-2">
                <b-col>
                    <b-btn
                        to="/grand_set_series_creation/-1/"
                        variant="success"
                    >
                        <b-icon icon="plus" />
                        Ajouter
                    </b-btn>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <ul>
                        <b-card
                            no-body
                            v-for="s in series"
                            :key="s.id"
                        >
                            <b-card-body
                                class="d-flex justify-content-between"
                            >
                                <a :href="`#/grand_set_series_creation/${s.id}/`">
                                    {{ s.name }}
                                </a>
                                <span>
                                    <b-btn
                                        size="sm"
                                        :to="`/recommendation/${s.id}/`"
                                    >
                                        Recommander une activité
                                    </b-btn>
                                    <b-btn
                                        size="sm"
                                        :to="`/grand_set_series_creation/${s.id}/`"
                                    >
                                        Modifier
                                    </b-btn>
                                    <b-btn
                                        v-if="s.last_grand_set"
                                        size="sm"
                                        :to="`/grand_set/${s.last_grand_set}/`"
                                    >
                                        Voir
                                    </b-btn>
                                    <b-btn
                                        variant="danger"
                                        size="sm"
                                        class="ml-4"
                                        @click="removeSerie(s.id)"
                                    >
                                        <b-icon icon="trash" />
                                    </b-btn>
                                </span>
                            </b-card-body>
                        </b-card>
                    </ul>
                </b-col>
            </b-row>
        </b-container>
    </div>
</template>

<script>
import Moment from "moment";
import axios from "axios";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    data: function () {
        return {
            series: []
        };
    },
    methods: {
        removeSerie: function (serieId) {
            this.$bvModal.msgBoxConfirm("Êtes-vous sûr de vouloir supprimer cette série ?", {
                title: "Suppression de la série",
                okVariant: "danger",
                okTitle: "Oui",
                cancelTitle: "Non",
                footerClass: "p-2",
                hideHeaderClose: false,
                centered: true
            })
                .then(response => {
                    if (response) {
                        this.series.splice(this.series.findIndex(s => s.id === serieId), 1);
                        axios.delete(`/grandset/api/grandset_series/${serieId}/`, token);
                    }
                })
                .catch(err => {
                    // An error occurred
                    console.log(err);
                });
            return;
        }
    },
    mounted: function () {
        axios.get("/grandset/api/grandset_series/")
            .then(resp => {
                this.series = resp.data.results.map(s => {
                    s.last_grand_set = null;
                    return s;
                });
                const last_grand_set = this.series.map(s => axios.get(`/grandset/api/grandset/?grand_set_series=${s.id}&date__gte=${Moment().format("L")}`));
                Promise.all(last_grand_set)
                    .then(resps => {
                        resps.forEach((gS, idx) => {
                            this.series[idx].last_grand_set = gS.data.count > 0 ? gS.data.results[0].id : null;
                        });
                    });
            });
    },
};
</script>
