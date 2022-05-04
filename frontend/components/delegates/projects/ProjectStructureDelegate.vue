<template>
  <v-layout align-center style="width: 100%">
    <DefaultText v-if="index" class="mr-1" :color="color" size="12">{{
      index
    }}</DefaultText>
    <div :class="['decorator mr-2 mb-1', kind]"></div>
    <v-layout>
      <DefaultText size="12" :color="color">{{ internalName }}</DefaultText>
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
    color() {
      switch (this.kind) {
        case "action":
          return "#02595b";
        case "milestone":
          return "#00868a";
        case "task":
          return "#06bcc1";
      }
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
  width: 10px;
  height: 10px;
  min-width: 10px;
  min-height: 10px;
  max-height: 10px;
  max-width: 10px;
  border-radius: 3px;
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