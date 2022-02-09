<template>
  <v-layout align-center wrap>
    <div class="decorator mb-1 mr-2" :style="{ backgroundColor: color, borderColor: color }"></div>
    <DefaultText>{{ `${name} (USD ${value}` }}</DefaultText>
    <div class="separator mx-1"></div>
    <DefaultText>{{ `${share}%)` }}</DefaultText>
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
  width: 14px;
  height: 14px;
  min-width: 14px;
  min-height: 14px;
}
.separator {
  width: 2px;
  min-width: 2px;
  height: 18px;
  background-color: #dce0e7;
}
</style>