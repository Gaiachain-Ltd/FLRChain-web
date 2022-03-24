<template>
  <DefaultPopup :show.sync="show">
    <v-flex slot="icon"> </v-flex>
    <v-flex slot="content" ma-6>
      <DefaultText :size="22" color="#253F50" family="open-sans">{{
        text
      }}</DefaultText>
    </v-flex>
    <v-layout slot="buttons" mb-6 mx-6>
      <v-spacer></v-spacer>
      <ActionButton
        class="mr-3"
        color="white"
        :border="`1px ${$vuetify.theme.themes.light.primary} solid !important`"
        :textColor="`${$vuetify.theme.themes.light.primary} !important`"
        @click.prevent="ok"
        >Ok</ActionButton
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
        this.$emit("update:value", value);
      },
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    ActionButton: () => import("@/components/buttons/ActionButton"),
    DefaultPopup: () => import("@/components/popups/DefaultPopup"),
  },
  methods: {
    ok() {
      this.show = false;
    },
  },
};
</script>