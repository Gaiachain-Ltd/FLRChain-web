<template>
  <v-card>
    <v-layout fill-height align-center class="mt-1 mx-1 pa-1">
      <v-layout align-center class="mx-1" v-if="fundraising !== -1">
        <StatusIndicator
          class="mr-1"
          :color="$vuetify.theme.themes.light.primary"
        ></StatusIndicator>
        <DefaultText :size="12" :color="$vuetify.theme.themes.light.quinary">{{
          `${fundraising} fundraising`
        }}</DefaultText>
      </v-layout>
      <v-layout align-center class="mx-1" v-if="active !== -1">
        <StatusIndicator
          class="mr-1"
          :color="$vuetify.theme.themes.light.success"
        ></StatusIndicator>
        <DefaultText :size="12" :color="$vuetify.theme.themes.light.quinary">{{
          `${active} active`
        }}</DefaultText>
      </v-layout>
      <v-layout align-center class="mx-1" v-if="closed !== -1">
        <StatusIndicator
          class="mr-1"
          :color="$vuetify.theme.themes.light.error"
        ></StatusIndicator>
        <DefaultText :size="12" :color="$vuetify.theme.themes.light.quinary">{{
          `${closed} closed`
        }}</DefaultText>
      </v-layout>
    </v-layout>
  </v-card>
</template>

<script>
export default {
  props: {
    fundraising: {
      type: Number,
      default: 0,
    },
    active: {
      type: Number,
      default: 0,
    },
    closed: {
      type: Number,
      default: 0,
    },
  },
  components: {
    StatusIndicator: () =>
      import("@/components/widgets/projects/StatusIndicator"),
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>