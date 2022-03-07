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
            :investment.sync="investment"
            :readonly="status"
          ></InvestmentForm>
        </v-flex>
        <v-flex>
          <BlockButton
            :disabled="project.sync == SYNCING"
            :loading="isSyncing"
            @clicked="
              () => {
                if (status) {
                  openExplorerTransactionLink(investment.txid);
                } else {
                  invest();
                }
              }
            "
            >{{ btnLabel }}</BlockButton
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
import { SYNC } from "@/constants/project";
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
      SYNCING: SYNC.TO_SYNC,
      investment: null,
    };
  },
  computed: {
    status() {
      return this.investment && this.investment.sync == SYNC.SYNCED;
    },
    btnLabel() {
      return this.status ? "Details" : "Invest";
    },
    url() {
      return `projects/${this.project.id}/investments/`;
    },
    isSyncing() {
      return this.investment && (this.investment.sync == SYNC.SYNCING || this.investment.sync == SYNC.TO_SYNC);
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
          .post(`projects/${this.project.id}/investments/`, this.investment)
          .then(() => {
            this.investment.sync = this.SYNCING;
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