<template>
  <div
    class="indicator"
    :style="{
      backgroundColor: color,
      width: `${size}px`,
      height: `${size}px`,
      marginBottom: `${marginBottom}px`,
    }"
  ></div>
</template>

<script>
export default {
  props: {
    color: {},
    size: {
      type: Number | String,
      default: 10,
    },
    marginBottom: {
      type: Number | String,
      default: 3
    }
  },
};
</script>

<style scoped>
.indicator {
  border-radius: 2px;
}
</style>