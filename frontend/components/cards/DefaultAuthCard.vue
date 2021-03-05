<template>
  <v-card min-width="500">
    <v-card-title>
      <div class="auth-title">{{ title }}</div>
    </v-card-title>
    <v-card-subtitle>
      <DefaultText class="mt-1">{{ subtitle }}</DefaultText>
    </v-card-subtitle>
    <v-card-text>
      <v-divider></v-divider>
      <slot name="content"></slot>
      <v-divider></v-divider>
    </v-card-text>
    <v-card-actions>
      <v-layout column align-center>
        <slot name="footer"></slot>
      </v-layout>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
    },
    subtitle: {
      type: String,
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>

<style scoped>
.auth-title {
  font-family: "open-sans" !important;
  font-weight: 400 !important;
  font-size: 32px !important;
  line-height: 42px !important;
  color: var(--v-primary-base);
}
</style>