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
                <h5>Groupes disponibles</h5>
                <b-input-group>
                    <b-form-input
                        placeholder="Rechercher un groupe"
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
                        v-for="(group, index) in filteredGroups"
                        :key="group.id"
                        @click="addGroup(index)"
                    >
                        {{ group.group_name }}:
                        <small>
                            {{ group.students_display.join(", ") }}
                        </small>
                    </b-list-group-item>
                </b-list-group>
            </b-col>
            <b-col>
                <h5>Groupes sélectionnés</h5>
                <b-list-group>
                    <b-list-group-item
                        button
                        v-for="(group, index) in value"
                        :key="group.id"
                        @click="removeGroup(index)"
                    >
                        {{ group.group_name }}:
                        <small>
                            {{ group.students_display.join(", ") }}
                        </small>
                    </b-list-group-item>
                </b-list-group>
            </b-col>
        </b-row>
    </div>
</template>

<script>
import axios from "axios";

export default {
    props: {
        /** The selected groups */
        value: {
            type: Array,
            default: () => []
        },
        series: {
            type: Boolean,
            default: true,
        },
    },
    data() {
        return {
            availGroup: [],
            search: ""
        };
    },
    computed: {
        filteredGroups: function () {
            if (this.search === "") return this.availGroup;

            return this.availGroup.filter(a => {
                const isInGroupName = a.group_name.toLowerCase().includes(this.search.toLowerCase());
                const isInStudentsName = a.students_display.join("").toLowerCase().includes(this.search.toLowerCase());
                return isInGroupName || isInStudentsName;
            });
        },
    },
    methods: {
        addGroup(index) {
            const group = this.availGroup.splice(index, 1);
            this.$emit("input", this.value.concat(group));
        },
        removeGroup(index) {
            this.availGroup.unshift(this.value[index]);
            this.$emit("input", this.value.filter((v, i) => i != index));
        }
    },
    mounted () {
        if (this.series) {
            // Load all groups available.
            axios.get("/grandset/api/group/")
                .then(resp => {
                    const selectedGroups = this.value.map(g => g.id);
                    this.availGroup = resp.data.results.filter(g => !selectedGroups.includes(g.id));
                });
        }
    },
};
</script>
