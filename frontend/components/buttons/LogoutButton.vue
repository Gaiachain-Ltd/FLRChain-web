<template>
  <DefaultPopup :show.sync="showLogoutPopup">
    <template v-slot="{ on, attrs }">
      <v-layout
        class="pointer-cursor"
        row
        shrink
        ma-0
        pa-0
        align-center
        v-on="on"
      >
        <v-layout column ma-0>
          <DefaultText :color="$vuetify.theme.themes.light.quinary">{{
            `${$auth.user.first_name} ${$auth.user.last_name}`
          }}</DefaultText>
          <v-layout shrink>
            <div
              class="account-type-text"
              :style="{ backgroundColor: accountTypeColor }"
            >
              {{ accountType }}
            </div>
          </v-layout>
        </v-layout>
        <v-flex class="logout-icon-style" shrink ml-4>
          <DefaultSVGIcon
            :icon="require('@/assets/toolbar/logout.svg')"
          ></DefaultSVGIcon>
        </v-flex>
      </v-layout>
    </template>
    <v-flex slot="icon">
      <DefaultSVGIcon
        :icon="require('@/assets/popup/logout.svg')"
        :size="70"
      ></DefaultSVGIcon>
    </v-flex>
    <v-flex slot="content" my-6>
      <DefaultText
        class="text-center"
        :size="22"
        color="#253F50"
        family="open-sans"
        >Are you sure you want to log out?</DefaultText
      >
    </v-flex>
    <v-layout slot="buttons" column ma-0 style="width: 100%">
      <v-flex mb-3>
        <BlockButton color="error" @clicked="logOut">Log out</BlockButton>
      </v-flex>
      <v-flex>
        <BlockButton class="cancel-style" color="white" @clicked="cancel"
          >Cancel</BlockButton
        >
      </v-flex>
    </v-layout>
  </DefaultPopup>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      showLogoutPopup: false,
    };
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultSVGIcon: () => import("@/components/icons/DefaultSVGIcon"),
    DefaultPopup: () => import("@/components/popups/DefaultPopup"),
    BlockButton: () => import("@/components/buttons/BlockButton"),
  },
  computed: {
    ...mapGetters(["isFacililator"]),
    accountType() {
      return this.isFacililator ? "FACILILATOR" : "INVESTOR";
    },
    accountTypeColor() {
      return this.isFacililator ? "#0075DC" : "#00B854";
    },
  },
  methods: {
    logOut() {
      this.showLogoutPopup = false;
      this.$auth.logout().then(this.$router.push("/login"));
    },
    cancel() {
      this.showLogoutPopup = false;
    },
  },
};
</script>

<style scoped>
.account-type-text {
  font-size: 9px !important;
  color: white;
  border-radius: 15px;
  padding-top: 2px;
  padding-bottom: 0px;
  padding-left: 6px;
  padding-right: 6px;
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
.cancel-style {
  border: 1px black solid !important;
}
</style>