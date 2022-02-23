<template>
  <v-data-table :headers="headers" :items="activities" hide-default-footer>
    <template v-slot:item.amount="{ item }">
      {{ amount(item) }}
    </template>
    <template v-slot:item.datetime="{ item }">
      {{ datetime(item) }}
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
  },
  async fetch() {
    this.activities = await this.$axios
      .get(`projects/${this.project.id}/activities/`)
      .then((reply) => reply.data.filter(activity => activity.status == 1));
  },
};
</script>   