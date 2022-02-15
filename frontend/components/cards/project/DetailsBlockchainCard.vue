<template>
<DefaultCard>
    <v-layout column>
        <LabeledText class="mb-6" label="Project wallet" text="LINK"></LabeledText>
        <LabeledText label="Smart contract" text="LINK"></LabeledText>
    </v-layout>
</DefaultCard>
</template>

<script>
export default {
  components: {
    DefaultCard: () =>
      import("@/components/cards/DefaultCard"),
    LabeledText: () => import("@/components/texts/LabeledText"),
  },
};
</script>