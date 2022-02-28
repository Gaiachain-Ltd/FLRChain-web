<template>
  <v-layout align-center style="width: 100%">
    <DefaultText
      v-if="index"
      class="mr-3"
      :color="kind == 'milestone' ? '#00868A' : '#06BCC1'"
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
  border-style: solid;
  border-width: 2px;
  width: 12px;
  height: 12px;
  min-width: 12px;
  min-height: 12px;
  max-height: 12px;
  max-width: 12px;
  border-radius: 4px;
  rotate: 45deg;
}
.action {
  background-color: #02595b;
  border-color: #02595b;
}
.milestone {
  background-color: white;
  border-color: #00868a;
}
.task {
  background-color: white;
  border-color: #06bcc1;
}
</style>