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
    <b-form-group
        :label="compName"
        label-cols-md="4"
        label-align-md="right"
    >
        <b-input-group>
            <b-form-input
                :value="value"
                type="range"
                min="0"
                max="2"
                @input="updateData"
            />
            <b-input-group-append
                class="w-50"
            >
                <b-input-group-text
                    :class="colorCompletion"
                >
                    {{ labelCompetence }}
                    <b-icon
                        v-if="value === '2'"
                        icon="check"
                        variant="success"
                    />
                </b-input-group-text>
            </b-input-group-append>
        </b-input-group>
    </b-form-group>
</template>

<script>

const compEvalLabel = ["Non maîtrisé", "Partiellement maîtrisé", "Maîtrisé"];

export default {
    props: {
        /** Competence name. */
        compName: {
            type: String,
            default: ""
        },
        value: {
            type: Number,
            default: 0
        }
    },
    data: function () {
        return {
        };
    },
    computed: {
        colorCompletion: function () {
            switch (this.value) {
            case 1:
                return "half-completed";
            case 2:
                return "completed";

            default:
                return "";
            }
        },
        labelCompetence: function () {
            return compEvalLabel[this.value];
        },
    },
    methods: {
        updateData: function (event) {
            this.$emit("input", parseInt(event));
        }
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
