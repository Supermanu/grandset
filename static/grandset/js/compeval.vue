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
    <BFormGroup
        :label="compName"
        label-cols-md="4"
        label-align-md="right"
    >
        <BInputGroup>
            <BFormInput
                :value="value"
                type="range"
                min="0"
                max="2"
                @input="updateData"
            />
            <template #append>
                <div class="w-50">
                    <BInputGroupText
                        :class="colorCompletion"
                    >
                        {{ labelCompetence }}
                        <IBiCheck
                            v-if="value === '2'"
                            variant="success"
                        />
                    </BInputGroupText>
                </div>
            </template>
        </BInputGroup>
    </BFormGroup>
</template>

<script>

const compEvalLabel = ["Non maîtrisé", "Partiellement maîtrisé", "Maîtrisé"];

export default {
    props: {
        /** Competence name. */
        compName: {
            type: String,
            default: "",
        },
        value: {
            type: Number,
            default: 0,
        },
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
        },
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
