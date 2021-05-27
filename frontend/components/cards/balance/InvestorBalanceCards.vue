<template>
  <v-layout row shrink ma-0>
    <v-flex xs2 shrink>
      <BalanceCard :value="total" label="All USDC"></BalanceCard>
    </v-flex>
    <v-spacer></v-spacer>
    <v-flex xs2 shrink>
      <BalanceCard :value="spent" label="Invested USDC"></BalanceCard>
    </v-flex>
    <v-spacer></v-spacer>
    <v-flex xs2 shrink>
      <BalanceCard :value="balance" label="Balance USDC"></BalanceCard>
    </v-flex>
    <v-spacer></v-spacer>
    <v-flex xs2 shrink>
      <ButtonCard
        :value="balance"
        @clicked="paymentPopupVisible = true"
      ></ButtonCard>
    </v-flex>
    <PaymentPopup
      :value.sync="paymentPopupVisible"
      v-if="paymentPopupVisible"
      @success="successPopupVisible = true"
      @error="errorPopupVisible = true"
    ></PaymentPopup>
    <SuccessPopup
    :value.sync="successPopupVisible"
    v-if="successPopupVisible"
    text="Payment success.">
    </SuccessPopup>
    <ErrorPopup
    :value.sync="errorPopupVisible"
    v-if="errorPopupVisible"
    text="Payment failed.">
    </ErrorPopup>
  </v-layout>
</template>

<script>
export default {
  data() {
    return {
      total: 0,
      spent: 0,
      balance: 0,
      paymentPopupVisible: false,
      successPopupVisible: false,
      errorPopupVisible: false,
    };
  },
  components: {
    BalanceCard: () => import("@/components/cards/balance/BalanceCard"),
    ButtonCard: () => import("@/components/cards/balance/ButtonCard"),
    PaymentPopup: () => import("@/components/popups/PaymentPopup"),
    SuccessPopup: () => import("@/components/popups/SuccessPopup"),
    ErrorPopup: () => import("@/components/popups/ErrorPopup")
  },
  async fetch() {
    const balanceInfo = await this.$axios
      .get("accounts/")
      .then((reply) => reply.data);
    this.total = balanceInfo.total;
    this.spent = balanceInfo.spent;
    this.balance = balanceInfo.balance;
  },
};
</script>