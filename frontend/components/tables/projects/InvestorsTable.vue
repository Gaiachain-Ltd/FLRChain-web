<template>
  <v-data-table
    :headers="headers"
    :items="investors"
    hide-default-footer
    no-data-text="No investors"
    :items-per-page="-1"
  >
    <template v-slot:item.amount="{ item }">
      {{ amount(item) }}
    </template>
    <template v-slot:item.round-time="{ item }">
      {{ datetime(item) }}
    </template>
    <template v-slot:item.details="{ item }">
      <v-layout @click.prevent="() => openExplorerTransactionLink(item.id)">
        <a href="">See more</a>
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
      investors: [],
      headers: [
        {
          text: "Investor",
          value: "name",
        },
        {
          text: "Amount",
          value: "amount",
        },
        {
          text: "Date",
          value: "round-time",
        },
        {
          text: "Details",
          value: "details",
          sortable: false
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
    this.investors = await this.$axios
      .get(`projects/${this.project.id}/investors/`)
      .then((reply) => reply.data);
  },
};
</script>   