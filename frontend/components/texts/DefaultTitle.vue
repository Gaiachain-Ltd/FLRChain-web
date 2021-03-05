<template>
  <v-flex shrink>
    <div class="toolbar-title">
      <slot></slot>
    </div>
  </v-flex>
</template>

<style scoped>
.toolbar-title {
  font-size: 28px !important;
  line-height: 40px !important;
  height: 40px;
  color: var(--v-quinary-base);
}
</style>