<template>
  <v-row justify="center">
    <v-dialog v-model="$store.state.payDialog" max-width="780px">
      <v-card>
        <v-card-title color="primary white--text">
          <span class="text-h5">Payment</span>
        </v-card-title>
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
            <v-row id="print-me" class="d-none">
              <div class="logo-container">
                <h2 style="text-align: center">SCSC</h2>
              </div>
              <table class="invoice-info-container">
                <tr>
                  <td>
                    Invoice Date: <strong>{{ getNow }}</strong>
                  </td>
                  <td></td>
                </tr>
                <tr>
                  <td>
                    Invoice No: <strong>#{{ currentOrderCode }}</strong>
                  </td>
                  <td></td>
                </tr>
                <tr>
                  <td>
                    Cashier: <strong>{{ $store.state.username }}</strong>
                  </td>
                  <td></td>
                </tr>
              </table>

              <table class="line-items-container">
                <thead>
                  <tr>
                    <th class="heading-quantity">Qty</th>
                    <th class="heading-description">Description</th>
                    <th class="heading-price">Price</th>
                    <th class="heading-subtotal">Subtotal</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in orderItems" v-bind:key="item.name">
                    <td>{{ item.quantity }}</td>
                    <td>{{ item.name }}</td>
                    <td class="right">{{ item.price | currency }}</td>
                    <td class="bold">
                      {{ (item.price * item.quantity) | currency }}
                    </td>
                  </tr>
                  <tr style="border: 1px solid black"></tr>
                  <tr>
                    <td>Term</td>
                    <td></td>
                    <td></td>
                    <td>Value</td>
                  </tr>
                  <tr>
                    <td>Subtotal</td>
                    <td></td>
                    <td></td>
                    <td>{{ totalPrice | currency }}</td>
                  </tr>
                  <tr>
                    <td>Discount</td>
                    <td></td>
                    <td></td>
                    <td>
                      {{ getDiscountValue | currency }}
                    </td>
                  </tr>
                  <tr>
                    <td>Total</td>
                    <td></td>
                    <td></td>
                    <td>
                      <strong>{{ getPriceAfterDiscount | currency }}</strong>
                    </td>
                  </tr>
                  <tr>
                    <td>Cash give</td>
                    <td></td>
                    <td></td>
                    <td>{{ paymentAmount }}</td>
                  </tr>
                  <tr>
                    <td>Charge</td>
                    <td></td>
                    <td></td>
                    <td>{{ change | currency }}</td>
                  </tr>
                </tbody>
              </table>

              <!-- <table class="line-items-container has-bottom-border">
                <thead>
                  <tr>
                    <th>Term</th>
                    <th></th>
                    <th>Value</th>
                  </tr>
                </thead>
                <tbody></tbody>
              </table> -->

              <div class="footer">
                <div class="footer-thanks">
                  <!-- <img
                    src="https://github.com/anvilco/html-pdf-invoice-template/raw/main/img/heart.png"
                    alt="heart"
                  /> -->
                  <span>Thank you!</span>
                </div>
              </div>
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
            :disabled="!canPurchase"
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
import { mapGetters, mapActions, mapState } from "vuex";
import moment from "moment";

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
      this.$htmlToPaper("print-me", {
        autoClose: true,
      });
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

    ...mapState("POS", {
      orderItems: "orderItems",
      currentOrderCode: "currentOrderCode",
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
    getNow() {
      return moment(Date.now()).format("MMMM Do YYYY, h:mm:ss a");
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