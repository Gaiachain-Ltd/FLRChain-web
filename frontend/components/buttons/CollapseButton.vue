<template>
  <v-btn small icon class="elevation-16 default" @click.prevent="onClicked">
    <v-img max-width="16" :src="icon" contain></v-img>
  </v-btn>
</template>

<script>
export default {
  props: {
    value: {},
  },
  data() {
    return {
      upIcon: require("@/assets/icons/up.svg"),
      downIcon: require("@/assets/icons/down.svg"),
    };
  },
  computed: {
    icon() {
      return this.value ? this.downIcon : this.upIcon;
    },
  },
  methods: {
    onClicked() {
      this.$emit("input", !this.value);
    },
  },
};
</script>

<style scoped>
.default {
  background-color: white;
}
</style>