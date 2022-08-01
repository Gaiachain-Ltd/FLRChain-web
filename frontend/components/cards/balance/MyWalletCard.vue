<template>
  <DefaultCard>
    <v-layout column>
      <LabeledText
        label="My wallet address"
        :text="address.address"
        @clicked="() => openExplorerAddressLink(address.address)"
        clickable
      ></LabeledText>
      <v-layout shrink>
        <ActionButton
          class="mt-1"
          color="white"
          :border="`1px ${$vuetify.theme.themes.light.primary} solid !important`"
          :textColor="`${$vuetify.theme.themes.light.primary} !important`"
          @click.prevent="() => openExplorerAddressLink(address.address)"
          >Details</ActionButton
        >
      </v-layout>
    </v-layout>
  </DefaultCard>
</template>

<script>
import AlgoExplorerMixin from "@/mixins/AlgoExplorerMixin";

export default {
  mixins: [AlgoExplorerMixin],
  data() {
    return {
      address: "",
    };
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultCard: () => import("@/components/cards/DefaultCard"),
    LabeledText: () => import("@/components/texts/LabeledText"),
    ActionButton: () => import("@/components/buttons/ActionButton"),
  },
  async fetch() {
    this.$axios
      .get("accounts/balance/")
      .then((reply) => (this.address = reply.data));
  },
};
</script>