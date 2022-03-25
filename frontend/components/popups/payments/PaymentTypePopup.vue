<template>
  <DefaultPopup :show.sync="show">
    <v-layout slot="icon">
    </v-layout>
    <v-layout column slot="content" ma-6>
      <BlockButton @clicked="onShowCardPopup">
        <v-layout align-center shrink>
          <DefaultSVGIcon
            class="mr-1"
            :icon="require('@/assets/payments/circle.svg')"
            :size="19"
          ></DefaultSVGIcon
          ><span>Credit Card (Circle)</span>
        </v-layout></BlockButton
      >
      <BlockButton
        class="mt-3"
        @clicked="
          () => {
            this.connector = this.MyAlgoWalletInit();
            this.connector
              .connect({ shouldSelectOneAccount: true })
              .then((accounts) => {
                this.account = accounts[0];
                this.onShowWalletPopup();
              })
              .catch(() =>
                this.onError(
                  'Unable to init MyAlgoWallet. Please try again later.'
                )
              );
          }
        "
      >
        <v-layout align-center shrink>
          <DefaultSVGIcon
            class="mr-1"
            :icon="require('@/assets/payments/myalgowallet.svg')"
            :size="19"
          ></DefaultSVGIcon
          ><span>MyAlgoWallet</span>
        </v-layout></BlockButton
      >
      <BlockButton
        class="mt-3"
        @clicked="
          () => {
            this.connector = this.AlgorandWalletInit();
            if (!this.connector.connected) {
              this.connector.createSession();
            }
            // Subscribe to connection events
            this.connector.on('connect', (error, payload) => {
              if (error) {
                this.onError(
                  'Unable to connect to Algorand Wallet. Please try again later.'
                );
                return;
              }

              // Get provided accounts
              this.account = payload.params[0];
              this.onShowWalletPopup();
            });

            this.connector.on('session_update', (error, payload) => {
              if (error) {
                this.onError(
                  'Unable to connect to Algorand Wallet. Please try again later.'
                );
                return;
              }

              // Get updated accounts
              this.account = payload.params[0];
              this.onShowWalletPopup();
            });

            this.connector.on('disconnect', (error, payload) => {
              if (error) {
                this.onError('Something went wrong. Please try again later.');
                return;
              }
            });
          }
        "
      >
        <v-layout align-center shrink>
          <DefaultSVGIcon
            class="mr-1"
            :icon="require('@/assets/payments/algorand_wallet.svg')"
            :size="19"
          ></DefaultSVGIcon
          ><span>Algorand Wallet</span>
        </v-layout></BlockButton
      >
      <ActionButton
        class="mt-3"
        color="white"
        :border="`1px ${$vuetify.theme.themes.light.primary} solid !important`"
        :textColor="`${$vuetify.theme.themes.light.primary} !important`"
        @click.prevent="show = false"
        >Cancel</ActionButton
      >
    </v-layout>
    <AlgorandPaymentPopup
      v-if="showWalletPopup"
      :value.sync="showWalletPopup"
      :connector="connector"
      :sender="account"
      :receiver="address"
      :kind="kind"
      @success="onSuccess"
      @error="onError"
    ></AlgorandPaymentPopup>
    <CreditCardPaymentPopup
      v-if="showCardPopup"
      :value.sync="showCardPopup"
      @success="onSuccess"
      @error="onError"
    ></CreditCardPaymentPopup>
  </DefaultPopup>
</template>

<script>
import MyAlgoConnect from "@randlabs/myalgo-connect";
import WalletConnect from "@walletconnect/client";
import QRCodeModal from "algorand-walletconnect-qrcode-modal";

const MYALGOWALLET = 0;
const ALGORANDWALLET = 1;

export default {
  props: {
    value: {},
    address: {},
  },
  data() {
    return {
      showWalletPopup: false,
      showCardPopup: false,
      connector: null,
      account: null,
      kind: MYALGOWALLET,
    };
  },
  computed: {
    show: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("update:value", value);
      },
    },
  },
  components: {
    ActionButton: () => import("@/components/buttons/ActionButton"),
    DefaultSVGIcon: () => import("@/components/icons/DefaultSVGIcon"),
    DefaultPopup: () => import("@/components/popups/DefaultPopup"),
    BlockButton: () => import("@/components/buttons/BlockButton"),
    CreditCardPaymentPopup: () =>
      import("@/components/popups/payments/CreditCardPaymentPopup"),
    AlgorandPaymentPopup: () =>
      import("@/components/popups/payments/AlgorandPaymentPopup"),
  },
  methods: {
    MyAlgoWalletInit() {
      this.kind = MYALGOWALLET;
      return new MyAlgoConnect();
    },
    AlgorandWalletInit() {
      this.kind = ALGORANDWALLET;
      return new WalletConnect({
        bridge: "https://bridge.walletconnect.org", // Required
        qrcodeModal: QRCodeModal,
      });
    },
    onShowWalletPopup() {
      this.showWalletPopup = true;
    },
    onShowCardPopup() {
      this.showCardPopup = true;
    },
    onSuccess(msg) {
      this.$emit("success", msg);
      this.onReset();
    },
    onError(msg) {
      this.$emit("error", msg);
      this.onReset();
    },
    onReset() {
      this.showWalletPopup = false;
      this.showCardPopup = false;

      if (this.kind == ALGORANDWALLET) {
        this.connector.killSession();
      }

      this.connector = null;
      this.account = null;
    },
  },
  beforeDestroy() {
    if (this.kind == ALGORANDWALLET && this.connector) {
      this.connector.killSession();
    }
  },
};
</script>