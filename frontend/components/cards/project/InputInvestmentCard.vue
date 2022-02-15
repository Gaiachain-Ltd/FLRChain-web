<template>
  <div>
    <DefaultCard>
      <v-layout column>
        <DefaultText class="my-3" bold :color="$vuetify.theme.themes.light.primary"
          >Invest in project</DefaultText
        >
        <v-flex>
          <InvestmentForm
            ref="investmentForm"
            :investment.sync="investment"
          ></InvestmentForm>
        </v-flex>
        <v-flex>
          <BlockButton :disabled="disabled" @clicked="invest"
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
export default {
  props: {
    project: {},
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      errorPopupVisible: false,
      investment: {
        amount: "0",
        start: this.project.start,
        end: this.project.end,
      },
    };
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    ErrorPopup: () => import("@/components/popups/ErrorPopup"),
    DefaultCard: () =>
      import("@/components/cards/DefaultCard"),
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
  },
};
</script>