<template>
  <div>
    <DefaultCard>
      <v-layout column>
        <DefaultText
          class="my-3"
          bold
          :color="$vuetify.theme.themes.light.primary"
          >Invest in project</DefaultText
        >
        <v-flex>
          <InvestmentForm
            ref="investmentForm"
            :amount.sync="amount"
            :readonly="!canInvest"
          ></InvestmentForm>
        </v-flex>
        <v-flex>
          <BlockButton
            :disabled="!canInvest"
            :loading="isSyncing"
            @clicked="invest"
            >Invest</BlockButton
          >
        </v-flex>
      </v-layout>
    </DefaultCard>
    <ErrorPopup
      v-if="errorPopupVisible"
      :value.sync="errorPopupVisible"
    ></ErrorPopup>
  </div>
</template>

<script>
import { SYNC, STATUS } from "@/constants/project";
import AlgoExplorerMixin from "@/mixins/AlgoExplorerMixin";
import SyncMixin from "@/mixins/SyncMixin";

export default {
  mixins: [AlgoExplorerMixin, SyncMixin],
  props: {
    project: {},
  },
  data() {
    return {
      errorPopupVisible: false,
      investment: null,
      amount: "",
    };
  },
  computed: {
    canInvest() {
      return (
        this.project.status != STATUS.CLOSED &&
        this.project.sync != SYNC.SYNCING
      );
    },
    url() {
      return `projects/${this.project.id}/investments/`;
    },
    isSyncing() {
      return (
        this.investment &&
        (this.investment.sync == SYNC.SYNCING ||
          this.investment.sync == SYNC.TO_SYNC)
      );
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    ErrorPopup: () => import("@/components/popups/ErrorPopup"),
    DefaultCard: () => import("@/components/cards/DefaultCard"),
    InvestmentForm: () => import("@/components/forms/project/InvestmentForm"),
    BlockButton: () => import("@/components/buttons/BlockButton"),
  },
  methods: {
    invest() {
      if (this.$refs.investmentForm.validate()) {
        this.$axios
          .post(`projects/${this.project.id}/investments/`, {
            amount: this.amount,
          })
          .then(() => {
            this.investment.sync = SYNC.SYNCING;
            this.requestRefresh();
          })
          .catch(() => (this.errorPopupVisible = true));
      }
    },
    onUpdate(value) {
      this.investment = value;
      this.$emit("refresh");
    },
  },
  async fetch() {
    await this.$axios.get(this.url).then((reply) => {
      this.investment = reply.data;
      this.requestRefresh();
    });
  },
};
</script>