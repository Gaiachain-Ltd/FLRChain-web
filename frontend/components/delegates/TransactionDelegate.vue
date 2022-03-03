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
      <DefaultText
        size="18"
        :color="$vuetify.theme.themes.light.octonary"
        v-if="transaction.project_title"
        >{{ transaction.project_title }}</DefaultText
      >
    </v-layout>
    <v-spacer></v-spacer>
    <DefaultText
      class="mr-10"
      @clicked="() => openExplorerTransactionLink(transaction.id)"
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
import AlgoExplorerMixin from "@/mixins/AlgoExplorerMixin";
import algosdk from "algosdk";
import { mapGetters } from "vuex";

export default {
  mixins: [AlgoExplorerMixin],
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
        default:
          return "Sent";
      }
    },
    isReceived() {
      switch (this.transaction.action) {
        case 1:
          return true;
        default:
          return false;
      }
    },
    statusColor() {
      switch (this.transaction.action) {
        case 1:
          return this.$vuetify.theme.themes.light.primary;
        default:
          return this.$vuetify.theme.themes.light.error;
      }
    },
    transactionIcon() {
      return this.isReceived ? this.receivedIcon : this.sentIcon;
    },
    formattedValue() {
      let sign = this.isReceived ? "+" : "-";
      return `${sign}${algosdk.microalgosToAlgos(this.transaction.amount)} USDC`;;
    },
    formatedDateTime() {
      return this.$moment
        .unix(this.transaction["round-time"])
        .format("YYYY-MM-DD HH:mm");
    },
  },
};
</script>