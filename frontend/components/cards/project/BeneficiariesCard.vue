<template>
  <DefaultCardWithTitle title="Beneficiaries:">
    <v-layout
      column
      ma-0
      v-for="(beneficiary, index) in beneficiaries"
      :key="beneficiary.id"
    >
      <v-divider v-if="index" class="my-3"></v-divider>
      <BeneficiaryDelegate :beneficiary="beneficiary"></BeneficiaryDelegate>
    </v-layout>
  </DefaultCardWithTitle>
</template>

<script>
export default {
  data() {
    return {
      beneficiaries: [
        {
          id: 0,
          first_name: "Jan",
          last_name: "Kowalski",
          status: 0,
        },
        {
          id: 2,
          first_name: "Stan",
          last_name: "Kowalski",
          status: 0,
        },
        {
          id: 3,
          first_name: "Khan",
          last_name: "Kowalski",
          status: 0,
        },
      ],
    };
  },
  components: {
    DefaultCardWithTitle: () =>
      import("@/components/cards/DefaultCardWithTitle"),
    BeneficiaryDelegate: () =>
      import("@/components/delegates/BeneficiaryDelegate"),
  },
};
</script>