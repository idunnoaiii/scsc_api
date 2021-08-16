<template>
  <v-row justify="center">
    <v-dialog v-model="$store.state.payDialog"  max-width="780px">
      <v-card>
        <v-toolbar>
          <v-card-title>
            <span class="text-h5">Payment</span>
          </v-card-title>
        </v-toolbar>
        <v-card-text>
          <v-container mt-4>
            <v-row>
              <v-col cols="12" sm="6" md="6">
                <v-text-field
                  label="Cashier"
                  :value="$store.state.username"
                  dense
                  outlined
                  readonly
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="6">
                <v-text-field
                  label="Customer"
                  :value="getCustomerCheckout.text"
                  dense
                  outlined
                  readonly
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="3">
                <div class="subtitle-1 text--grey">Subtotal</div>
              </v-col>
              <v-col cols="3">
                <v-text-field
                  placeholder="Placeholder"
                  :value="totalPrice | currency"
                  readonly
                  solo
                ></v-text-field
              ></v-col>
              <v-col cols="3" v-if="discount.value != 0">
                <div class="subtitle-1 text--grey">Discount:</div>
                <div class="caption text--grey">
                  {{ discount.type == 0 ? "Percentage(%)" : "Cash"
                  }}{{ ":" + discount.value }}
                </div>
              </v-col>
              <v-col cols="3" v-if="discount.value != 0">
                <v-text-field
                  :value="getDiscountValue | currency"
                  readonly
                  solo
                ></v-text-field
              ></v-col>
            </v-row>
            <v-row>
              <v-col cols="3">
                <div class="subtitle-1 text--grey">Total Pay</div>
              </v-col>
              <v-col cols="9">
                <v-text-field
                  placeholder="Placeholder"
                  :value="getPriceAfterDiscount | currency"
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
                  class="mx-1"
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
                  :value="change | currency"
                  readonly
                  solo
                ></v-text-field
              ></v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-divider class="mb-4"></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="green darken-1"
            class="white--text"
            text
            @click="printInvoice()"
          >
            Print
          </v-btn>
          <v-btn
            color="primary darken-1"
            class="white--text"
            text
            @click="$store.commit('SET_PAYDIALOG', false)"
          >
            Cancel
          </v-btn>
          <v-btn
            color="green darken-1"
            class="white--text"
            @click="
              $emit('confirm-payment', {
                amount: paymentAmount,
                change: change,
                discountValue: getDiscountValue,
              })
            "
            :disabled="!canPurchase"
          >
            Confirm
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <iframe
      id="iframe-print"
      src="/PrintInvoice"
      frameborder="0"
      width="100px"
      height="100px"
    >
    </iframe>
  </v-row>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "PayDialog",
  props: {
    show: Boolean,
  },
  data: function () {
    return {
      paymentAmount: 0,
      enableDialog: false,
      customerValue: { text: "Walk in customer", value: -1 },
    };
  },
  methods: {
    addToMonney(number) {
      this.paymentAmount = Number(this.paymentAmount) + number * 1000;
    },
    ...mapActions("POS", {
      calculateDiscount: "calculateDiscount",
    }),
    printInvoice() {
      // var doc = document.getElementById('iframe-print').contentWindow.document;
      // doc.open();
      // doc.write('Test');
      // doc.close();

      var iframe = document.getElementById("iframe-print");
      iframe.focus();
      iframe.contentWindow.print();
    },
  },
  computed: {
    canPurchase: function () {
      return this.paymentAmount >= this.getPriceAfterDiscount;
    },
    change: function () {
      if (this.paymentAmount < this.totalPrice) return 0;
      return this.paymentAmount - this.getPriceAfterDiscount;
    },
    ...mapGetters("POS", {
      totalPrice: "totalPrice",
      discount: "discount",
      getCustomerCheckout: "getCustomerCheckout",
    }),

    getPriceAfterDiscount: function () {
      return this.totalPrice - this.getDiscountValue;
    },

    getDiscountValue: function () {
      if (this.discount.type == 0) {
        return (
          Math.round((this.totalPrice * this.discount.value) / 100000) * 1000
        );
      }
      return this.discount.value;
    },
  },
  created() {
    this.calculateDiscount();
  },

  filters: {
    currency(value) {
      return value.toLocaleString();
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