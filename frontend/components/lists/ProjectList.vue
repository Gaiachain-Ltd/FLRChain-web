<template>
  <v-layout column fill-height>
    <v-layout column fill-height>
      <DefaultText :size="24" :color="color">{{ title }}</DefaultText>
      <v-layout column mt-6 class="list-style">
        <DefaultProjectDelegate
          class="mb-6 ml-1 mr-3"
          v-for="delegate in delegates"
          :key="delegate.id"
          :project="delegate"
        ></DefaultProjectDelegate>
        <v-flex>
          <div class="placeholder"></div>
        </v-flex>
      </v-layout>
    </v-layout>
  </v-layout>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
    },
    color: {
      type: String,
    },
  },
  data() {
    return {
      delegates: [
        {
          id: 1,
          name: "Loerem1",
          start: "2021-03-27",
          end: "2021-04-27",
          total: "2000",
        },
        {
          id: 2,
          name: "LOREM!",
          start: "2021-03-27",
          end: "2021-04-27",
          total: "2000",
        },
        {
          id: 3,
          name: "LOREM!",
          start: "2021-03-27",
          end: "2021-04-27",
          total: "2000",
        },
        {
          id: 4,
          name: "LOREM!",
          start: "2021-03-27",
          end: "2021-04-27",
          total: "2000",
        },
        {
          id: 5,
          name: "LOREM!",
          start: "2021-03-27",
          end: "2021-04-27",
          total: "2000",
        },
        {
          id: 6,
          name: "LOREM!",
          start: "2021-03-27",
          end: "2021-04-27",
          total: "2000",
        },
        {
          id: 7,
          name: "LOREM!",
          start: "2021-03-27",
          end: "2021-04-27",
          total: "2000",
        },
      ],
    };
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultProjectDelegate: () =>
      import("@/components/delegates/DefaultProjectDelegate"),
  },
};
</script>

<style scoped>
.list-style {
  max-height: calc(100% - 138px) !important;
  overflow: auto;
}
.placeholder {
  width: 100%;
  height: 12px;
}
</style>