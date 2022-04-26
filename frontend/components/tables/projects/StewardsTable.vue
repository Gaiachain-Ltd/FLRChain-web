<template>
  <v-data-table
    :headers="headers"
    :items="beneficiaries"
    :options.sync="options"
    hide-default-footer
    no-data-text="No stewards"
    :items-per-page="-1"
  >
    <template v-slot:item.name="{ item }">
      <StewardCell
        :profile="{ name: item.name, id: item.user_id }"
      ></StewardCell>
    </template>
    <template v-slot:item.round-time="{ item }">
      {{ datetime(item) }}
    </template>
    <template v-slot:item.status="{ item }">
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
      <v-layout
        @click.prevent="
          () => {
            if (item.status != INITIAL && item.sync != SYNCING) {
              openExplorerTransactionLink(item.approval_txid);
            } else {
              openExplorerTransactionLink(item.optin_txid);
            }
          }
        "
      >
        <a href="">See more</a>
      </v-layout>
    </template>
  </v-data-table>
</template>

<script>
import { mapGetters } from "vuex";
import SyncMixin from "@/mixins/SyncMixin";
import AlgoExplorerMixin from "@/mixins/AlgoExplorerMixin";
import { SYNC, APPROVAL } from "@/constants/project";
import _ from "lodash";

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
      beneficiaries: [],
      options: {
        sortBy: ["approval"],
      },
      headers: [
        {
          text: "Steward",
          value: "name",
        },
        {
          text: "Date",
          value: "round-time",
        },
        {
          text: "Location",
          value: "village",
        },
        {
          text: "Request",
          value: "status",
        },
        {
          text: "Details",
          value: "details",
          sortable: false,
        },
      ],
    };
  },
  computed: {
    ...mapGetters(["isFacililator"]),
    isSyncing() {
      let syncing = false;
      for (let index = 0; index < this.beneficiaries.length; index++) {
        const beneficiary = this.beneficiaries[index];
        if (beneficiary.sync == SYNC.TO_SYNC) {
          syncing = true;
          break;
        }
      }
      return syncing;
    },
    url() {
      return `projects/${this.project.id}/assignments/`;
    },
  },
  methods: {
    datetime(item) {
      return this.$moment.unix(item["round-time"]).format("YYYY-MM-DD HH:mm");
    },
    handleApproval(beneficiary, value) {
      this.$set(beneficiary, "status", value);
      this.$set(beneficiary, "sync", this.SYNCING);
      this.$axios
        .put(`projects/assignments/${beneficiary.id}/`, {
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
      this.beneficiaries = value;
    },
  },
  components: {
    ActionButton: () => import("@/components/buttons/ActionButton"),
    StewardCell: () => import("@/components/tables/projects/StewardCell"),
  },
  mounted() {
    this.requestRefresh();
  },
  async fetch() {
    await this.$axios.get(this.url).then((reply) => {
      this.onUpdate(reply.data);
      this.requestRefresh();
    });
  },
};
</script>   