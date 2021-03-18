<template>
  <DefaultCardWithTitle title="Your investment history:">
    <v-layout column ma-0>
      <v-layout row mb-6 ma-0>
        <v-flex>
          <DefaultText>Invested</DefaultText>
        </v-flex>
        <v-spacer></v-spacer>
        <v-flex shrink>
          <DefaultText>{{ investment.amount }}</DefaultText>
        </v-flex>
      </v-layout>
      <v-layout row mb-6 ma-0>
        <v-flex>
          <DefaultText>Facililator fee (10%)</DefaultText>
        </v-flex>
        <v-spacer></v-spacer>
        <v-flex shrink>
          <DefaultText>0</DefaultText>
        </v-flex>
      </v-layout>
      <v-layout row mb-6 ma-0>
        <v-flex>
          <DefaultText>Spent</DefaultText>
        </v-flex>
        <v-spacer></v-spacer>
        <v-flex shrink>
          <DefaultText>0</DefaultText>
        </v-flex>
      </v-layout>
      <v-divider class="mb-6"></v-divider>
      <v-layout row mb-6 ma-0>
        <v-flex>
          <DefaultText>Balance</DefaultText>
        </v-flex>
        <v-spacer></v-spacer>
        <v-flex shrink>
          <DefaultText>0</DefaultText>
        </v-flex>
      </v-layout>
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
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
  async fetch() {
    this.investment = await this.$axios
      .get(`projects/${this.$route.params.id}/investments/`)
      .then((reply) => reply.data);
  },
};
</script>