<template>
  <v-layout>
    <v-col cols="8" md="8">
      <v-card outlined height="100%">
        <v-container class="mt-5" flat>
          <v-row>
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
          <v-row>
            <v-col cols="12" sm="4">
              <v-hover v-slot="{ hover }" open-delay="200">
                <v-card color="cyan darken-1" :elevation="hover ? 16 : 2">
                  <v-row>
                    <v-col cols="12" sm="8">
                      <v-list-item three-line>
                        <v-list-item-content>
                          <v-list-item-title class="text-h4 md-1 white--text">
                            ${{revenue}}
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
            <v-col cols="12" sm="4">
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
            <v-col cols="12" sm="4">
              <v-hover v-slot="{ hover }" open-delay="200">
                <v-card color="orange darken-1" :elevation="hover ? 16 : 2">
                  <v-row>
                    <v-col cols="12" sm="8">
                      <v-list-item three-line>
                        <v-list-item-content>
                          <v-list-item-title class="text-h4 mb-1 white--text">
                            {{totalItemSold}}
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
                </v-data-table>
              </v-sheet>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </v-col>
    <v-col cols="4" md="4">
      <v-card outlined height="100%">
        <v-list-item three-line>
          <v-list-item-content>
            <v-list-item-title class="text-h5 mb-1"> Orders </v-list-item-title>
            <v-sheet elevation="2">
              <v-data-table
                :headers="orderItemHeaders"
                :items="orderItems"
                :search="search"
                @click:row="handleClick"
              >
                <template v-slot:[`item.created_date`]="{ item }">
                  <span>{{ item.created_date | toMoment }}</span>
                </template>
              </v-data-table>
            </v-sheet>
          </v-list-item-content>
        </v-list-item>
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
      orderHeaders: [
        {
          text: "Code",
          align: "start",
          sortable: true,
          value: "code",
        },
        { text: "Date", value: "created_date" },
        { text: "Total", value: "subtotal" },
        { text: "Paid", value: "paid" },
        { text: "Change", value: "change" },
        { text: "Customer", value: "customer.name" },
        { text: "Cashier", value: "user.username" },
      ],
      orderItemHeaders: [
        { text: "Name", value: "item_name" },
        { text: "Quantity", value: "quantity" },
        { text: "Price", value: "price" },
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
          order_items: [
           
          ],
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
    },
    pickDateRange(value) {
      let startDate = value[0].add(-(new Date().getTimezoneOffset())/60, "hour").toISOString();
      let endDate = value[1].endOf("day").add(-(new Date().getTimezoneOffset())/60, "hour").toISOString()
      console.log(startDate, endDate)
      axios.get(`/api/v1/orders/filter?startDate=${startDate}&endDate=${endDate}`)
      .then((response) => {
        this.orders = response.data;
      })
    },
  },

  computed: {
    revenue(){
      return this.orders.reduce((acc, item) => acc + item.subtotal, 0)
    },
    totalItemSold(){
      return this.orders.reduce((acc, item)=> acc + item.order_items.length, 0)
    }
  },

  filters: {
    toMoment: function (date) {
      return moment(date).format("MM/DD/YYYY, h:mm a");
    },
  },
};
</script>