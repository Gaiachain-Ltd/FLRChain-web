<template>
  <DefaultCard :showOverlay="!project.app_id">
    <v-layout column>
      <LabeledText
        class="mb-6"
        label="Project wallet address"
        :text="projectAddress"
        @clicked="() => openExplorerAddressLink(projectAddress)"
        clickable
      ></LabeledText>
      <LabeledText
        label="Smart contract id"
        :text="project.app_id"
        @clicked="() => openExplorerApplicationLink(project.app_id)"
        clickable
      ></LabeledText>
    </v-layout>
  </DefaultCard>
</template>

<script>
import algosdk from "algosdk";
import AlgoExplorerMixin from "@/mixins/AlgoExplorerMixin";

export default {
  mixins: [AlgoExplorerMixin],
  props: {
    project: {},
  },
  computed: {
    projectAddress() {
      if (this.project.app_id) {
        return algosdk.getApplicationAddress(this.project.app_id);
      } else {
        return "";
      }
    },
  },
  components: {
    DefaultCard: () => import("@/components/cards/DefaultCard"),
    LabeledText: () => import("@/components/texts/LabeledText"),
  },
};
</script>