<template>
  <DefaultCardWithTitle title="Invest in project:">
    <v-layout column ma-0>
      <v-flex>
        <InvestmentForm :investment.sync="investment"></InvestmentForm>
      </v-flex>
      <v-flex>
        <BlockButton @clicked="invest">Invest</BlockButton>
      </v-flex>
    </v-layout>
  </DefaultCardWithTitle>
</template>

<script>
export default {
  data() {
    return {
      investment: {},
    };
  },
  components: {
    DefaultCardWithTitle: () =>
      import("@/components/cards/DefaultCardWithTitle"),
    InvestmentForm: () => import("@/components/forms/project/InvestmentForm"),
    BlockButton: () => import("@/components/buttons/BlockButton"),
  },
  methods: {
    invest() {
      this.$axios
        .post(`projects/${this.$route.params.id}/investments/`, this.investment)
        .then(this.$emit("refresh"));
    },
  },
};
</script>