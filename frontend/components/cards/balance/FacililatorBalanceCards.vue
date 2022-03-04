<template>
  <DefaultCard>
    <v-layout column>
      <DefaultText
        bold
        :color="$vuetify.theme.themes.light.primary"
        class="mb-3"
        >Summary</DefaultText
      >
      <v-row shrink>
        <v-col>
          <BalanceCard
            :value="balance"
            label="Balance"
            text="Your current wallet balance"
          ></BalanceCard>
        </v-col>
        <v-col>
          <ProjectCounter></ProjectCounter>
        </v-col>
      </v-row>
    </v-layout>
  </DefaultCard>
</template>

<script>
export default {
  data() {
    return {
      balance: 0,
    };
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),

    DefaultCard: () => import("@/components/cards/DefaultCard"),
    BalanceCard: () => import("@/components/cards/balance/BalanceCard"),
    ProjectCounter: () => import("@/components/cards/balance/ProjectCounter"),
  },
  async fetch() {
    const balanceInfo = await this.$axios
      .get("accounts/")
      .then((reply) => reply.data);
    this.balance = balanceInfo.balance;
  },
};
</script>
