<template>
  <v-layout
    class="pointer-cursor"
    row
    shrink
    ma-0
    pa-0
    align-center
    @click.prevent="logOut"
  >
    <v-layout column ma-0>
      <DefaulText :color="$vuetify.theme.themes.light.quinary">{{
        $auth.user.first_name || "Damian Cholewa"
      }}</DefaulText>
      <div class="account-type-text">{{ accountType }}</div>
    </v-layout>
    <v-flex class="logout-icon-style" shrink ml-4>
      <DefaultSVGIcon
        :icon="require('@/assets/toolbar/logout.svg')"
      ></DefaultSVGIcon>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  data() {
    return {};
  },
  components: {
    DefaulText: () => import("@/components/texts/DefaultText"),
    DefaultSVGIcon: () => import("@/components/icons/DefaultSVGIcon"),
  },
  computed: {
    accountType() {
      switch (this.$auth.user.type) {
        case 1:
          return "FACILITATOR";
        case 2:
          return "INVESTOR";
        default:
          return "FACILITATOR";
      }
    },
  },
  methods: {
    logOut() {
      this.$auth.logout().then(this.$router.push("/login"));
    },
  },
};
</script>

<style scoped>
.account-type-text {
  font-size: 10px !important;
  color: var(--v-quinary-base);
}
.logout-icon-style {
  min-width: 20px !important;
  height: 20px !important;
  width: 20px !important;
  min-height: 20px !important;
}
.pointer-cursor {
  cursor: pointer;
}
</style>