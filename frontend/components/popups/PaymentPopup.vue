<template>
  <DefaultPopup :show.sync="show">
    <v-layout column slot="content">
      <CreditCardForm ref="cardform" v-if="page === 0" :card.sync="card"></CreditCardForm>
      <BillingDetailsForm
        ref="billingform"
        v-if="page === 1"
        :billingDetails.sync="card.billingDetails"
      ></BillingDetailsForm>
    </v-layout>
    <v-layout slot="buttons" column ma-0 style="width: 100%">
      <v-flex mb-3>
        <BlockButton @clicked="handleNext">{{ nextButtonText }}</BlockButton>
      </v-flex>
      <v-flex>
        <BlockButton color="error" @clicked="handlePrev">{{
          prevButtonText
        }}</BlockButton>
      </v-flex>
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
        number: "4007410000000006",
        expiry: "12/2022",
        billingDetails: {
          name: `${this.$auth.user.first_name} ${this.$auth.user.last_name}`,
          city: "Lublin",
          country: "PL",
          line1: "Text",
          postalCode: "20-303",
          email: this.$auth.user.email,
        },
      },
      paymentId: null,
      idempotencyKey: uuidv4(),
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
    async encryptedCardData() {
      let copiedCard = { ...this.card };
      const decodedPublicKey = atob(this.publicKey);
      const options = {
        message: openpgp.message.fromText(
          JSON.stringify({
            number: copiedCard.number,
            cvv: copiedCard.cvv,
          })
        ),
        publicKeys: (await openpgp.key.readArmored(decodedPublicKey)).keys,
      };
      // delete copiedCard.number;
      // delete copiedCard.cvv;
      return await openpgp.encrypt(options).then((ciphertext) => {
        return {
          ...copiedCard,
          idempotencyKey: this.idempotencyKey,
          encryptedData: btoa(ciphertext.data),
          keyId: this.keyId,
        };
      });
    },
    async saveCard() {
      if (this.page === 0) {
        return (this.page += 1);
      }
      const data = await this.encryptedCardData();
      await this.$axios.post("payments/circle/card/", data).then((reply) => {
        console.log("SAVE CARD:", reply);
        this.card.cardId = reply.data.data.id;
        this.createPayment();
      });
    },
    async createPayment() {
      const data = await this.encryptedCardData();
      await this.$axios
        .post("payments/circle/card/payment/", data)
        .then((reply) => {
          console.log("CREATE PAYMENT REPLY:", reply);
          this.paymentId = reply.data.data.id;
          this.$emit("success");
          this.show = false;
        })
        .catch(() => {
          this.$emit("error");
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