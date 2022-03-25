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
            :value="allocated"
            label="Allocated"
            text="Total amount of your investitions"
          ></BalanceCard>
        </v-col>
        <v-col>
          <BalanceCard
            :value="distributed"
            label="Distributed"
            text="Total amount of distributed USDC to stewards from your projects"
          ></BalanceCard>
        </v-col>
        <v-col>
          <BalanceCard
            :value="balance"
            label="Balance"
            text="Your current wallet balance"
          ></BalanceCard>
        </v-col>
      </v-row>
    </v-layout>
  </DefaultCard>
</template>

<script>
export default {
  data() {
    return {
      allocated: 0,
      spent: 0,
      balance: 0,
    };
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultCard: () => import("@/components/cards/DefaultCard"),
    BalanceCard: () => import("@/components/cards/balance/BalanceCard"),
    ButtonCard: () => import("@/components/cards/balance/ButtonCard"),
  },
  async fetch() {
    const balanceInfo = await this.$axios
      .get("accounts/details/")
      .then((reply) => reply.data);
    this.allocated = balanceInfo.allocated;
    this.distributed = balanceInfo.distributed ? balanceInfo.distributed : 0;
    this.balance = balanceInfo.balance;
  },
};
</script>
