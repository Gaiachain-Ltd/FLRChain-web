<template>
  <v-layout row ma-0>
    <v-flex>
      <DefaultText :size="14">{{ name }}</DefaultText>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  props: {
    beneficiary: {},
  },
  computed: {
    name() {
      return `${this.beneficiary.first_name} ${this.beneficiary.last_name}`;
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>