<template>
  <v-card>
    <v-layout ma-0 pa-6 justify-center>
      <slot>
        <v-spacer></v-spacer>
        <ActionButton
          v-if="!hideCancel"
          class="mr-3"
          label="Cancel"
          color="white"
          :border="`1px ${$vuetify.theme.themes.light.primary} solid !important`"
          :textColor="`${$vuetify.theme.themes.light.primary} !important`"
          :disabled="loading"
          @click.prevent="$emit('cancel')"
        ></ActionButton>
        <ActionButton
          :disabled="disabled"
          color="primary"
          label="Save changes"
          :loading="loading"
          @click.prevent="$emit('save')"
        ></ActionButton>
      </slot>
    </v-layout>
  </v-card>
</template>

<script>
export default {
  props: {
    disabled: {
      type: Boolean,
      default: false,
    },
    loading: {
      type: Boolean,
      default: false
    },
    hideCancel: {
      type: Boolean,
      default: false
    }
  },
  components: {
    ActionButton: () => import("@/components/buttons/ActionButton"),
  },
};
</script>
