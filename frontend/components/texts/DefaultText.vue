<template>
  <v-flex
    shrink
    :class="['default-text-style', clickable && 'pointer-cursor']"
    @click.prevent="$emit('clicked')"
    :style="{ color: color || $vuetify.theme.themes.light.quaternary }"
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
    clickable: {
      type: Boolean,
      default: false,
    }
  }
};
</script>

<style scoped>
.default-text-style {
  font-size: 16px !important;
}
.pointer-cursor {
  cursor: pointer;
}
</style>