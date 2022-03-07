<template>
  <DefaultCard :showOverlay="!project.app_id">
    <v-layout column>
      <LabeledText
        label="Project wallet address"
        :text="projectAddress"
        @clicked="() => openExplorerAddressLink(projectAddress)"
        clickable
      ></LabeledText>
      <v-layout shrink class="mb-4">
        <ActionButton
          class="mt-1"
          color="white"
          :border="`1px ${$vuetify.theme.themes.light.primary} solid !important`"
          :textColor="`${$vuetify.theme.themes.light.primary} !important`"
          @click.prevent="() => openExplorerAddressLink(projectAddress)"
          >Details</ActionButton
        >
      </v-layout>
      <LabeledText
        label="Smart contract id"
        :text="project.app_id"
        @clicked="() => openExplorerApplicationLink(project.app_id)"
        clickable
      ></LabeledText>
      <v-layout shrink>
        <ActionButton
          class="mt-1"
          color="white"
          :border="`1px ${$vuetify.theme.themes.light.primary} solid !important`"
          :textColor="`${$vuetify.theme.themes.light.primary} !important`"
          @click.prevent="() => openExplorerApplicationLink(project.app_id)"
          >Details</ActionButton
        >
      </v-layout>
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
    ActionButton: () => import("@/components/buttons/ActionButton"),
  },
};
</script>