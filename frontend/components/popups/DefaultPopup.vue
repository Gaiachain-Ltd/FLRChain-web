<template>
  <v-dialog v-model="dialog" max-width="400">
    <template v-slot:activator="{ on, attrs }">
      <slot v-bind:attrs="attrs" v-bind:on="on"></slot>
    </template>
    <v-card ma-0>
      <v-layout column ma-0 pa-6 align-center>
        <slot name="icon">
          <v-flex>
            <DefaultSVGIcon
              :icon="require('@/assets/popup/question.svg')"
              :size="70"
            ></DefaultSVGIcon>
          </v-flex>
        </slot>
        <slot name="content"></slot>
        <slot name="buttons"></slot>
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
    DefaultSVGIcon: () => import("@/components/icons/DefaultSVGIcon"),
  },
};
</script>