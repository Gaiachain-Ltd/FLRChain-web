<template>
  <v-layout align-center style="width: 100%">
    <DefaultText
      v-if="index"
      class="mr-3"
      :color="$vuetify.theme.themes.light.primary"
      >{{ index }}</DefaultText
    >
    <div :class="['decorator mr-3 mb-1', kind]"></div>
    <v-layout>
      <DefaultText>{{ internalName }}</DefaultText>
    </v-layout>
  </v-layout>
</template>

<script>
export default {
  props: {
    name: {
      type: String,
    },
    index: {
      type: Number | String,
      default: "",
    },
    kind: {
      type: String,
      default: "task",
    },
  },
  computed: {
    internalName() {
      return this.name ? this.name : "Untitled";
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>

<style scoped lang="scss">
.decorator {
  border-color: var(--v-primary-base);
  border-style: solid;
  border-width: 1px;
  width: 12px;
  height: 12px;
  min-width: 12px;
  min-height: 12px;
  max-height: 12px;
  max-width: 12px;
  border-radius: 4px;
  rotate: 45deg;

  &.action {
    background-color: var(--v-primary-base);
  }
}
</style>