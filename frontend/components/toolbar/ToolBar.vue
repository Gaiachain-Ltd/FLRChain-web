<template>
  <v-layout row shrink ma-0 align-center>
    <DefaultTitle>{{ title }}</DefaultTitle>
    <v-spacer></v-spacer>
    <v-flex shrink>
      <LogoutButton></LogoutButton>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
    },
  },
  components: {
    LogoutButton: () => import("@/components/buttons/LogoutButton"),
    DefaultTitle: () => import("@/components/texts/DefaultTitle"),
  },
};
</script>