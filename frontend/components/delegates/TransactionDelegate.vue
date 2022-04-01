<template>
  <v-row align-center>
    <v-col>
      <v-layout align-center>
        <DefaultSVGIcon
          class="mr-6 mb-1"
          :size="40"
          :icon="transactionIcon"
        ></DefaultSVGIcon>
        <DefaultText
          size="22"
          :color="
            isReceived
              ? $vuetify.theme.themes.light.success
              : $vuetify.theme.themes.light.error
          "
          >{{ formattedValue }}</DefaultText
        >
      </v-layout>
    </v-col>
    <v-spacer></v-spacer>
    <v-col>
      <DefaultText size="14">Project</DefaultText>
      <DefaultText size="18" :color="$vuetify.theme.themes.light.octonary">{{
        transaction.project_name ? transaction.project_name : "-"
      }}</DefaultText>
    </v-col>
    <v-col>
      <DefaultText size="14">Action</DefaultText>
      <DefaultText size="18" :color="$vuetify.theme.themes.light.octonary">{{
        actionText
      }}</DefaultText>
    </v-col>
    <v-spacer></v-spacer>
    <v-col>
      <v-layout align-center fill-height>
        <DefaultSVGIcon
          class="mb-1 mr-2"
          :icon="require('@/assets/icons/calendar.svg')"
        ></DefaultSVGIcon>
        <DefaultText :color="$vuetify.theme.themes.light.octonary">{{
          transaction["created"]
        }}</DefaultText>
      </v-layout>
    </v-col>
    <v-col shrink>
      <v-layout justify-center align-center fill-height>
      <DefaultText
        class="mr-10"
        @clicked="() => openExplorerTransactionLink(transaction.id)"
        :color="$vuetify.theme.themes.light.primary"
        clickable
        >Details
      </DefaultText>
      </v-layout>
    </v-col>
  </v-row>
</template>

<script>
import AlgoExplorerMixin from "@/mixins/AlgoExplorerMixin";
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
      receivedIcon: require("@/assets/balance/Up.svg"),
      sentIcon: require("@/assets/balance/Down.svg"),
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
      return `${sign}${ this.transaction.amount } USDC`;
    },
  },
};
</script>