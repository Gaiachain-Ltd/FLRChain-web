<template>
  <DefaultPopup :show.sync="show">
    <v-layout column slot="content">
      <BlockButton>Credit Card</BlockButton>
      <BlockButton
        @clicked="
          () => {
            this.connector = this.MyAlgoWalletInit();
            this.connector
              .connect({ shouldSelectOneAccount: true })
              .then((accounts) => {
                this.account = accounts[0];
                this.onContinue();
              });
          }
        "
        >MyAlgoWallet</BlockButton
      >
      <BlockButton
        @clicked="
          () => {
            this.connector = this.AlgorandWalletInit();
            if (!this.connector.connected) {
              this.connector.createSession();
            }
            // Subscribe to connection events
            this.connector.on('connect', (error, payload) => {
              if (error) {
                throw error;
              }

              // Get provided accounts
              this.account = payload.params[0];
              this.onContinue();
            });

            this.connector.on('session_update', (error, payload) => {
              if (error) {
                throw error;
              }

              // Get updated accounts
              this.account = payload.params[0];
              this.onContinue();
            });

            this.connector.on('disconnect', (error, payload) => {
              if (error) {
                throw error;
              }
            });
          }
        "
        >Algorand Wallet</BlockButton
      >
    </v-layout>
    <MyAlgoWAlletPopup
      :value.sync="showMyAlgoWalletPopup"
      :connector="connector"
      :account="account"
      :kind="kind"
      v-if="showMyAlgoWalletPopup"
    ></MyAlgoWAlletPopup>
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
  },
  data() {
    return {
      showMyAlgoWalletPopup: false,
      connector: null,
      account: null,
      kind: MYALGOWALLET
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
    DefaultPopup: () => import("@/components/popups/DefaultPopup"),
    BlockButton: () => import("@/components/buttons/BlockButton"),
    MyAlgoWAlletPopup: () =>
      import("@/components/popups/payments/MyAlgoWalletPopup"),
  },
  methods: {
    onMyAlgoWallet() {
      this.showMyAlgoWalletPopup = true;
    },
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
    onContinue() {
      this.showMyAlgoWalletPopup = true;
    },
  },
  beforeDestroy() {
    if (this.kind == ALGORANDWALLET) {
      this.connector.killSession();
    }
  }
};
</script>