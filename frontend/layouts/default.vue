<template>
  <v-app class="background-style">
    <v-navigation-drawer app class="background-style">
      <v-layout column align-center>
        <v-flex shrink mt-6>
          <img :src="logo" />
        </v-flex>
        <v-layout shrink column ml-10 mt-6>
          <SideMenuItem
            class="my-3"
            v-for="item in items"
            :key="item.label"
            :item="item"
          ></SideMenuItem>
        </v-layout>
        <v-spacer></v-spacer>
      </v-layout>
    </v-navigation-drawer>
    <v-main>
      <v-container fill-height>
        <Nuxt />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      logo: require("@/assets/side/sidebar_logo.svg"),
    };
  },
  computed: {
    items() {
      let items = [];
      [
        {
          iconOn: require("@/assets/side/home_on.svg"),
          iconOff: require("@/assets/side/home_off.svg"),
          enabled: this.$route.name === "index",
          label: "Home",
          route: "/",
          visible: true,
        },
        {
          iconOn: require("@/assets/side/plus_on.svg"),
          iconOff: require("@/assets/side/plus_off.svg"),
          enabled: this.$route.name === "project-create",
          label: "Create project",
          route: "/project/create",
          visible: true, //this.$auth.user.type === 2, //Facilitator
        },
        {
          iconOn: require("@/assets/side/wallet_on.svg"),
          iconOff: require("@/assets/side/wallet_off.svg"),
          enabled: this.$route.name === "balance",
          label: "Balance",
          route: "/balance",
          visible: true,
        },
      ].forEach((item) => {
        if (item.visible) {
          items.push(item);
          console.log(this.$route.name);
        }
      });
      return items;
    },
  },
  components: {
    SideMenuItem: () => import("@/components/sidemenu/SideMenuItem"),
  },
};
</script>

<style scoped>
.background-style {
  background-color: var(--v-accent-base) !important;
}
</style>