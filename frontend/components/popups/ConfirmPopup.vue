<template>
  <DefaultPopup :show.sync="show">
    <v-flex slot="icon"></v-flex>
    <v-flex slot="content" ma-6>
      <DefaultText>{{ text }}</DefaultText>
    </v-flex>
    <v-layout slot="buttons" mb-6 mx-6>
      <v-spacer></v-spacer>
      <ActionButton
        class="mr-3"
        color="white"
        :border="`1px ${$vuetify.theme.themes.light.primary} solid !important`"
        :textColor="`${$vuetify.theme.themes.light.primary} !important`"
        @click.prevent="show = false"
        >Cancel</ActionButton
      >
      <ActionButton color="primary" @click.prevent="handleConfirm"
        >Confirm</ActionButton
      >
    </v-layout>
  </DefaultPopup>
</template>

<script>
export default {
  props: {
    value: {
      type: Boolean,
    },
    text: {
      type: String,
      default: "",
    },
  },
  computed: {
    show: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("input", value);
      },
    },
  },
  components: {
    ActionButton: () => import("@/components/buttons/ActionButton"),
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultPopup: () => import("@/components/popups/DefaultPopup"),
  },
  methods: {
    handleConfirm() {
      this.$emit("confirm");
      this.show = false;
    },
  },
};
</script>