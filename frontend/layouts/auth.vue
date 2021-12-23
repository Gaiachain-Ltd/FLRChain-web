<template>
  <v-app class="background-style">
    <v-main>
      <v-container fluid fill-height>
        <v-layout column align-center>
          <v-flex shrink mt-10>
            <img :src="logo" width="180px" />
          </v-flex>
          <v-layout class="main-component-style" mt-10 column align-center>
            <Nuxt />
          </v-layout>
        </v-layout>
      </v-container>
    </v-main>
  </v-app>
</template>
<script>
export default {
  data() {
    return {
      logo: require("@/assets/logo.svg"),
    };
  },
};
</script>

<style scoped>
.background-style {
  background-color: var(--v-accent-base) !important;
}
.main-component-style {
  z-index: 1;
}
</style>