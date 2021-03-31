<template>
  <v-layout column ma-0>
    <v-layout row ma-0>
      <DefaultText :color="color" :size="14">{{ investor }}</DefaultText>
      <v-spacer></v-spacer>
      <DefaultText :color="color" :size="14">{{ amount }}</DefaultText>
    </v-layout>
    <v-flex class="mt-3">
      <DefaultText :color="color" :size="14">{{ investmentDate }}</DefaultText>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  props: {
    investment: {},
  },
  computed: {
    investor() {
      return `${this.investment.investor.first_name} ${this.investment.investor.last_name}`;
    },
    investmentDate() {
      const start = this.$moment(this.investment.start).format("YYYY-MM-DD");
      const end = this.$moment(this.investment.end).format("YYYY-MM-DD");
      return `${start} - ${end}`;
    },
    amount() {
      return `${parseFloat(this.investment.amount)} USDC`;
    },
    color() {
      return this.$vuetify.theme.themes.light.nonary;
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>