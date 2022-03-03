<template>
  <DefaultCard>
    <v-layout column shrink>
      <DefaultText
        class="my-3"
        bold
        :color="$vuetify.theme.themes.light.primary"
        >Top up</DefaultText
      >
      <ActionButton @click.prevent="paymentPopupVisible = true"
        >Add USDC</ActionButton
      >
    </v-layout>
    <PaymentTypePopup
      :value.sync="paymentPopupVisible"
      v-if="paymentPopupVisible"
      :address="address"
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
  </DefaultCard>
</template>

<script>
export default {
  data() {
    return {
      address: "",
      paymentPopupVisible: false,
      successPopupVisible: false,
      errorPopupVisible: false,
      infoPopupVisible: false,
      successPopupText: "",
      errorPopupText: "",
    };
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    ActionButton: () => import("@/components/buttons/ActionButton"),
    DefaultCard: () => import("@/components/cards/DefaultCard"),
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
    await this.$axios
      .get("accounts/details/")
      .then((reply) => (this.address = reply.data.addres));

    // if (!this.$auth.user.opted_in) {
    //   this.$auth.fetchUser().then(() => {
    //     if (!this.$auth.user.opted_in) {
    //       this.infoPopupVisible = true;
    //     }
    //   });
    // }
  },
};
</script>
