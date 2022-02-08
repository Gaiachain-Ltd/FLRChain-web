<template>
  <v-layout column shrink align-end>
    <v-layout style="width: 100%" mb-3>
      <DefaultText :size="12" :color="$vuetify.theme.themes.light.senary"
        >Project image</DefaultText
      >
    </v-layout>
    <v-img
      :src="require('@/assets/images/placeholder.png')"
      contain
    ></v-img>
    <v-layout shrink mt-3>
      <ActionButton color="primary">Upload file</ActionButton>
    </v-layout>
  </v-layout>
</template>

<script>
export default {
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    ActionButton: () => import("@/components/buttons/ActionButton"),
  },
};
</script>