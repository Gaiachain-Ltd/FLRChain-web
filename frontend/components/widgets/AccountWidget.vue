<template>
  <v-layout column ma-0>
    <v-flex v-if="isFacililator">
      <AccountWidgetDelegate
        label="Your projects:"
        :value="projectCount"
      ></AccountWidgetDelegate>
    </v-flex>
    <v-flex v-else>
      <AccountWidgetDelegate
        label="All:"
        :value="total"
        usdc
      ></AccountWidgetDelegate>
    </v-flex>
    <v-flex v-if="isFacililator">
      <AccountWidgetDelegate
        label="Active projects:"
        :value="projectActiveCount"
      ></AccountWidgetDelegate>
    </v-flex>
    <v-flex v-else>
      <AccountWidgetDelegate
        label="Invested:"
        :value="spent"
        usdc
      ></AccountWidgetDelegate>
    </v-flex>
    <v-flex mt-2>
      <AccountWidgetDelegate
        label="Balance:"
        :value="balance"
        usdc
      ></AccountWidgetDelegate>
    </v-flex>
  </v-layout>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      total: 0,
      spent: 0,
      balance: 0,
      projectCount: 0,
      projectActiveCount: 0,
    };
  },
  computed: {
    ...mapGetters(["isFacililator"]),
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    AccountWidgetDelegate: () =>
      import("@/components/delegates/AccountWidgetDelegate"),
  },
  async fetch() {
    const balanceInfo = await this.$axios
      .get("accounts/")
      .then((reply) => reply.data);
    this.total = balanceInfo.total;
    this.spent = balanceInfo.spent;
    this.balance = balanceInfo.balance;

    if (this.isFacililator) {
      this.projectCount = await this.$axios
        .get("projects/")
        .then((reply) => reply.data.count);

      this.projectActiveCount = await this.$axios
        .get("projects/", { investment__isnull: false })
        .then((reply) => reply.data.count);
    }
  },
};
</script>