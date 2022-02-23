<template>
  <v-data-table :headers="headers" :items="activities" hide-default-footer>
    <template v-slot:item.amount="{ item }">
      {{ amount(item) }}
    </template>
    <template v-slot:item.datetime="{ item }">
      {{ datetime(item) }}
    </template>
    <template v-slot:item.request="{ item }">
      <v-layout align-center>
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
          value: "request",
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
        .then(() => {
          const index = _.findIndex(this.activities, ["id", activity.id]);
          console.log("INDEX", index);
          if (index !== -1) {
            this.activities.splice(index, 1);
          }
        });
    },
  },
  components: {
    ActionButton: () => import("@/components/buttons/ActionButton"),
  },
  async fetch() {
    this.activities = await this.$axios
      .get(`projects/${this.project.id}/activities/`)
      .then((reply) => reply.data.filter(activity => activity.status == 0));
  },
};
</script>   