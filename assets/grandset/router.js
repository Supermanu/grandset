// This file is part of Happyschool.
//
// Happyschool is the legal property of its developers, whose names
// can be found in the AUTHORS file distributed with this source
// distribution.
//
// Happyschool is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Happyschool is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with Happyschool.  If not, see <http://www.gnu.org/licenses/>.

import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

import GrandSetCreation from "./grandsetcreation.vue";
import GrandSet from "./grandset.vue";
import ActivityChange from "./activitychange.vue";
import ActivityManagement from "./activitymanagement.vue";
import Evaluation from "./evaluation.vue";

export default new VueRouter({
    routes: [
        {
            path: "",
            redirect: () => {
                // eslint-disable-next-line no-undef
                if (last_grandset) {
                    // eslint-disable-next-line no-undef
                    return `/grand_set/${last_grandset.id}/`;
                } else {
                    return "/grand_set_series/";
                }
            }
        },
        // {
        //     path: "/grand_set_series/",
        //     component: GrandSetSeries,
        //     props: true
        // },
        {
            path: "/grand_set_series_creation/:objectId/",
            component: GrandSetCreation,
            props: true
        },
        {
            path: "/grand_set_creation/:grandSetSeriesId/:objectId/",
            component: GrandSetCreation,
            props: (route) => {
                const props = {...route.params };
                props.series = false;
                return props;
            }
        },
        {
            path: "/grand_set/:grandSetId/",
            component: GrandSet,
            props: true
        },
        {
            path: "/activitychange/:grandSetId/:groupId/:activityLogId/",
            component: ActivityChange,
            props: true
        },
        {
            path: "/activitymanagement/:grandSetId/:activityId/",
            component: ActivityManagement,
            props: true
        },
        {
            path: "/evaluation/:activityLogId/:groupId/",
            component: Evaluation,
            props: true
        },
    ]
});
