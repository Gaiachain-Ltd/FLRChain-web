<template>
  <v-form ref="form">
    <v-layout column>
      <v-flex>
        <TextInput
          label="Cardholder name*"
          :text.sync="billingDetails.name"
        ></TextInput>
      </v-flex>
      <v-flex>
        <TextInput
          label="Address line 1*"
          :text.sync="billingDetails.line1"
        ></TextInput>
      </v-flex>
      <v-layout row ma-0>
        <v-flex xs5>
          <TextInput label="City*" :text.sync="billingDetails.city"></TextInput>
        </v-flex>
        <v-spacer></v-spacer>
        <v-flex xs5>
          <TextInput
            label="Postalcode*"
            :text.sync="billingDetails.postalCode"
          ></TextInput>
        </v-flex>
      </v-layout>
      <v-flex>
        <TextInput
          label="Country code*"
          :text.sync="billingDetails.country"
        ></TextInput>
      </v-flex>
      <v-flex>
        <TextInput label="Email*" :text.sync="billingDetails.email"></TextInput>
      </v-flex>
    </v-layout>
  </v-form>
</template>

<script>
export default {
  props: {
    billingDetails: {},
  },
  components: {
    TextInput: () => import("@/components/inputs/TextInput"),
  },
};
</script>