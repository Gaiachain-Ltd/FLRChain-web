<template>
  <v-layout row align-center ma-0>
    <DefaultSVGIcon
      class="mr-6 mb-1"
      :size="40"
      :icon="transactionIcon"
    ></DefaultSVGIcon>
    <DefaultText
      size="22"
      :color="
        isReceived
          ? $vuetify.theme.themes.light.primary
          : $vuetify.theme.themes.light.octonary
      "
      >{{ formattedValue }}</DefaultText
    >
    <v-spacer></v-spacer>
    <v-layout column ma-0 align-center>
      <DefaultText size="14">{{ actionText }}</DefaultText>
      <DefaultText size="16" v-if="transaction.project_name">{{
        transaction.project_name
      }}</DefaultText>
    </v-layout>
    <v-spacer></v-spacer>
    <DefaultText
      class="mr-10"
      @clicked="openExplorerLink"
      :color="$vuetify.theme.themes.light.primary"
      clickable
      >Explorer Link
    </DefaultText>
    <DefaultSVGIcon
      class="mb-1 mr-2"
      :icon="require('@/assets/icons/calendar.svg')"
    ></DefaultSVGIcon>
    <DefaultText :color="$vuetify.theme.themes.light.octonary">{{
      formatedDateTime
    }}</DefaultText>
  </v-layout>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  props: {
    transaction: {
      type: Object,
    },
  },
  data() {
    return {
      receivedIcon: require("@/assets/balance/received.svg"),
      sentIcon: require("@/assets/balance/sent.svg"),
    };
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultSVGIcon: () => import("@/components/icons/DefaultSVGIcon"),
  },
  computed: {
    ...mapGetters(["isFacililator"]),
    actionText() {
      switch (this.transaction.action) {
        case 1:
          return "Received";
        case 3:
          return "Return on investment project";
        case 4:
          return "Invest in project";
        case 6:
          return "Facililator fee";
        default:
          return `Action: ${this.transaction.action}`;
      }
    },
    isReceived() {
      switch (this.transaction.action) {
        case 1:
          return true;
        case 3:
          return true;
        case 4:
          return false;
        case 6:
          return this.isFacililator ? true : false;
        default:
          return true;
      }
    },
    transactionIcon() {
      return this.isReceived ? this.receivedIcon : this.sentIcon;
    },
    formattedValue() {
      let sign = this.isReceived ? "+" : "-";
      return `${sign}${parseFloat(this.transaction.amount)} USDC`;
    },
    formatedDateTime() {
      return this.$moment(this.transaction.created).format("HH:mm YYYY-MM-DD");
    },
    explorerSrc() {
      return `https://testnet.algoexplorer.io/tx/${this.transaction.txid}`;
    },
  },
  methods: {
    openExplorerLink() {
      window.open(this.explorerSrc, "_blank");
    },
  },
};
</script>