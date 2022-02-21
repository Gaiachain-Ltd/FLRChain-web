<template>
  <v-data-table :headers="headers" :items="beneficiaries" hide-default-footer>
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
      <v-layout
        @click.prevent="() => openExplorerTransactionLink(item.optin_txid)"
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
    datetime(item) {
      return this.$moment.unix(item["round-time"]).format("YYYY-MM-DD HH:mm");
    },
    handleApproval(beneficiary, value) {
      this.$axios
        .put(`projects/assignments/${beneficiary.id}/`, {
          status: value,
        })
        .then(() => {
          const index = _.findIndex(this.beneficiaries, ["id", beneficiary.id]);
          console.log("INDEX", index);
          if (index !== -1) {
            this.beneficiaries.splice(index, 1);
          }
        });
    },
  },
  components: {
    ActionButton: () => import("@/components/buttons/ActionButton"),
  },
  async fetch() {
    this.beneficiaries = await this.$axios
      .get(`projects/${this.project.id}/assignments/`)
      .then((reply) => reply.data.filter((ben) => ben.approval == 0));
  },
};
</script>   