<template>
  <v-data-table :headers="headers" :items="investors" hide-default-footer>
  </v-data-table>
</template>

<script>
export default {
  props: {
    project: {},
  },
  data() {
    return {
      investors: [],
      headers: [
        {
          text: "Steward",
          value: "name",
        },
        {
          text: "Date",
          value: "amount",
        },
        {
          text: "Status",
          value: "details",
        },
      ],
    };
  },
  async fetch() {
    // this.investors = await this.$axios
    //   .get(`projects/${this.project.id}/investors/`)
    //   .then((reply) => reply.data);
  },
};
</script>   