<template>
  <v-layout
    row
    ma-0
    class="delegate"
    @click.prevent="openExplorerTransactionLink(investor.id)"
    v-ripple
  >
    <DefaultText :color="color" :size="14">{{ name }}</DefaultText>
    <v-spacer></v-spacer>
    <DefaultText :color="color" :size="14">{{ amount }}</DefaultText>
    <div class="separator mx-1"></div>
    <DefaultText :color="color" :size="14">{{ datetime }}</DefaultText>
  </v-layout>
</template>

<script>
import algosdk from "algosdk";
import AlgoExplorerMixin from "@/mixins/AlgoExplorerMixin";

export default {
  mixins: [AlgoExplorerMixin],
  props: {
    investor: {
      type: Object,
    },
  },
  computed: {
    name() {
      if (this.investor.first_name || this.investor.last_name) {
        return `${this.investor.first_name} ${this.investor.last_name}`;
      } else {
        return this.investor.sender;
      }
    },
    datetime() {
      console.log("TD", this.investor["round-time"]);
      return this.$moment
        .unix(this.investor["round-time"])
        .format("YYYY-MM-DD");
    },
    amount() {
      return `${algosdk.microalgosToAlgos(this.investor.amount)} USDC`;
    },
    color() {
      return this.$vuetify.theme.themes.light.nonary;
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>

<style scoped>
.delegate {
  cursor: pointer;
}
.delegate:hover {
  opacity: 0.8;
}
.separator {
  width: 2px;
  min-width: 2px;
  height: 18px;
  background-color: #dce0e7;
}
</style>