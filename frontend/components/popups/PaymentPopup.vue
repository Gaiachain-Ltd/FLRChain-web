<template>
  <DefaultPopup :show.sync="show">
    <v-layout column slot="content">
      <CreditCardForm :card.sync="card"></CreditCardForm>
    </v-layout>
    <v-layout slot="buttons" column ma-0 style="width: 100%">
      <v-flex mb-3>
        <BlockButton @clicked="saveCard">Pay</BlockButton>
      </v-flex>
      <v-flex>
        <BlockButton color="error" @clicked="show = false">Cancel</BlockButton>
      </v-flex>
    </v-layout>
  </DefaultPopup>
</template>

<script>
import { v4 as uuidv4 } from 'uuid';
const openpgp = require("openpgp");

export default {
  props: {
    value: {},
  },
  data() {
    return {
      publicKey: null,
      keyId: null,
      card: {
        number: "4007410000000006",
        expiry: "12/22",
        phoneNumber: "+48663317345",
        email: "damian.cholewa.choli@gmail.com",
        billingDetails: {
          name: "Damian Cholewa",
          city: "Lublin",
          country: "PL",
          line1: "Text",
          line2: "Text",
          district: "DDD",
          postalCode: "20-303"
        }
      },
      paymentId: null,
      idempotencyKey: uuidv4()
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
  },
  components: {
    DefaultPopup: () => import("@/components/popups/DefaultPopup"),
    CreditCardForm: () => import("@/components/forms/payment/CreditCardForm"),
    BlockButton: () => import("@/components/buttons/BlockButton"),
  },
  methods: {
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
      const data = await this.encryptedCardData();
      await this.$axios.post("payments/circle/card/", data).then(
        (reply) => {
          console.log("SAVE CARD:", reply);
          this.card.cardId = reply.data.data.id;
          this.createPayment();
        }
      )
    },
    async createPayment() {
      const data = await this.encryptedCardData();
      await this.$axios.post("payments/circle/card/payment/", data).then(
        (reply) => {
          console.log("CREATE PAYMENT REPLY:", reply);
          this.paymentId = reply.data.data.id;
          this.$emit('success');
          this.show = false;
        }
      ).catch(
        () => {
          this.$emit('error');
        }
      )
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