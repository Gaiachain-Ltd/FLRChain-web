<template>
  <v-btn
    v-bind="$attrs"
    v-on="$listeners"
    :class="[
      'text-none elevation-0 my-1 mr-1 default',
      creator && 'creator',
      highlight && 'highlight',
    ]"
  >
    <v-layout align-center>
      <slot></slot>
      <DefaultSVGIcon
        v-if="!creator"
        :icon="require('@/assets/icons/delete.svg')"
        size="15"
        class="mb-1 ml-2"
      ></DefaultSVGIcon>
    </v-layout>
  </v-btn>
</template>

<script>
export default {
  props: {
    creator: {
      type: Boolean,
      default: false,
    },
    highlight: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    DefaultSVGIcon: () => import("@/components/icons/DefaultSVGIcon"),
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
.highlight {
  color: white !important;
  background-color: var(--v-primary-base) !important;
  border-color: var(--v-primary-base) !important;
}
button.v-btn[disabled] {
  opacity: 0.3;
}
</style>