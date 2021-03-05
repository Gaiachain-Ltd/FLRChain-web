<template>
  <v-menu
    v-model="showMenu"
    :close-on-content-click="false"
    transition="scale-transition"
    offset-y
    offset-overflow
    bottom
    :nudge-bottom="-30"
    max-width="290px"
    min-width="auto"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-layout column>
        <DefaultText :size="12" :color="$vuetify.theme.themes.light.senary">{{
          label
        }}</DefaultText>
        <v-text-field
          class="text-field-style"
          background-color="#f7f9fb"
          height="50"
          v-model="date"
          v-bind="attrs"
          v-on="on"
          @click.prevent="showMenu = showMenu"
          solo
          flat
          readonly
        >
          <v-layout
            column
            pr-2
            mb-1
            align-center
            slot="prepend-inner"
            @click="showMenu = !showMenu"
          >
            <DefaultSVGIcon
              :icon="require('@/assets/icons/calendar.svg')"
            ></DefaultSVGIcon>
          </v-layout>
        </v-text-field>
      </v-layout>
    </template>
    <v-date-picker
      v-model="date"
      no-title
      color="primary"
      @input="showMenu = false"
    ></v-date-picker>
  </v-menu>
</template>

<script>
export default {
  props: {
    label: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      date: this.$moment().format("YYYY-MM-DD"),
      showMenu: false,
    };
  },
  components: {
    DefaultSVGIcon: () => import("@/components/icons/DefaultSVGIcon"),
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>

<style scoped>
.text-field-style {
  border-radius: 7px !important;
}
</style>