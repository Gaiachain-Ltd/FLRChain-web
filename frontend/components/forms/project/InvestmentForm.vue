<template>
  <v-form ref="form" @submit.prevent>
    <v-layout column>
      <TextInput
        label="Coins for investment*"
        v-model="internalAmount"
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
    amount: {},
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
  computed: {
    internalAmount: {
      get() {
        return this.amount;
      },
      set(value) {
        this.$emit('update:amount', value);
      }
    }
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