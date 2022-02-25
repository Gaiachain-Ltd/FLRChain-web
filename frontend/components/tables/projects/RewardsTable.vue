<template>
  <v-data-table :headers="headers" :items="activities" hide-default-footer>
    <template v-slot:item.amount="{ item }">
      {{ amount(item) }}
    </template>
    <template v-slot:item.datetime="{ item }">
      {{ datetime(item) }}
    </template>
    <template v-slot:item.status="{ item }">
      <v-layout align-center v-if="item.status == 0">
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
      <div v-else :style="{ color: statusColor(item.status) }">
        {{ status(item.status) }}
      </div>
    </template>
    <template v-slot:item.details="{ item }">
      <v-layout @click.prevent="() => openExplorerTransactionLink(item.txid)">
        <a>See more</a>
      </v-layout>
    </template>
  </v-data-table>
</template>

<script>
import algosdk from "algosdk";
import AlgoExplorerMixin from "@/mixins/AlgoExplorerMixin";

export default {
  mixins: [AlgoExplorerMixin],
  props: {
    project: {},
  },
  data() {
    return {
      activities: [],
      options: {
        sortBy: ["status"],
      },
      headers: [
        {
          text: "Steward",
          value: "name",
        },
        {
          text: "Task ID",
          value: "task_id",
        },
        {
          text: "Amount",
          value: "amount",
        },
        {
          text: "Date",
          value: "datetime",
        },
        {
          text: "Request",
          value: "status",
        },
        {
          text: "Details",
          value: "details",
        },
      ],
    };
  },
  methods: {
    amount(item) {
      return `${algosdk.microalgosToAlgos(item.amount)} USDC`;
    },
    datetime(item) {
      return this.$moment.unix(item["round-time"]).format("YYYY-MM-DD HH:mm");
    },
    handleApproval(activity, value) {
      this.$axios
        .put(`projects/${this.project.id}/activities/${activity.id}/`, {
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
    this.activities = await this.$axios
      .get(`projects/${this.project.id}/activities/`)
      .then((reply) => reply.data);
  },
};
</script>   