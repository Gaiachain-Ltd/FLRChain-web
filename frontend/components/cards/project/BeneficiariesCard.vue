<template>
  <DefaultCardWithTitle title="Beneficiaries:">
    <v-layout
      column
      ma-0
      v-for="(assignment, index) in assignments"
      :key="assignment.id"
    >
      <v-divider v-if="index" class="my-3"></v-divider>
      <BeneficiaryDelegate
        :assignment="assignment"
        @refresh="onRefresh"
      ></BeneficiaryDelegate>
    </v-layout>
  </DefaultCardWithTitle>
</template>

<script>
export default {
  data() {
    return {
      assignments: [],
    };
  },
  components: {
    DefaultCardWithTitle: () =>
      import("@/components/cards/DefaultCardWithTitle"),
    BeneficiaryDelegate: () =>
      import("@/components/delegates/BeneficiaryDelegate"),
  },
  methods: {
    onRefresh() {
      this.$fetch();
    },
  },
  async fetch() {
    this.assignments = await this.$axios
      .get(`projects/${this.$route.params.id}/assignments/`)
      .then((reply) => reply.data.results);
  },
};
</script>