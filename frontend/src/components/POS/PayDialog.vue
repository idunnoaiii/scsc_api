<template>
  <v-row justify="center">
    <v-dialog v-model="show" persistent max-width="600px">

      <v-card>
        <v-card-title>
          <span class="text-h5">Payment</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" sm="6" md="6">
                <v-text-field
                  label="Customer"
                  value="Thien"
                  readonly
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="6">
                <v-text-field
                  label="In-charge"
                  value="Clerk"
                  readonly
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="3">
                <div class="subtitle-1 text--grey">Total Price</div>
              </v-col>
              <v-col cols="9">
                <v-text-field
                  placeholder="Placeholder"
                  :value="totalPrice"
                  readonly
                  solo
                ></v-text-field
              ></v-col>
            </v-row>
            <v-row>
              <v-col cols="3">
                <div class="subtitle-1 text--grey">Payment</div>
              </v-col>
              <v-col cols="9">
                <v-text-field
                  v-model="paymentAmount"
                  solo
                  type="number"
                  step="1000"
                  clearable
                ></v-text-field>
                <v-btn
                  :key="n"
                  class="ml-0"
                  v-for="n in [1, 2, 5, 10, 20, 50, 100, 200, 500]"
                  @click="addToMonney(n)"
                  color="green"
                  outlined
                  x-small
                  >{{ n }}k</v-btn
                >
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="3">
                <div class="subtitle-1 text--grey">Change</div>
              </v-col>
              <v-col cols="9">
                <v-text-field
                  placeholder="Placeholder"
                  :value="change"
                  readonly
                  solo
                ></v-text-field
              ></v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="red darken-1"
            small
            class="white--text"
            @click="$emit('close-payment-dialog')"
          >
            Close
          </v-btn>
          <v-btn
            color="green darken-1"
            small
            class="white--text"
            @click="$emit('confirm-payment', { amount: paymentAmount, change: change })"
            :disabled="!canPurchase"
          >
            Confirm Payment
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
export default {
  name: "PayDialog",
  props: {
    show: Boolean,
  },
  data: function () {
    return {
      paymentAmount: 0,
      totalPrice: 123.0,
      enableDialog: false,
    };
  },
  methods: {
    addToMonney(number) {
      this.paymentAmount += number * 1000;
    },
  },
  computed: {
    canPurchase: function () {
      return this.paymentAmount >= this.totalPrice;
    },
    change: function () {
      if (this.paymentAmount < this.totalPrice) return 0;
      return this.paymentAmount - this.totalPrice;
    },
  },

};
</script>


<style scoped>
.min-width-300 {
  min-width: 300px !important;
}
.text-white {
  color: #ffffff !important;
}
</style>