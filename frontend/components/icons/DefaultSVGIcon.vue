<template>
  <v-flex class="icon-style" shrink>
    <img :src="icon" class="icon-style" />
  </v-flex>
</template>

<script>
export default {
  props: {
    icon: {},
  },
};
</script>

<style scoped>
.icon-style {
  min-width: 20px !important;
  min-height: 20px !important;
  height: 20px !important;
  width: 20px !important;
}
</style>