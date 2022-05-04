<template>
  <DefaultPopup :show.sync="show">
    <v-layout slot="icon">
    </v-layout>
    <v-layout column slot="content" mt-6 mx-6>
      <DefaultText class="mb-3">Credit card details</DefaultText>
      <CreditCardForm
        ref="cardform"
        v-if="page === 0"
        :card.sync="card"
      ></CreditCardForm>
      <BillingDetailsForm
        ref="billingform"
        v-if="page === 1"
        :billingDetails.sync="card.billingDetails"
      ></BillingDetailsForm>
    </v-layout>
        <v-layout slot="buttons" mb-6 mx-6>
      <v-spacer></v-spacer>
      <ActionButton
        class="mr-3"
        color="white"
        :border="`1px ${$vuetify.theme.themes.light.primary} solid !important`"
        :textColor="`${$vuetify.theme.themes.light.primary} !important`"
        @click.prevent="handlePrev"
        >{{ prevButtonText }}</ActionButton
      >
      <ActionButton color="primary" @click.prevent="handleNext" :loading="loading"
        >{{ nextButtonText }}</ActionButton
      >
    </v-layout>
  </DefaultPopup>
</template>

<script>
import { v4 as uuidv4 } from "uuid";
const openpgp = require("openpgp");

export default {
  props: {
    value: {},
  },
  data() {
    return {
      page: 0,
      publicKey: null,
      keyId: null,
      card: {
        amount: "10",
        number: "4007410000000006",
        expiry: "12/2022",
        cvv: "123",
        billingDetails: {
          name: `${this.$auth.user.first_name} ${this.$auth.user.last_name}`,
          address: "st. Test 1/23",
          city: "Test",
          country: "US",
          postalCode: "12-123",
          district: "",
        },
      },
      paymentId: null,
      idempotencyKey: uuidv4(),
      loading: false,
    };
  },
  computed: {
    show: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("update:value", value);
      },
    },
    nextButtonText() {
      if (this.page === 0) {
        return "Confirm";
      } else {
        return "Pay";
      }
    },
    prevButtonText() {
      if (this.page === 0) {
        return "Cancel";
      } else {
        return "Back";
      }
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    ActionButton: () => import("@/components/buttons/ActionButton"),
    DefaultSVGIcon: () => import("@/components/icons/DefaultSVGIcon"),
    DefaultPopup: () => import("@/components/popups/DefaultPopup"),
    CreditCardForm: () => import("@/components/forms/payment/CreditCardForm"),
    BillingDetailsForm: () =>
      import("@/components/forms/payment/BillingDetailsForm"),
    BlockButton: () => import("@/components/buttons/BlockButton"),
  },
  methods: {
    handleNext() {
      if (this.page === 0 && this.$refs.cardform.validate()) {
        this.page += 1;
      } else if (this.page === 1 && this.$refs.billingform.validate()) {
        this.saveCard();
      }
    },
    handlePrev() {
      if (this.page === 0) {
        this.show = false;
      } else {
        this.page -= 1;
      }
    },
    async saveCard() {
      if (this.page === 0) {
        return (this.page += 1);
      }

      this.card.encryptedData = await this.encryptedData();
      delete this.card.number;
      delete this.card.cvv;

      this.loading = true;

      await this.$axios
        .post("payments/circle/card/", {
          idempotencyKey: this.idempotencyKey,
          keyId: this.keyId,
          encryptedData: this.card.encryptedData,
          expiry: this.card.expiry,
          billingDetails: this.card.billingDetails,
        })
        .then((reply) => {
          this.card.cardId = reply.data.data.id;
          this.createPayment();
        })
        .catch(() => {
          this.$emit("error");
          this.show = false;
        });
    },
    async createPayment() {
      await this.$axios
        .post("payments/circle/card/payment/", {
          idempotencyKey: this.idempotencyKey,
          keyId: this.keyId,
          encryptedData: this.card.encryptedData,
          amount: this.card.amount,
          cardId: this.card.cardId,
        })
        .then((reply) => {
          this.paymentId = reply.data.data.id;
          this.$emit("success");
          this.show = false;
        })
        .catch(() => {
          this.$emit("error");
          this.show = false;
        });
    },
    async encryptedData() {
      if (
        !this.publicKey ||
        !this.card.number ||
        !this.card.cvv ||
        this.card.number.length < 15 ||
        this.card.cvv.length < 3
      ) {
        return null;
      }

      const decodedPublicKey = atob(this.publicKey);
      const options = {
        message: openpgp.message.fromText(
          JSON.stringify({
            number: this.card.number,
            cvv: this.card.cvv,
          })
        ),
        publicKeys: (await openpgp.key.readArmored(decodedPublicKey)).keys,
      };

      return await openpgp.encrypt(options).then((ciphertext) => {
        return btoa(ciphertext.data);
      });
    },
  },
  async fetch() {
    await this.$axios
      .get("payments/circle/key/")
      .then((reply) => {
        this.publicKey = reply.data.publicKey;
        this.keyId = reply.data.keyId;
      })
      .catch((error) => {
        console.log("ERROR", error);
      });
  },
};
</script>