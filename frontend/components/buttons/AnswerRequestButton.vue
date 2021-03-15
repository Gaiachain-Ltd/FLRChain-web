<template>
  <DefaultPopup>
    <template v-slot="{ on, attrs }">
      <v-btn
        v-bind="attrs"
        v-on="on"
        class="answer-btn-style elevation-0 round text-none white--text"
        height="20"
        color="septenary"
        >Answer request</v-btn
      >
    </template>
  </DefaultPopup>
</template>

<script>
export default {
  components: {
    DefaultPopup: () => import("@/components/popups/DefaultPopup")
  },
};
</script>

<style scoped>
.answer-btn-style {
  border-radius: 7px !important;
  font-family: "open-sans" !important;
  font-size: 14px !important;
  font-weight: 600 !important;
  letter-spacing: -0.24px !important;
}
</style>