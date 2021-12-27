<template>
  <v-app class="background-style">
    <v-navigation-drawer
      app
      class="background-style elevation-16"
      v-model="drawerState"
      left
      fixed
    >
      <v-layout column align-center fill-height>
        <v-flex shrink mt-6>
          <img :src="logo" width="135px" />
        </v-flex>
        <v-layout shrink column mt-6>
          <SideMenuItem
            class="my-3"
            v-for="item in items"
            :key="item.label"
            :item="item"
          ></SideMenuItem>
        </v-layout>
        <v-spacer></v-spacer>
        <v-flex shrink class="mb-6">
          <client-only>
            <AccountWidget></AccountWidget>
          </client-only>
        </v-flex>
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
import { mapGetters, mapActions } from "vuex";

export default {
  data() {
    return {
      logo: require("@/assets/logo.svg"),
    };
  },
  computed: {
    ...mapGetters(["isFacililator", "getDrawerState"]),
    items() {
      let items = [];
      [ 
        {
          iconOn: require("@/assets/side/profile_on.svg"),
          iconOff: require("@/assets/side/profile_off.svg"),
          enabled: this.$route.name === "profile",
          label: "Profile",
          route: "/profile",
          visible: true,
        },
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
          visible: this.isFacililator,
        },
        {
          iconOn: require("@/assets/side/wallet_on.svg"),
          iconOff: require("@/assets/side/wallet_off.svg"),
          enabled: this.$route.name === "balance",
          label: "Investments",
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
    drawerState: {
      get() {
        return this.getDrawerState;
      },
      set(value) {
        console.log(value, this.getDrawerState);
        this.updateDrawerState(value);
      },
    },
  },
  methods: {
    ...mapActions(["updateDrawerState"]),
  },
  components: {
    SideMenuItem: () => import("@/components/sidemenu/SideMenuItem"),
    AccountWidget: () => import("@/components/widgets/AccountWidget"),
  },
};
</script>

<style scoped>
.background-style {
  background-color: var(--v-accent-base) !important;
}
</style>
