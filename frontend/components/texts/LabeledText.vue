<template>
  <v-layout column>
    <v-flex>
      <DefaultText :color="$vuetify.theme.themes.light.primary" bold>{{
        label
      }}</DefaultText>
    </v-flex>
    <v-layout
      row
      shrink
      ma-0
      align-center
      :class="clickable && 'clickable'"
      @click.prevent="$emit('clicked')"
    >
      <v-flex v-if="icon" shrink mb-1 mr-2>
        <DefaultSVGIcon :icon="icon" :size="16"></DefaultSVGIcon>
      </v-flex>
      <v-flex>
        <DefaultText :size="14" bold>{{ text }}</DefaultText>
      </v-flex>
    </v-layout>
  </v-layout>
</template>

<script>
export default {
  props: {
    label: {
      type: String,
    },
    text: {
      type: String | Number,
    },
    icon: {
      type: String,
    },
    clickable: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultSVGIcon: () => import("@/components/icons/DefaultSVGIcon"),
  },
};
</script>

<style scoped>
.clickable {
  cursor: pointer;
}
.clickable:hover {
  opacity: 0.8;
}
</style>