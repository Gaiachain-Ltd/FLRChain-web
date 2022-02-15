<template>
  <DefaultCard :title="title">
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
          <DefaultText>{{ facililatorFeeLabel }}</DefaultText>
        </v-flex>
        <v-spacer></v-spacer>
        <v-flex shrink>
          <DefaultText>{{ facililatorFee }}</DefaultText>
        </v-flex>
      </v-layout>
      <v-layout row ma-0 :class="!isFacililator ? 'mb-6' : ''">
        <v-flex>
          <DefaultText>{{ spentLabel }}</DefaultText>
        </v-flex>
        <v-spacer></v-spacer>
        <v-flex shrink>
          <DefaultText>{{ spent }}</DefaultText>
        </v-flex>
      </v-layout>
      <v-divider v-if="!isFacililator" class="mb-6"></v-divider>
      <v-layout row ma-0 shrink v-if="!isFacililator">
        <v-flex shrink>
          <DefaultText>Balance</DefaultText>
        </v-flex>
        <v-spacer></v-spacer>
        <v-flex shrink>
          <DefaultText>{{ balance }}</DefaultText>
        </v-flex>
      </v-layout>
    </v-layout>
  </DefaultCard>
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
    facililatorFeeLabel() {
      return this.isFacililator ? "Earned fee (10%)" : "Facililator fee (10%)";
    },
    facililatorFee() {
      return `${parseFloat(this.investment.facililator_fee)} USDC`;
    },
    spentLabel() {
      return this.isFacililator ? "Tasks rewards" : "Spent";
    },
    spent() {
      return `${parseFloat(this.investment.spent)} USDC`;
    },
    balance() {
      return `${parseFloat(this.investment.balance)} USDC`;
    }
  },
  components: {
    DefaultCard: () =>
      import("@/components/cards/DefaultCard"),
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
  async fetch() {
    this.investment = await this.$axios
      .get(`projects/${this.$route.params.id}/accounts/`)
      .then((reply) => reply.data);
  },
};
</script>