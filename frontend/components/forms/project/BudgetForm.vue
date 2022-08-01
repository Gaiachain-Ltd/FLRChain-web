<template>
  <v-form ref="form" @submit.prevent>
    <v-layout column>
      <DefaultText class="mb-3" :color="$vuetify.theme.themes.light.primary"
        >Budget</DefaultText
      >
      <TextInput
        label="Facilitator administration funds"
        v-model="project.fac_adm_funds"
        :rules="facAdmFundsRules"
        :readonly="readonly"
        :icon="icon"
      >
        <DefaultText slot="append" size="12">{{
          `(${facAdmFundsShare}%)`
        }}</DefaultText>
      </TextInput>
      <TextInput
        label="Total task rewards"
        v-model="totalRewards"
        readonly
        :icon="icon"
      >
        <DefaultText class="append-readonly" slot="append" size="12">{{
          `(${rewardsShare}%)`
        }}</DefaultText>
      </TextInput>
      <TextInput label="Total batch" v-model="totalBatch" readonly :icon="icon">
        <DefaultText class="append-readonly" slot="append" size="12">{{
          `(${batchesShare}%)`
        }}</DefaultText>
      </TextInput>
      <TextInput label="Total" v-model="total" readonly :icon="icon">
        <DefaultText class="append-readonly" slot="append" size="12"
          >(100%)</DefaultText
        >
      </TextInput>
    </v-layout>
  </v-form>
</template>

<script>
import ValidatorMixin from "@/validators";
import ProjectMixin from "@/mixins/ProjectMixin";
import { STATUS } from "@/constants/project";

export default {
  mixins: [ProjectMixin, ValidatorMixin],
  props: {
    project: {},
    readonly: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      facAdmFunds: this.project && this.project.fac_adm_funds ? this.project.fac_adm_funds : 0.0, 
      icon: require("@/assets/icons/currency.svg"),
    };
  },
  computed: {
    facAdmFundsRules() {
      if (this.project && this.project.status == STATUS.FUNDRAISING) {
        return [...this.requiredRules, ...this.decimalRules];
      } else {
        [...this.requiredRules, ...this.decimalRules, ...this.noLessThan(this.facAdmFunds)];
      }
    }
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    TextInput: () => import("@/components/inputs/TextInput"),
  },
  methods: {
    validate() {
      return this.$refs.form.validate();
    },
  },
};
</script>

<style scoped>
.append-readonly {
  margin-top: 15px !important;
}
</style>