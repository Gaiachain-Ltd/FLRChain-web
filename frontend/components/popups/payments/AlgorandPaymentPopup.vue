<template>
  <DefaultPopup :show.sync="show">
    <v-layout column slot="content">
      <TextInput
        :label="`Amount (max ${this.maxAmount})*`"
        :text.sync="amount"
        required
      ></TextInput>
      <BlockButton
        :loading="!params || !info || loading"
        @clicked="
          () => {
            this.loading = true;

            const txn = this.onConfirm();

            if (this.kind == 0) {
              this.connector
                .signTransaction(txn.toByte())
                .then((signedTxn) => this.onSend(signedTxn.blob))
                .catch(() =>
                  this.onError('Something went wrong. Please try again later.')
                );
            } else {
              this.connector
                .sendCustomRequest(txn)
                .then((signedTxn) => this.onSend(signedTxn))
                .catch(() =>
                  this.onError('Something went wrong. Please try again later.')
                );
            }
          }
        "
        >CONFIRM</BlockButton
      >
    </v-layout>
  </DefaultPopup>
</template>

<script>
import algosdk from "algosdk";
import { formatJsonRpcRequest } from "@json-rpc-tools/utils";

const USDC = 10458941;
const MYALGOWALLET = 0;
const ALGORANDWALLET = 1;

export default {
  props: {
    value: {},
    connector: {},
    sender: {},
    receiver: {},
    kind: {},
  },
  data() {
    return {
      algodClient: null,
      params: null,
      info: null,
      amount: "0",
      maxAmount: "0",
      address: "",
      loading: false,
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
    DefaultText: () => import("@/components/texts/DefaultText"),
    TextInput: () => import("@/components/inputs/TextInput"),
    DefaultPopup: () => import("@/components/popups/DefaultPopup"),
    BlockButton: () => import("@/components/buttons/BlockButton"),
  },
  methods: {
    onConfirm() {
      const txn = algosdk.makeAssetTransferTxnWithSuggestedParamsFromObject({
        suggestedParams: { ...this.params },
        from: this.address,
        to: this.receiver,
        amount: parseFloat(this.amount),
        assetIndex: USDC,
      });

      if (this.kind == ALGORANDWALLET) {
        const txnsToSign = [
          {
            txn: this.arrayBufferToBase64(
              algosdk.encodeUnsignedTransaction(txn)
            ),
            message: "Top up FLRChain USDC balance.",
          },
        ];

        const requestParams = [txnsToSign];

        const t = formatJsonRpcRequest("algo_signTxn", requestParams);
        return t;
      }
      return txn;
    },
    onSend(signedTxn) {
      if (Array.isArray(signedTxn)) {
        signedTxn = this.convertToUint8Array(signedTxn);
      }
      this.algodClient
        .sendRawTransaction(signedTxn)
        .do()
        .then(() => this.onSuccess("Transaction successful!"))
        .catch(() =>
          this.onError("Something went wrong. Please try again later.")
        );
    },
    arrayBufferToBase64(buffer) {
      var binary = "";
      var bytes = [].slice.call(new Uint8Array(buffer));
      bytes.forEach((b) => (binary += String.fromCharCode(b)));
      return window.btoa(binary);
    },
    convertToUint8Array(arr) {
      const bytes = new Uint8Array(...arr);
      return bytes;
    },
    onSuccess(msg) {
      this.$emit("success", msg);
    },
    onError(msg) {
      this.$emit("error", msg);
    },
  },
  async mounted() {
    if (this.kind == 0) {
      this.address = this.sender.address;
    } else {
      this.address = this.sender.accounts[0];
    }
    this.algodClient = new algosdk.Algodv2(
      "",
      "https://api.testnet.algoexplorer.io",
      ""
    );

    try {
      this.params = await this.algodClient.getTransactionParams().do();
    } finally {
      if (!this.params) {
        this.onError("Unable to fetch wallet info. Please try again later.");
        return;
      }
    }

    try {
      this.info = await this.algodClient.accountInformation(this.address).do();
    } finally {
      if (!this.info) {
        this.onError("Unable to fetch wallet info. Please try again later.");
        return;
      }
    }

    for (let index = 0; index < this.info.assets.length; index++) {
      const asset = this.info.assets[index];
      if (asset["asset-id"] == USDC) {
        this.maxAmount = asset.amount;
        return;
      }
    }

    this.onError(
      "Your wallet don't support USDC. Please add USDC asset to your wallet."
    );
  },
};
</script>