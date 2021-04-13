<template>
  <v-form ref="form">
    <v-layout column>
      <v-layout row ma-0>
        <v-flex mr-3 class="date-style">
          <DateInput
            label="Start date*"
            :text.sync="investment.start"
            :rules="[...requiredRules, ...dateRules]"
            required
          ></DateInput>
        </v-flex>
        <v-flex ml-3 class="date-style">
          <DateInput
            label="End date*"
            :text.sync="investment.end"
            :rules="[...requiredRules, ...dateRules]"
            required
          ></DateInput>
        </v-flex>
      </v-layout>
      <v-flex>
        <TextInput
          label="Coins for investment*"
          :text.sync="investment.amount"
          :rules="[...requiredRules, ...decimalRules, ...nonZeroDecimalRules]"
          :icon="icon"
          required
        ></TextInput>
      </v-flex>
    </v-layout>
  </v-form>
</template>

<script>
import ValidatorMixin from "@/validators";

export default {
  mixins: [ValidatorMixin],
  props: {
    investment: {},
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