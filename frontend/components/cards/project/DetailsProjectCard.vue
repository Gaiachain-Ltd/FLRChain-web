<template>
  <v-card mb-0>
    <v-layout column ma-0 pa-6>
      <v-flex mb-6>
        <LabeledText label="Project time" :text="project.start"></LabeledText>
      </v-flex>
      <v-flex mb-6>
        <LabeledText label="Project status" :text="project.start"></LabeledText>
      </v-flex>
      <v-flex mb-6>
        <LabeledText label="Facilitator" :text="project.start"></LabeledText>
      </v-flex>
      <v-flex>
        <LabeledText
          label="Description"
          :text="project.description"
        ></LabeledText>
      </v-flex>
    </v-layout>
  </v-card>
</template>

<script>
export default {
  props: {
    project: {},
  },
  components: {
    LabeledText: () => import("@/components/texts/LabeledText"),
  },
};
</script>