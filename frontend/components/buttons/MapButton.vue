<template>
  <v-layout v-if="link" align-center>
    <DefaultSVGIcon
      class="mb-1 mr-2"
      :icon="require('@/assets/icons/map.svg')"
      :size="18"
    ></DefaultSVGIcon>
    <v-flex shrink @click.stop="openLink">
      <a :href="link" target="_blank">Map</a>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  props: {
    link: {
      type: String,
      default: "",
    },
  },
  components: {
    DefaultSVGIcon: () => import("@/components/icons/DefaultSVGIcon"),
  },
  methods: {
    openLink() {
      window.open(this.link, "_blank");
    },
  },
};
</script>