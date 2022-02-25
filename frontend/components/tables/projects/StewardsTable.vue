<template>
  <v-data-table :headers="headers" :items="beneficiaries" :options.sync="options" hide-default-footer>
    <template v-slot:item.datetime="{ item }">
      {{ datetime(item) }}
    </template>
    <template v-slot:item.approval="{ item }">
      <v-layout align-center v-if="item.approval == 0">
        <ActionButton
          class="mr-1"
          :border="`1px ${$vuetify.theme.themes.light.success} solid !important`"
          color="white"
          :textColor="$vuetify.theme.themes.light.success"
          @click.prevent="() => handleApproval(item, 1)"
          >Approve</ActionButton
        >
        <ActionButton
          class="ml-1"
          :border="`1px ${$vuetify.theme.themes.light.error} solid !important`"
          color="white"
          :textColor="$vuetify.theme.themes.light.error"
          @click.prevent="() => handleApproval(item, 2)"
          >Reject</ActionButton
        >
      </v-layout>
      <div v-else :style="{ color: statusColor(item.approval) }">
        {{ status(item.approval) }}
      </div>
    </template>
    <template v-slot:item.details="{ item }">
      <v-layout
        @click.prevent="
          () => {
            if (item.approval) {
              openExplorerTransactionLink(item.approval_txid);
            } else {
              openExplorerTransactionLink(item.optin_txid);
            }
          }
        "
      >
        <a>See more</a>
      </v-layout>
    </template>
  </v-data-table>
</template>

<script>
import AlgoExplorerMixin from "@/mixins/AlgoExplorerMixin";
import _ from "lodash";

export default {
  mixins: [AlgoExplorerMixin],
  props: {
    project: {},
  },
  data() {
    return {
      beneficiaries: [],
      options: {
        "sortBy": ['approval']
      },
      headers: [
        {
          text: "Steward",
          value: "name",
        },
        {
          text: "Date",
          value: "datetime",
        },
        {
          text: "Location",
          value: "village",
        },
        {
          text: "Request",
          value: "approval",
        },
        {
          text: "Details",
          value: "details",
        },
      ],
    };
  },
  methods: {
    datetime(item) {
      return this.$moment.unix(item["round-time"]).format("YYYY-MM-DD HH:mm");
    },
    handleApproval(beneficiary, value) {
      this.$axios
        .put(`projects/assignments/${beneficiary.id}/`, {
          status: value,
        })
        .then(() => this.$fetch());
    },
    status(value) {
      switch (value) {
        case 0:
          return "Pending";
        case 1:
          return "Accepted";
        case 2:
          return "Rejected";
        default:
          return value;
      }
    },
    statusColor(value) {
      switch (value) {
        case 1:
          return this.$vuetify.theme.themes.light.success;
        case 2:
          return this.$vuetify.theme.themes.light.error;
        default:
          return undefined;
      }
    },
  },
  components: {
    ActionButton: () => import("@/components/buttons/ActionButton"),
  },
  async fetch() {
    this.beneficiaries = await this.$axios
      .get(`projects/${this.project.id}/assignments/`)
      .then((reply) => reply.data);
  },
};
</script>   