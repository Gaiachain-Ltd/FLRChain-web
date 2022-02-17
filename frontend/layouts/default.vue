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
          <template v-for="item in items">
            <v-layout column :key="item.label">
              <SideMenuItem class="mt-6" :item="item"></SideMenuItem>
              <v-expand-transition>
                <v-layout column v-if="item.enabled">
                  <SideMenuItem
                    v-for="children in item.childrens"
                    :key="children.label"
                    :item="children"
                    class="mt-2"
                  >
                  </SideMenuItem>
                </v-layout>
              </v-expand-transition>
            </v-layout>
          </template>
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
      <v-container fill-height pa-0>
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
      return [
        {
          iconOn: require("@/assets/side/profile_on.svg"),
          iconOff: require("@/assets/side/profile_off.svg"),
          enabled: this.$route.name === "profile",
          label: this.$route.path,
          route: "/profile",
          visible: true,
        },
        {
          iconOn: require("@/assets/side/projects_on.svg"),
          iconOff: require("@/assets/side/projects_off.svg"),
          enabled:
            this.$route.name === "index" ||
            this.$route.name.includes("project"),
          label: "Projects",
          route: "/",
          visible: true,
          childrens: [
            {
              enabled:
                this.$route.path == "/" ||
                this.$route.path.includes("/project/all"),
              label: "All",
              route: "/",
              fontSize: 13,
              visible: true,
            },
            {
              enabled: this.$route.path.includes("/project/fundraising"),
              label: "Fundraising",
              route: "/project/fundraising",
              fontSize: 13,
              visible: true,
            },
            {
              enabled: this.$route.path.includes("/project/active"),
              label: "Active",
              route: "/project/active",
              fontSize: 13,
              visible: true,
            },
            {
              enabled: this.$route.path.includes("/project/closed"),
              label: "Closed",
              route: "/project/closed",
              fontSize: 13,
              visible: true,
            },
            {
              iconOn: require("@/assets/side/plus_on.svg"),
              iconOff: require("@/assets/side/plus_off.svg"),
              enabled: this.$route.name === "project-create",
              label: "Create project",
              route: "/project/create",
              fontSize: 13,
              iconSize: 12,
              spacing: 1,
              visible: this.isFacililator,
            },
          ].filter((child) => child.visible),
        },
        {
          iconOn: require("@/assets/side/investment_on.svg"),
          iconOff: require("@/assets/side/investment_off.svg"),
          enabled: this.$route.name === "balance",
          label: "Investments",
          route: "/balance",
          visible: true,
        },
      ].filter((item) => item.visible);
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
