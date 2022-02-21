<template>
  <v-data-table :headers="headers" :items="beneficiaries" hide-default-footer>
    <template v-slot:item.datetime="{ item }">
      {{ datetime(item) }}
    </template>
    <template v-slot:item.details="{ item }">
      <v-layout @click.prevent="() => openExplorerTransactionLink(item.optin_txid)">
        <a>See more</a>
      </v-layout>
    </template>
  </v-data-table>
</template>

<script>
import AlgoExplorerMixin from "@/mixins/AlgoExplorerMixin";

export default {
  mixins: [AlgoExplorerMixin],
  props: {
    project: {},
  },
  data() {
    return {
      beneficiaries: [],
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
        },
        {
          text: "Details",
          value: "details"
        },
      ],
    };
  },
  methods: {
    datetime(item) {
      return this.$moment.unix(item["round-time"]).format("YYYY-MM-DD HH:mm");
    },
  },
  async fetch() {
    this.beneficiaries = await this.$axios
      .get(`projects/${this.project.id}/assignments/`)
      .then((reply) => reply.data.filter(ben => ben.approval == 0));
  },
};
</script>   