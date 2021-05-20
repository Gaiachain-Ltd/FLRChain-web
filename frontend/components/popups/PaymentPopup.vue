<template>
  <DefaultPopup :show.sync="show"> </DefaultPopup>
</template>

<script>
const openpgp = require('openpgp');

export default {
  props: {
    value: {},
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
    DefaultPopup: () => import("@/components/popups/DefaultPopup"),
  },
  mounted() {
    console.log("HELLO", openpgp);
  },
};
</script>