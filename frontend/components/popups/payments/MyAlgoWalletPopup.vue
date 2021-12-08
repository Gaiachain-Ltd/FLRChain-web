<template>
  <DefaultPopup :show.sync="show">
    <v-layout column slot="content">
      <TextInput
        :label="`Amount (max ${this.maxAmount})*`"
        :text.sync="amount"
        required
      ></TextInput>
      <BlockButton
        :loading="!params || !info"
        @clicked="
          () => {
            const txn = this.onConfirm();

            if (this.kind == 0) {
              this.connector
                .signTransaction(txn.toByte())
                .then((signedTxn) => this.onSend(signedTxn.blob));
            } else {
              this.connector
                .sendCustomRequest(txn)
                .then((signedTxn) => this.onSend(signedTxn));
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

export default {
  props: {
    value: {},
    connector: {},
    account: {},
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
      console.log("HERE");
      const txn = algosdk.makeAssetTransferTxnWithSuggestedParamsFromObject({
        suggestedParams: { ...this.params },
        from: this.address,
        to: "SAWFVFKRTZLKORKN5J4D4H7MQ3QJBRMWXIVWC7QMB2EAHNYT5CTHEZ2ZNY",
        amount: parseFloat(this.amount),
        assetIndex: USDC,
      });
      console.log("SSS", txn);
      if (this.kind == 1) {
        const txnsToSign = [
          {
            txn: this.arrayBufferToBase64(
              algosdk.encodeUnsignedTransaction(txn)
            ),
            message: "Description of transaction being signed",
            // Note: if the transaction does not need to be signed (because it's part of an atomic group
            // that will be signed by another party), specify an empty singers array like so:
            // signers: [],
          },
        ];
        console.log("TXNS");
        const requestParams = [txnsToSign];

        const t = formatJsonRpcRequest("algo_signTxn", requestParams);
        console.log("TXN", t);
        return t;
      }
      return txn;
    },
    onDebug(tt) {
      console.log(tt);
      console.log(this.base64ToArrayBuffer(tt));
    },
    onSend(signedTxn) {
      if (Array.isArray(signedTxn)) {
        signedTxn = this.convertToUint8Array(signedTxn);
      }
      this.algodClient.sendRawTransaction(signedTxn).do();
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
  },
  async mounted() {
    console.log("SHOWN!!!", this.account);
    if (this.kind == 0) {
      this.address = this.account.address;
    } else {
      this.address = this.account.accounts[0];
    }
    this.algodClient = new algosdk.Algodv2(
      "",
      "https://api.testnet.algoexplorer.io",
      ""
    );
    this.params = await this.algodClient.getTransactionParams().do();
    console.log("PARAMS", this.params);
    this.info = await this.algodClient.accountInformation(this.address).do();
    console.log("INFO", this.info);
    if (!this.info) {
      console.log("NO INFO");
      return;
    }
    for (let index = 0; index < this.info.assets.length; index++) {
      const asset = this.info.assets[index];
      if (asset["asset-id"] == USDC) {
        this.maxAmount = asset.amount;
        return;
      }
    }

    console.log("NOT FOUND!");
  },
};
</script>