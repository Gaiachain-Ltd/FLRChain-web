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
        :value="allocated"
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
  timers: {
    refresh: { time: 30000, autostart: true, repeat: true },
  },
  data() {
    return {
      total: 0,
      allocated: 0,
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
  methods: {
    refresh() {
      this.$fetch();
    },
  },
  async fetch() {
    const balanceInfo = await this.$axios
      .get("accounts/")
      .then((reply) => reply.data);
    this.allocated = balanceInfo.allocated;
    this.balance = balanceInfo.balance;
    this.total = this.allocated + this.balance;

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