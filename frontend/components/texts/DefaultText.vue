<template>
  <v-flex
    shrink
    :class="[clickable && 'pointer-cursor']"
    @click.prevent="$emit('clicked')"
    :style="{
      color: color || $vuetify.theme.themes.light.quaternary,
      fontSize: `${size}px !important`,
    }"
  >
    <slot></slot>
  </v-flex>
</template>

<script>
export default {
  props: {
    color: {
      type: String,
      default: "",
    },
    size: {
      type: Number,
      default: 16,
    },
    clickable: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

<style scoped>
.pointer-cursor {
  cursor: pointer;
}
</style>