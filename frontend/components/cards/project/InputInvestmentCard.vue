<template>
  <div>
    <DefaultCardWithTitle title="Invest in project:">
      <v-layout column ma-0>
        <v-flex>
          <InvestmentForm
            ref="investmentForm"
            :investment.sync="investment"
          ></InvestmentForm>
        </v-flex>
        <v-flex>
          <BlockButton @clicked="invest">Invest</BlockButton>
        </v-flex>
      </v-layout>
    </DefaultCardWithTitle>
    <ErrorPopup
      v-if="errorPopupVisible"
      :value.sync="errorPopupVisible"
    ></ErrorPopup>
  </div>
</template>

<script>
export default {
  props: {
    project: {},
  },
  data() {
    return {
      errorPopupVisible: false,
      investment: {
        amount: "0",
        start: this.project.start,
        end: this.project.end
      },
    };
  },
  components: {
    ErrorPopup: () => import("@/components/popups/ErrorPopup"),
    DefaultCardWithTitle: () =>
      import("@/components/cards/DefaultCardWithTitle"),
    InvestmentForm: () => import("@/components/forms/project/InvestmentForm"),
    BlockButton: () => import("@/components/buttons/BlockButton"),
  },
  methods: {
    invest() {
      if (this.$refs.investmentForm.validate()) {
        this.$axios
          .post(
            `projects/${this.$route.params.id}/investments/`,
            this.investment
          )
          .then(() => this.$emit("refresh"))
          .catch(() => (this.errorPopupVisible = true));
      }
    },
  }
};
</script>