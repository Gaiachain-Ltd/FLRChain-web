<template>
  <v-data-table
    :headers="headers"
    :items="activities"
    no-data-text="No rewards"
    hide-default-footer
    :items-per-page="-1"
  >
    <template v-slot:item.task_name="{ item }">
      {{ item.activity_type == 0 ? `${item.task_name}` : `${item.task_name} (BATCH)`}}
    </template>
    <template v-slot:item.amount="{ item }">
      {{ amount(item) }}
    </template>
    <template v-slot:item.datetime="{ item }">
      {{ datetime(item) }}
    </template>
    <template v-slot:item.request="{ item }">
      <v-layout
        align-center
        v-if="isFacililator && (item.status == INITIAL || item.sync == SYNCING)"
      >
        <ActionButton
          class="mr-1"
          color="white"
          :border="`1px ${$vuetify.theme.themes.light.success} solid !important`"
          :textColor="$vuetify.theme.themes.light.success"
          :loading="item.status == ACCEPTED"
          :disabled="item.status == REJECTED"
          @click.prevent="() => handleApproval(item, ACCEPTED)"
          >Approve</ActionButton
        >
        <ActionButton
          class="ml-1"
          color="white"
          :border="`1px ${$vuetify.theme.themes.light.error} solid !important`"
          :textColor="$vuetify.theme.themes.light.error"
          :loading="item.status == REJECTED"
          :disabled="item.status == ACCEPTED"
          @click.prevent="() => handleApproval(item, REJECTED)"
          >Reject</ActionButton
        >
      </v-layout>
      <div v-else :style="{ color: statusColor(item.status) }">
        {{ status(item.status) }}
      </div>
    </template>
    <template v-slot:item.details="{ item }">
      <v-layout @click.prevent="() => openExplorerTransactionLink(item.txid)">
        <a>See more</a>
      </v-layout>
    </template>
  </v-data-table>
</template>

<script>
import { mapGetters } from "vuex";
import { SYNC, APPROVAL } from "@/constants/project";
import SyncMixin from "@/mixins/SyncMixin";
import AlgoExplorerMixin from "@/mixins/AlgoExplorerMixin";

export default {
  mixins: [AlgoExplorerMixin, SyncMixin],
  props: {
    project: {},
  },
  data() {
    return {
      ACCEPTED: APPROVAL.ACCEPTED,
      REJECTED: APPROVAL.REJECTED,
      INITIAL: APPROVAL.INITIAL,
      SYNCING: SYNC.TO_SYNC,
      activities: [],
      options: {
        sortBy: ["status"],
      },
      headers: [
        {
          text: "Steward",
          value: "name",
        },
        {
          text: "Task name",
          value: "task_name",
        },
        {
          text: "Amount",
          value: "amount",
        },
        {
          text: "Date",
          value: "datetime",
        },
        {
          text: "Request",
          value: "request",
        },
        {
          text: "Details",
          value: "details",
        },
      ],
    };
  },
  computed: {
    ...mapGetters(["isFacililator"]),
    isSyncing() {
      let syncing = false;
      for (let index = 0; index < this.activities.length; index++) {
        const activity = this.activities[index];
        if (activity.sync == SYNC.TO_SYNC) {
          syncing = true;
          break;
        }
      }
      return syncing;
    },
    url() {
      return `projects/${this.project.id}/activities/`;
    },
  },
  methods: {
    amount(item) {
      return `${item.amount} USDC`;
    },
    datetime(item) {
      return this.$moment.unix(item["round-time"]).format("YYYY-MM-DD HH:mm");
    },
    handleApproval(activity, value) {
      this.$set(activity, "status", value);
      this.$set(activity, "sync", this.SYNCING);
      this.$axios
        .put(`projects/${this.project.id}/activities/${activity.id}/`, {
          status: value,
        })
        .then(() => {
          this.requestRefresh();
        });
    },
    status(value) {
      switch (value) {
        case this.INITIAL:
          return "Pending";
        case this.ACCEPTED:
          return "Accepted";
        case this.REJECTED:
          return "Rejected";
        default:
          return value;
      }
    },
    statusColor(value) {
      switch (value) {
        case this.ACCEPTED:
          return this.$vuetify.theme.themes.light.success;
        case this.REJECTED:
          return this.$vuetify.theme.themes.light.error;
        default:
          return undefined;
      }
    },
    onUpdate(value) {
      this.activities = value;
      this.$emit("refresh");
    },
  },
  components: {
    ActionButton: () => import("@/components/buttons/ActionButton"),
  },
  async fetch() {
    await this.$axios.get(this.url).then((reply) => {
      this.activities = reply.data;
      this.requestRefresh();
    });
  },
};
</script>   