<template>
  <v-form ref="form">
    <v-layout column>
      <v-flex>
        <TextInput
          label="Amount*"
          v-model="card.amount"
          placeholder="Amount..."
          :mask="'##########'"
          :rules="[...requiredRules, ...decimalRules, ...nonZeroDecimalRules]"
        ></TextInput>
      </v-flex>
      <v-flex>
        <CCNumberInput
          label="Card number*"
          placeholder="Credit card number..."
          :text.sync="card.number"
        ></CCNumberInput>
      </v-flex>
      <v-layout row ma-0>
        <v-flex xs5>
          <CVVInput
            label="CVV*"
            :text.sync="card.cvv"
            placeholder="###"
          ></CVVInput>
        </v-flex>
        <v-spacer></v-spacer>
        <v-flex xs5>
          <CCExpInput
            label="Expiry*"
            :text.sync="card.expiry"
            placeholder="##/###"
          ></CCExpInput>
        </v-flex>
      </v-layout>
    </v-layout>
  </v-form>
</template>

<script>
import ValidatorMixin from "@/validators";

export default {
  mixins: [ValidatorMixin],
  props: {
    card: {},
  },
  components: {
    CVVInput: () => import("@/components/inputs/CVVInput"),
    CCNumberInput: () => import("@/components/inputs/CCNumberInput"),
    CCExpInput: () => import("@/components/inputs/CCExpInput"),
    TextInput: () => import("@/components/inputs/TextInput"),
  },
  methods: {
    validate() {
      return this.$refs.form.validate();
    }
  }
};
</script>