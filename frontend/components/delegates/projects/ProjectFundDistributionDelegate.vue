<template>
  <v-layout align-center wrap>
    <div class="decorator mb-1 mr-2" :style="{ backgroundColor: color, borderColor: color }"></div>
    <DefaultText size="10">{{ `${name} (USD ${value}` }}</DefaultText>
    <div class="separator mx-1"></div>
    <DefaultText size="10">{{ `${share}%)` }}</DefaultText>
  </v-layout>
</template>

<script>
export default {
  props: {
    name: {
      type: String,
    },
    value: {
      type: Number | String,
      default: "0.00"
    },
    share: {
      type: Number | String,
      default: 0
    },
    color: {
      type: String,
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>

<style scoped>
.decorator {
  border-width: 1px;
  border-style: solid;
  border-radius: 4px;
  width: 12px;
  height: 12px;
  min-width: 12px;
  min-height: 12px;
}
.separator {
  width: 2px;
  min-width: 2px;
  height: 14px;
  background-color: #dce0e7;
}
</style>