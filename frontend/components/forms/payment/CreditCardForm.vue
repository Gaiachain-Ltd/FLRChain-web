<template>
  <v-form ref="form">
    <v-layout column>
      <v-flex>
        <TextInput label="Amount*" :text.sync="card.amount"></TextInput>
      </v-flex>
      <v-flex>
        <TextInput label="Card number*" :text.sync="card.number"></TextInput>
      </v-flex>
      <v-layout row ma-0>
        <v-flex xs5>
          <TextInput label="CVV*" :text.sync="card.cvv"></TextInput>
        </v-flex>
        <v-spacer></v-spacer>
        <v-flex xs5>
          <TextInput label="Expiry*" :text.sync="card.expiry"></TextInput>
        </v-flex>
      </v-layout>
      <v-divider class="mb-6"></v-divider>
      <v-flex>
        <TextInput label="Cardholder name*" :text.sync="card.billingDetails.name"></TextInput>
      </v-flex>
      <v-flex>
        <TextInput label="Address line 1*" :text.sync="card.billingDetails.line1"></TextInput>
      </v-flex>
      <v-flex>
        <TextInput label="Address line 2" :text.sync="card.billingDetails.line2"></TextInput>
      </v-flex>
      <v-flex>
        <TextInput label="Postalcode*" :text.sync="card.billingDetails.postalCode"></TextInput>
      </v-flex>
      <v-flex>
        <TextInput label="District" :text.sync="card.billingDetails.district"></TextInput>
      </v-flex>
      <v-flex>
        <TextInput label="City*" :text.sync="card.billingDetails.city"></TextInput>
      </v-flex>
      <v-flex>
        <TextInput label="Country code*" :text.sync="card.billingDetails.country"></TextInput>
      </v-flex>
      <v-flex>
        <TextInput label="Phone" :text.sync="card.phoneNumber"></TextInput>
      </v-flex>
      <v-flex>
        <TextInput label="Email*" :text.sync="card.email"></TextInput>
      </v-flex>
    </v-layout>
  </v-form>
</template>

<script>
export default {
  props: {
    card: {},
  },
  components: {
    TextInput: () => import("@/components/inputs/TextInput"),
  },
};
</script>