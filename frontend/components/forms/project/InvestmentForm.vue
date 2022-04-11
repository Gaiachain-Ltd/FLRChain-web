<template>
  <v-form ref="form" @submit.prevent>
    <v-layout column>
      <TextInput
        v-if="investment"
        label="Coins for investment*"
        v-model="investment.amount"
        :rules="[...requiredRules, ...decimalRules, ...nonZeroDecimalRules]"
        :icon="icon"
        :readonly="readonly"
        required
      ></TextInput>
    </v-layout>
  </v-form>
</template>

<script>
import ValidatorMixin from "@/validators";

export default {
  mixins: [ValidatorMixin],
  props: {
    investment: {},
    readonly: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      icon: require("@/assets/icons/currency.svg"),
    };
  },
  components: {
    TextInput: () => import("@/components/inputs/TextInput"),
    DateInput: () => import("@/components/inputs/DateInput"),
  },
  methods: {
    validate() {
      return this.$refs.form.validate();
    },
  },
};
</script>

<style scoped>
.date-style {
  min-width: 100px;
  width: 100px;
}
</style>