<template>
  <v-btn
    v-bind="$attrs"
    v-on="$listeners"
    :class="['text-none elevation-0 my-1 mr-1 default', creator && 'creator']"
  >
    <slot></slot>
  </v-btn>
</template>

<script>
export default {
  props: {
    creator: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

<style scoped>
.default {
  color: var(--v-quaternary-base);
  border-style: solid;
  border-color: var(--v-quaternary-base);
  border-radius: 20px;
  border-width: 1px;
  padding-top: 3px !important;
  background-color: white !important;
}
.creator {
  background-color: #f7f9fb !important;
}
</style>