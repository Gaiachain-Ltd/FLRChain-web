<template>
  <v-btn
    v-bind="$attrs"
    v-on="$listeners"
    class="action-btn-style text-none elevation-0"
    :style="{ border: border, color: textColor }"
    height="41"
    ><slot>{{ label }}</slot></v-btn
  >
</template>

<script>
export default {
  props: {
    label: {
      type: String,
    },
    border: {
      type: String,
      default: "unset",
    },
    textColor: {
      type: String,
      default: "white",
    },
  },
};
</script>

<style scoped>
.action-btn-style {
  border-radius: 7px !important;
  font-family: "open-sans" !important;
  font-size: 12px !important;
  font-weight: 600 !important;
}
</style>
