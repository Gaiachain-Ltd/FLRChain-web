<template>
  <v-layout row ma-0 align-center>
    <v-flex>
      <DefaultText :size="14">{{ name }}</DefaultText>
    </v-flex>
    <v-spacer></v-spacer>
    <v-flex shrink v-if="assignment.status === 1">
      <DefaultText :size="14" :color="$vuetify.theme.themes.light.primary"
        >Accepted</DefaultText
      >
    </v-flex>
    <v-flex shrink v-if="assignment.status === 0">
      <DefaultText :size="14" :color="$vuetify.theme.themes.light.error"
        >Rejected</DefaultText
      >
    </v-flex>
    <v-flex shrink v-if="assignment.status === 2">
      <AnswerRequestButton
        :assignment="assignment"
        @refresh="$emit('refresh')"
      ></AnswerRequestButton>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  props: {
    assignment: {},
  },
  computed: {
    name() {
      return `${this.assignment.beneficiary.first_name} ${this.assignment.beneficiary.last_name}`;
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    AnswerRequestButton: () =>
      import("@/components/buttons/AnswerRequestButton"),
  },
};
</script>