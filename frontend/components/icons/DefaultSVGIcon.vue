<template>
  <v-flex shrink :style="iconStyle">
    <v-img :src="icon" :style="iconStyle" />
  </v-flex>
</template>

<script>
export default {
  props: {
    icon: {},
    size: {
      type: Number | String,
      default: 20,
    },
  },
  computed: {
    iconStyle() {
      return {
        minWidth: `${this.size}px !important`,
        minHeigth: `${this.size}px !important`,
        width: `${this.size}px !important`,
        height: `${this.size}px !important`,
      };
    },
  },
};
</script>