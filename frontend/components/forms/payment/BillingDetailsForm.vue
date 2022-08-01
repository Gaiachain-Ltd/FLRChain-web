<template>
  <v-form ref="form">
    <v-layout column>
      <v-flex>
        <TextInput
          label="Cardholder name*"
          v-model="billingDetails.name"
          :rules="[...requiredRules]"
          placeholder="Card holder name..."
        ></TextInput>
      </v-flex>
      <v-flex>
        <TextInput
          label="Address*"
          v-model="billingDetails.address"
          :rules="[...requiredRules]"
          placeholder="Address..."
        ></TextInput>
      </v-flex>
      <v-layout row ma-0>
        <v-flex xs5>
          <TextInput
            label="City*"
            v-model="billingDetails.city"
            :rules="[...requiredRules]"
            placeholder="City..."
          ></TextInput>
        </v-flex>
        <v-spacer></v-spacer>
        <v-flex xs5>
          <TextInput
            label="Postalcode*"
            v-model="billingDetails.postalCode"
            :rules="[...requiredRules]"
            placeholder="Postalcode..."
          ></TextInput>
        </v-flex>
      </v-layout>
      <v-flex>
        <CountryAutocomplete
          label="Country*"
          :text.sync="billingDetails.country"
        ></CountryAutocomplete>
      </v-flex>
      <v-flex
        v-if="billingDetails.country == 'US' || billingDetails.country == 'CA'"
      >
        <TextInput
          label="District*"
          v-model="billingDetails.district"
          :rules="[...requiredRules]"
          mask="AA"
          placeholder="District (2-letter)..."
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
    billingDetails: {},
  },
  components: {
    TextInput: () => import("@/components/inputs/TextInput"),
    CountryAutocomplete: () =>
      import("@/components/inputs/CountryAutocomplete"),
  },
  methods: {
    validate() {
      return this.$refs.form.validate();
    },
  },
};
</script>