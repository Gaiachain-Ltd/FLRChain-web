<template>
  <v-layout row align-center ma-0>
    <DefaultText size="22">{{ transaction.amount }}</DefaultText>
    <v-spacer></v-spacer>
    <v-layout column ma-0>
      <DefaultText size="14">{{ transaction.action }}</DefaultText>
      <DefaultText size="16" v-if="transaction.project_name">{{
        transaction.project_name
      }}</DefaultText>
    </v-layout>
    <v-spacer></v-spacer>
    <DefaultText>{{ transaction.created }}</DefaultText>
  </v-layout>
</template>

<script>
export default {
  props: {
    transaction: {
      type: Object,
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>