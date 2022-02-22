<template>
  <v-layout>
    <DefaultText>{{ steward.name }}</DefaultText>
    <v-spacer></v-spacer>
    <DefaultText :color="statusColor(steward.approval)" bold>{{
      status(steward.approval)
    }}</DefaultText>
  </v-layout>
</template>

<script>
export default {
  props: {
    steward: {},
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
  methods: {
    status(value) {
      switch (value) {
        case 0:
          return "Pending";
        case 1:
          return "Accepted";
        case 2:
          return "Rejected";
        default:
          return value;
      }
    },
    statusColor(value) {
      switch (value) {
        case 1:
          return this.$vuetify.theme.themes.light.success;
        case 2:
          return this.$vuetify.theme.themes.light.error;
        default:
          return undefined;
      }
    },
  },
};
</script>