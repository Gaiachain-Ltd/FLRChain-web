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
import algosdk from "algosdk";
import AlgoExplorerMixin from "@/mixins/AlgoExplorerMixin";

export default {
  mixins: [AlgoExplorerMixin],
  props: {
    project: {},
  },
  data() {
    return {
      errorPopupVisible: false,
      SYNCING: SYNC.TO_SYNC,
      investment: {
        amount: "0",
      },
    };
  },
  computed: {
    status() {
      return this.investment && this.investment.status;
    },
    btnLabel() {
      return this.status ? "Details" : "Invest";
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
            this.invested = true;
            this.$emit("refresh");
          })
          .catch(() => (this.errorPopupVisible = true));
      }
    },
  },
  async fetch() {
    this.investment = await this.$axios
      .get(`projects/${this.project.id}/investments/`)
      .then((reply) => reply.data);
    if (this.investment.status) {
      this.investment.amount = algosdk.microalgosToAlgos(this.investment.amount)
    }
  },
};
</script>