<template>
  <v-layout>
    <v-col cols="8" md="8">
      <v-card outlined height="100%">
        <v-container class="mt-5" flat>
          <v-row>
            <span class="text-h4 ml-3"> Sales Report </span>
            <v-spacer></v-spacer>
            <v-md-date-range-picker
              opens="right"
              class="my-2"
              @change="pickDateRange"
            >
            </v-md-date-range-picker>
          </v-row>
        </v-container>

        <v-container fluid width="100%" class="mt-5">
          <v-row class="justify-center">
            <v-col cols="12" sm="3">
              <v-hover v-slot="{ hover }" open-delay="200">
                <v-card color="cyan darken-1" :elevation="hover ? 16 : 2">
                  <v-row>
                    <v-col cols="12" sm="8">
                      <v-list-item three-line>
                        <v-list-item-content>
                          <v-list-item-title class="text-h5 md-1 white--text">
                            ${{ revenue | currency }}
                          </v-list-item-title>
                          <v-list-item-subtitle class="white--text">
                            Revenue
                          </v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                    </v-col>
                    <v-col cols="12" sm="4">
                      <div
                        size="100"
                        class="text-h1 text-center white--text ml-n15"
                      >
                        <v-icon color="cyan lighten-5" size="100"
                          >mdi-currency-cny</v-icon
                        >
                      </div>
                    </v-col>
                  </v-row>
                </v-card>
              </v-hover>
            </v-col>
            <v-col cols="12" sm="3">
              <v-hover v-slot="{ hover }" open-delay="200">
                <v-card color="pink darken-1" :elevation="hover ? 16 : 2">
                  <v-row>
                    <v-col cols="12" sm="8">
                      <v-list-item three-line>
                        <v-list-item-content>
                          <v-list-item-title class="text-h4 mb-1 white--text">
                            {{ orders.length }}
                          </v-list-item-title>
                          <v-list-item-subtitle class="white--text">
                            Orders
                          </v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                    </v-col>
                    <v-col cols="12" sm="4">
                      <div
                        size="100"
                        class="text-h1 text-center white--text ml-n15"
                      >
                        <v-icon color="pink lighten-5" size="100"
                          >mdi-receipt</v-icon
                        >
                      </div>
                    </v-col>
                  </v-row>
                </v-card>
              </v-hover>
            </v-col>
            <v-col cols="12" sm="3">
              <v-hover v-slot="{ hover }" open-delay="200">
                <v-card color="orange darken-1" :elevation="hover ? 16 : 2">
                  <v-row>
                    <v-col cols="12" sm="8">
                      <v-list-item three-line>
                        <v-list-item-content>
                          <v-list-item-title class="text-h4 mb-1 white--text">
                            {{ totalItemSold }}
                          </v-list-item-title>
                          <v-list-item-subtitle class="white--text">
                            Item sold
                          </v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                    </v-col>
                    <v-col cols="12" sm="4">
                      <div
                        size="100"
                        class="text-h1 text-center white--text ml-n15"
                      >
                        <v-icon color="orange lighten-3" size="100"
                          >mdi-chart-line</v-icon
                        >
                      </div>
                    </v-col>
                  </v-row>
                </v-card>
              </v-hover>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12">
              <v-sheet elevation="2">
                <v-card-title>
                  Orders
                  <v-spacer></v-spacer>
                  <v-text-field
                    v-model="search"
                    append-icon="mdi-magnify"
                    label="Search"
                    single-line
                    hide-details
                  ></v-text-field>
                </v-card-title>
                <v-data-table
                  :headers="orderHeaders"
                  :items="orders"
                  :search="search"
                  @click:row="handleClick"
                >
                  <template v-slot:[`item.created_date`]="{ item }">
                    <span>{{ item.created_date | toMoment }}</span>
                  </template>
                  <template v-slot:[`item.paid`]="{ item }">
                    <span>{{ item.paid | currency }}</span>
                  </template>
                </v-data-table>
              </v-sheet>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </v-col>
    <v-col cols="4" md="4">
      <v-card outlined height="100%">
        <v-container  flat>
          <v-card>
            <v-container flat>
              <v-row>
                <span class="ma-3 text-h5"> Order Detail </span>
              </v-row>
              <v-row>
                <v-col cols="6">
                  <v-text-field
                    label="Customer"
                    readonly
                    dense
                    hide-details
                    :value="cashier"
                  >
                  </v-text-field>
                </v-col>
                <v-col cols="6">
                  <v-text-field
                    label="Date"
                    readonly
                    dense
                    hide-details
                    :value="date | toMoment"
                  >
                  </v-text-field>
                </v-col>
                <v-col cols="4">
                  <v-text-field
                    label="Subtotal"
                    readonly
                    outlined
                    dense
                    hide-details
                    :value="subtotal | currency"
                  >
                  </v-text-field>
                </v-col>
                <v-col cols="4">
                  <v-text-field
                    label="Discount"
                    readonly
                    outlined
                    dense
                    hide-details
                    :value="discount | currency"
                  >
                  </v-text-field>
                </v-col>
                <v-col cols="4">
                  <v-text-field
                    label="Total"
                    outlined
                    dense
                    hide-details
                    color="green"
                    :value="subtotal | currency"
                    background-color="green lighten-5"
                  >
                  </v-text-field>
                </v-col>
              </v-row>
            </v-container>
          </v-card>
        </v-container>
        <v-container>
          <v-list-item three-line>
            <v-list-item-content>
              <v-sheet elevation="2">
                <v-data-table :headers="orderItemHeaders" :items="orderItems">
                  <template v-slot:[`item.created_date`]="{ item }">
                    <span>{{ item.created_date | toMoment }}</span>
                  </template>
                   <template v-slot:[`item.total`]="{ item }">
                    <span>{{ (item.price * item.quantity) | currency }}</span>
                  </template>
                </v-data-table>
              </v-sheet>
            </v-list-item-content>
          </v-list-item>
        </v-container>
      </v-card>
    </v-col>
  </v-layout>
</template>


<script>
import axios from "../../axios";
import moment from "moment";

export default {
  data() {
    return {
      dateRange: [],
      search: "",
      cashier: "",
      date: "",
      subtotal: "",
      total: "",
      paid: "",
      change: "",
      discount: "",
      orderHeaders: [
        {
          text: "Code",
          align: "start",
          sortable: true,
          value: "code",
        },
        { text: "Date", value: "created_date" },
        { text: "Total", value: "total" },
        { text: "Discount", value: "discount" },
        { text: "Customer", value: "user.username" },
      ],
      orderItemHeaders: [
        { text: "Name", value: "item_name" },
        { text: "Quantity", value: "quantity" },
        { text: "Price", value: "price" },
        { text: "Total", value: "total" },
      ],
      orders: [
        {
          customer_id: null,
          code: 0,
          user_id: 1,
          status: true,
          tax: 0,
          subtotal: 165000,
          paid: 500000,
          change: 499877,
          order_items: [],
        },
      ],
      orderItems: [],
    };
  },
  created() {
    this.init();
    console.log(
      moment("2021-06-27T03:32:14.693000").format("MMMM Do YYYY, h:mm:ss a")
    );
  },
  methods: {
    init: function () {
      this.pickDateRange([moment().startOf("day"), moment()]);
    },
    handleClick(row) {
      this.orderItems = row.order_items;
      this.cashier = row.user.username;
      this.date = row.created_date;
      this.total = row.subtotal;
      this.discount = row.discount;
      this.subtotal = row.total;
      this.paid = row.paid;
      this.change = row.change;
    },
    pickDateRange(value) {
      let startDate = value[0]
        .add(-new Date().getTimezoneOffset() / 60, "hour")
        .toISOString();
      let endDate = value[1]
        .endOf("day")
        .add(-new Date().getTimezoneOffset() / 60, "hour")
        .toISOString();
      console.log(startDate, endDate);
      axios
        .get(`/api/v1/orders/filter?startDate=${startDate}&endDate=${endDate}`)
        .then((response) => {
          this.orders = response.data;
        });
    },
  },

  computed: {
    revenue() {
      return this.orders.reduce((acc, item) => acc + item.total, 0);
    },
    totalItemSold() {
      return this.orders.reduce(
        (acc, item) =>
          acc +
          item.order_items.reduce((acc1, item1) => acc1 + item1.quantity, 0),
        0
      );
    },
  },

  filters: {
    toMoment: function (date) {
      return moment(date)
        .add(-(new Date().getTimezoneOffset() / 60), "hour")
        .format("MM/DD/YYYY, h:mm a");
      // return moment(date).format("MM/DD/YYYY, h:mm a");
    },
    currency: function (value) {
      return value && value.toLocaleString() || 0;
    },
  },
};
</script>