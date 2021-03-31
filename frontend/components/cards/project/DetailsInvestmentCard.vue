<template>
  <DefaultCardWithTitle :title="title">
    <v-layout column ma-0>
      <v-layout row mb-6 ma-0>
        <v-flex>
          <DefaultText>Invested</DefaultText>
        </v-flex>
        <v-spacer></v-spacer>
        <v-flex shrink>
          <DefaultText>{{ total }}</DefaultText>
        </v-flex>
      </v-layout>
      <v-layout row mb-6 ma-0>
        <v-flex>
          <DefaultText>Facililator fee (10%)</DefaultText>
        </v-flex>
        <v-spacer></v-spacer>
        <v-flex shrink>
          <DefaultText>{{ facililatorFee }}</DefaultText>
        </v-flex>
      </v-layout>
      <v-layout row mb-6 ma-0>
        <v-flex>
          <DefaultText>Spent</DefaultText>
        </v-flex>
        <v-spacer></v-spacer>
        <v-flex shrink>
          <DefaultText>{{ spent }}</DefaultText>
        </v-flex>
      </v-layout>
      <v-divider class="mb-6"></v-divider>
      <v-layout row ma-0 shrink>
        <v-flex shrink>
          <DefaultText>Balance</DefaultText>
        </v-flex>
        <v-spacer></v-spacer>
        <v-flex shrink>
          <DefaultText>{{ balance }}</DefaultText>
        </v-flex>
      </v-layout>
    </v-layout>
  </DefaultCardWithTitle>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      investment: {},
    };
  },
  computed: {
    ...mapGetters(["isFacililator"]),
    title() {
      return this.isFacililator ? "Investment history:" : "Your investment history:";
    },
    total() {
      return `${parseFloat(this.investment.total)} USDC`;
    },
    facililatorFee() {
      return `${parseFloat(this.investment.facililator_fee)} USDC`;
    },
    spent() {
      return `${parseFloat(this.investment.spent)} USDC`;
    },
    balance() {
      return `${parseFloat(this.investment.balance)} USDC`;
    }
  },
  components: {
    DefaultCardWithTitle: () =>
      import("@/components/cards/DefaultCardWithTitle"),
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
  async fetch() {
    this.investment = await this.$axios
      .get(`projects/${this.$route.params.id}/accounts/`)
      .then((reply) => reply.data);
  },
};
</script>