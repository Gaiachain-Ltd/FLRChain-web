<template>
  <DefaultPopup :show.sync="show">
    <v-flex slot="content" my-6>
      <DefaultText
        class="text-center"
        :size="22"
        color="#253F50"
        family="open-sans"
        >{{ text }}</DefaultText
      >
    </v-flex>
    <v-layout slot="buttons" column ma-0 style="width: 100%">
      <v-flex mb-3>
        <BlockButton color="primary" @clicked="ok">Ok</BlockButton>
      </v-flex>
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
    BlockButton: () => import("@/components/buttons/BlockButton"),
    DefaultPopup: () => import("@/components/popups/DefaultPopup"),
  },
  methods: {
    ok() {
      this.show = false;
    },
  },
};
</script>