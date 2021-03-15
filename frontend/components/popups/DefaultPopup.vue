<template>
  <v-dialog v-model="dialog" persistent max-width="290">
    <template v-slot:activator="{ on, attrs }">
      <slot v-bind:attrs="attrs" v-bind:on="on"></slot>
    </template>
    <v-card>
      <v-layout column ma-0>
      </v-layout>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: {
    text: {
      type: String,
    },
  },
  data() {
    return {
      dialog: false,
    };
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>