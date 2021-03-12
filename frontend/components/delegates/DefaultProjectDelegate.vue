<template>
  <v-card @click.prevent="details">
    <v-layout column ma-6>
      <DefaultText :size="18" :color="$vuetify.theme.themes.light.quinary">{{
        project.title
      }}</DefaultText>
      <v-layout row ma-0 mt-6>
        <v-layout column shrink>
          <DefaultText :size="14">Project deadline</DefaultText>
          <DefaultText class="mt-3" :size="12">{{ project.end }}</DefaultText>
        </v-layout>
        <v-layout column ml-10>
          <DefaultText :size="14">Total invest amount</DefaultText>
          <DefaultText class="mt-3" :size="12">{{
            project.total || 0
          }}</DefaultText>
        </v-layout>
      </v-layout>
    </v-layout>
  </v-card>
</template>

<script>
export default {
  props: {
    project: {},
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
  methods: {
    details() {
      this.$router.push(`/project/${this.project.id}`);
    },
  },
};
</script>