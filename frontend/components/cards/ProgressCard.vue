<template>
  <v-layout column shrink>
    <v-layout align-center class="mb-1">
      <v-layout shrink>
        <DefaultText :color="$vuetify.theme.themes.light.primary">{{
          min.label
        }}</DefaultText>
        <DefaultText class="ml-2" bold>{{ min.value }}</DefaultText>
        <DefaultText class="ml-1">USDC</DefaultText>
        <DefaultText class="ml-1">{{ `(${min.share}%)` }}</DefaultText>
      </v-layout>
      <v-spacer></v-spacer>
      <v-layout shrink>
        <DefaultText :color="$vuetify.theme.themes.light.primary">{{
          max.label
        }}</DefaultText>
        <DefaultText class="ml-2" bold>{{ max.value }}</DefaultText>
        <DefaultText class="ml-1">USDC</DefaultText>
        <DefaultText class="ml-1">{{ `(${max.share}%)` }}</DefaultText>
      </v-layout>
    </v-layout>
    <DefaultCard>
      <v-progress-linear
        :height="10"
        v-model="min.share"
        rounded
      ></v-progress-linear>
    </DefaultCard>
  </v-layout>
</template>

<script>
export default {
  props: {
    min: {},
    max: {},
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultCard: () => import("@/components/cards/DefaultCard"),
  },
};
</script>