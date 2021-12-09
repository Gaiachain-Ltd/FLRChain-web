<template>
  <v-layout row shrink ma-0 class="justify-space-around">
    <v-layout xs12 sm5 md3 lg2 xl1 ma-3 shrink>
      <BalanceCard :value="total" label="All USDC"></BalanceCard>
    </v-layout>
    <v-layout xs12 sm5 md3 lg2 xl1 ma-3 shrink>
      <BalanceCard :value="spent" label="Invested USDC"></BalanceCard>
    </v-layout>
    <v-layout xs12 sm5 md3 lg2 xl1 ma-3 shrink>
      <BalanceCard :value="balance" label="Balance USDC"></BalanceCard>
    </v-layout>
    <v-layout xs12 sm12 md12 lg2 xl1 ma-3 shrink>
      <ButtonCard
        :value="balance"
        @clicked="paymentPopupVisible = true"
        :disabled="!$auth.user.opted_in"
      ></ButtonCard>
    </v-layout>
    <PaymentTypePopup
      :value.sync="paymentPopupVisible"
      v-if="paymentPopupVisible"
      @success="onSuccess"
      @error="onError"
    >
    </PaymentTypePopup>
    <SuccessPopup
      v-if="successPopupVisible"
      :value.sync="successPopupVisible"
      :text="successPopupText"
    >
    </SuccessPopup>
    <ErrorPopup
      :value.sync="errorPopupVisible"
      v-if="errorPopupVisible"
      :text="errorPopupText"
    >
    </ErrorPopup>
    <InfoPopup
      v-if="infoPopupVisible"
      :value.sync="infoPopupVisible"
      text="Your account is not active yet."
    ></InfoPopup>
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
      infoPopupVisible: false,
      successPopupText: "",
      errorPopupText: "",
    };
  },
  components: {
    BalanceCard: () => import("@/components/cards/balance/BalanceCard"),
    ButtonCard: () => import("@/components/cards/balance/ButtonCard"),
    PaymentTypePopup: () =>
      import("@/components/popups/payments/PaymentTypePopup"),
    SuccessPopup: () => import("@/components/popups/SuccessPopup"),
    ErrorPopup: () => import("@/components/popups/ErrorPopup"),
    InfoPopup: () => import("@/components/popups/InfoPopup"),
  },
  methods: {
    onSuccess(msg) {
      if (msg) {
        this.successPopupText = msg;
      } else {
        this.successPopupText = "Your payment is processing.";
      }
      this.paymentPopupVisible = false;
      this.successPopupVisible = true;
    },
    onError(msg) {
      if (msg) {
        this.errorPopupText = msg;
      } else {
        this.errorPopupText =
          "Unable to process your payment. Please try again later.";
      }
      this.errorPopupVisible = true;
    },
  },
  async fetch() {
    const balanceInfo = await this.$axios
      .get("accounts/")
      .then((reply) => reply.data);
    this.total = balanceInfo.total;
    this.spent = balanceInfo.spent;
    this.balance = balanceInfo.balance;

    if (!this.$auth.user.opted_in) {
      this.$auth.fetchUser().then(() => {
        if (!this.$auth.user.opted_in) {
          this.infoPopupVisible = true;
        }
      });
    }
  },
};
</script>
