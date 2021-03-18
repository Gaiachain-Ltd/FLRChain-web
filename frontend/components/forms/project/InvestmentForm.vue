<template>
  <v-layout column>
    <v-layout row ma-0>
      <v-flex mr-3 class="date-style">
        <DateInput label="Start date" :text.sync="investment.start"></DateInput>
      </v-flex>
      <v-flex ml-3 class="date-style">
        <DateInput label="End date" :text.sync="investment.end"></DateInput>
      </v-flex>
    </v-layout>
    <v-flex>
      <TextInput
        label="Coins for investment"
        :text.sync="investment.amount"
      ></TextInput>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  props: {
    investment: {},
  },
  components: {
    TextInput: () => import("@/components/inputs/TextInput"),
    DateInput: () => import("@/components/inputs/DateInput"),
  },
};
</script>

<style scoped>
.date-style {
  min-width: 100px;
  width: 100px;
}
</style>