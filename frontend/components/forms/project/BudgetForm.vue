<template>
  <v-layout column>
    <DefaultText class="mb-3" :color="$vuetify.theme.themes.light.primary"
      >Budget</DefaultText
    >
    <TextInput
      label="Facilitator administration funds"
      v-model="project.fac_adm_funds"
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
</template>

<script>
import ProjectMixin from "@/mixins/ProjectMixin";

export default {
  mixins: [ProjectMixin],
  props: {
    project: {},
    readonly: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      icon: require("@/assets/icons/currency.svg"),
    };
  },
  computed: {},
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    TextInput: () => import("@/components/inputs/TextInput"),
  },
};
</script>

<style scoped>
.append-readonly {
  margin-top: 15px !important;
}
</style>